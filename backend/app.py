from flask import Flask, g, request, session, render_template, jsonify, abort, send_file
from flask.json import JSONEncoder
from flask_pymongo import PyMongo, ObjectId
from pymongo.errors import OperationFailure
from gridfs import GridFSBucket, NoFile
import jinja2
from jinja2 import Template

import re
import os
from shutil import rmtree
import uuid
import subprocess

class MongoIdEncoder(JSONEncoder):
    def default(self, o):
        if isinstance(o, ObjectId):
            return str(o)
        return JSONEncoder.default(self, o)

Flask.json_encoder = MongoIdEncoder

app = Flask(__name__, static_folder='../dist/static', template_folder='../dist', instance_relative_config=True)
app.config.from_object('settings')
app.config.from_envvar('BEKIGA_SETTINGS', silent=True)

if app.debug:
    from flask_cors import CORS
    cors = CORS(app, resources={
        '/api/*': { 'origins': '*' },
        '/_suggestions/': { 'origins': '*' }
    })

mongo = PyMongo(app)
FILE_STORAGE = 'files'

TEX_PATH = 'tex/'

tex_jinja = jinja2.Environment(
    block_start_string = '\BLOCK{',
    block_end_string = '}',
    variable_start_string = '\VAR{',
    variable_end_string = '}',
    comment_start_string = '\#{',
    comment_end_string = '}',
    line_statement_prefix = '%%',
    line_comment_prefix = '%#',
    trim_blocks = True,
    autoescape = False,
    loader = jinja2.FileSystemLoader(os.path.abspath('.'))
)

def mongo_one(collection, str_id):
    return mongo.db[collection].find_one_or_404({ '_id': ObjectId(str_id) })

def _resolve_foreign(obj, key, foreign_collection):
    """
    Resolve the value at `key` as foreign key on the given `foreign_collection`
    """
    f_id = obj.get(key, None)
    if f_id is None:
        abort(404)
    
    obj[key] = mongo_one(foreign_collection, f_id)

class FileDownloader:
    fs = None
    fname = None
    revision = None

    def __init__(self, fs, fname, revision=-1):
        self.fs = fs
        self.fname = fname
        self.revision = revision
    
    def download(self, dst_folder):
        dst = os.path.join(dst_folder, self.fname)
        try:
            with open(dst, 'wb') as dst_file:
                self.fs.download_to_stream_by_name(self.fname,
                                                   dst_file,
                                                   revision=self.revision)
        except NoFile:
            return None
        
        return self.fname


def _render(**kvargs):
    template = tex_jinja.get_template(os.path.join(TEX_PATH, 'template.tex'))
    return template.render(**kvargs)


def render_protocol(protocol):
    sub_folder = os.path.join(TEX_PATH, uuid.uuid4().hex)
    os.mkdir(sub_folder)

    protocol['inspectionStandards'] = r' \\ '.join(protocol['inspectionStandards'])
    tmp = protocol['facility']['picture']
    if tmp:
        protocol['facility']['picture'] = tmp.download(sub_folder);
    for entry in protocol['entries']:
        cat = entry['category']
        cat['inspectionStandards'] = ', '.join(map(lambda i: i['name'], cat['inspectionStandards']))
        for flaw in entry['flaws']:
            flaw['notes'] = flaw['notes'].replace('\r\n', r'\newline ').replace('\n', r'\newline')
            if flaw['picture']:
                flaw['picture'] = flaw['picture'].download(sub_folder)
    
    with open(os.path.join(sub_folder, 'main.tex'), 'w') as dst_file:
        dst_file.write(_render(**protocol))
    
    compiler = subprocess.Popen([
        'pdflatex',
        '-synctex=1',
        '-interaction=nonstopmode',
        'main.tex'
    ], cwd=sub_folder)
    compiler.wait()

    pdf = open(os.path.join(sub_folder, 'main.pdf'), 'rb')
    resp = send_file(pdf, attachment_filename='protocol.pdf')

    rmtree(sub_folder)

    return resp

def find_full_protocol(str_id):
    """
    Get the protocol with id `str_id`. Resolves all foreign keys. Pictures will 
    be available as FileDownloader s.
    Returns a dictionary representing the protocol.
    """
    protocol = {
        'title': '',
        'inspectionStandards': '',
        'inspectionDate': '',
        'attendees': '',
        'facility': '',
        'inspector': '',
        'issuer': '',
        'entries': [], 
    }

    protocol.update(mongo_one('protocols', str_id))

    protocol['inspectionStandards'] = protocol['inspectionStandards'].replace('\r\n', '\n').split('\n')

    foreigns = [
        ('inspector', 'persons'),
        ('issuer', 'organizations'),
        ('facility', 'facilities')
    ]
    [ _resolve_foreign(protocol, *i) for i in foreigns ]

    _resolve_foreign(protocol['inspector'], 'organization', 'organizations')

    fs = GridFSBucket(mongo.db, 'files')

    if protocol['facility'].get('picture', False):
        fac = protocol['facility']
        fname = 'facility_' + str(fac['_id']) + '.' + fac['picture']
        protocol['facility']['picture'] = FileDownloader(fs, fname)
    
    entries = []
    for entry_id in protocol['entries'].split(','):
        entry = {
            'category': '',
            'title': '',
            'manufacturer': '',
            'yearBuilt': '',
            'inspectionSigns': '',
            'manufactureInfoAvailable': '',
            'easyAccess': '',
            'flaws': [],
            'index': '',
        }
        entry.update(mongo_one('entries', entry_id))

        _resolve_foreign(entry, 'category', 'categories')
        standards = []
        for std_id in entry['category']['inspectionStandards'].split(','):
            standards.append(mongo_one('inspectionStandards', std_id))
        
        entry['category']['inspectionStandards'] = standards

        flaws = []
        for flaw_id in entry['flaws'].split(','):
            flaw = {
                'flaw': '',
                'priority': '',
                'notes': '',
                'picture': '',
            }
            flaw.update(mongo_one('flaws', flaw_id))

            if flaw['picture']:
                fname = 'flaw_' + str(flaw['_id']) + '.' + flaw['picture']
                flaw['picture'] = FileDownloader(fs, fname)
            
            flaws.append(flaw)
        
        entry['flaws'] = flaws
        entries.append(entry)
    
    protocol['entries'] = entries

    return protocol

@app.route('/', methods=['GET'])
def index():
    """Render the main application page."""
    return render_template('index.html')

@app.route('/render/<_id>', methods=['GET'])
def render(_id):
    """
    Render the protocol identified given by the request argument `_id`.
    Returns the rendered protocol as pdf.
    """
    return render_protocol(find_full_protocol(_id))

def api(collection):
    """
    Handles api request for the given collection.
    Returns a json object with a `result` field. Its content varies by request method.

    GET:
    The request may specify arguments to filter the results on the given collection.
    If `_id` is given a single document is returned, else a list of documents is returned.

    POST:
    Constructs a new document using the arguments given and inserts it into the collection.
    Returns the id if the new document.

    PATCH:
    The request should specify arguments `find` and `data`. They are used to select and update
    the documents.
    If `_id` is given to find the document a single document-id is returned, else the document-ids
    of all updated documents are returned.

    DELETE:
    The request may specify arguments to filter results. All results matched by the filter
    are deleted.
    Returns the number of deleted documents
    """

    if request.method == 'PATCH' or request.method == 'POST':
        if request.form is None:
            abort(400)
        args = { i: request.form[i] for i in request.form }
    else:
        if request.args is None:
            abort(400)
        args = { i: request.args[i] for i in request.args }

    result = None
    if request.method == 'GET':
        if '_id' in args:
            result = mongo_one(collection, args['_id'])
        else:
            result = list(mongo.db[collection].find(args))
    elif request.method == 'POST':
        result = { '_id': str(mongo.db[collection].insert_one(args).inserted_id) }
    elif request.method == 'PATCH':
        find = args.get('find', None)
        data = args.get('data', None)
        if find is None or data is None:
            abort(400)
        if '_id' in find:
            result = str(mongo.db[collection].update_one({ '_id': ObjectId(find['_id']) }, data).upserted_id)
        else:
            result = mongo.db[collection].update_many(find, data).upserted_id
            result = list(map(str, result))
    elif request.method == 'DELETE':
        if '_id' in args:
            result = mongo.db[collection].delete_one({ '_id': ObjectId(args['_id']) }).deleted_count
        else:
            result = mongo.db[collection].delete_many(args).deleted_count
    else:
        abort(400)
    
    return jsonify(result=result)

@app.route('/api/protocols/', methods=['GET', 'POST', 'PATCH', 'DELETE'])
def protocols():
    return api('protocols')

@app.route('/api/categories/', methods=['GET', 'POST', 'PATCH', 'DELETE'])
def categories():
    return api('categories')

@app.route('/api/facilities/', methods=['GET', 'POST', 'PATCH', 'DELETE'])
def facilities():
    return api('facilities')

@app.route('/api/inspectionStandards/', methods=['GET', 'POST', 'PATCH', 'DELETE'])
def inspectionStandards():
    return api('inspectionStandards')

@app.route('/api/organizations/', methods=['GET', 'POST', 'PATCH', 'DELETE'])
def organizations():
    return api('organizations')

@app.route('/api/persons/', methods=['GET', 'POST', 'PATCH', 'DELETE'])
def persons():
    return api('persons')

@app.route('/api/entries/', methods=['GET', 'POST', 'PATCH', 'DELETE'])
def entries():
    return api('entries')

@app.route('/api/flaws/', methods=['GET', 'POST', 'PATCH', 'DELETE'])
def flaws():
    return api('flaws')

@app.route('/api/files/', methods=['GET', 'POST'])
def files():
    """
    Handles up-/downloads of files.
    The request should provide a field `_id` identifying the file.

    POST:
    The request should provide the file.
    """


    if request.method == 'GET':
        _id = request.args.get('_id', None)
        if _id is None:
            abort(400)
        return mongo.send_file(_id, FILE_STORAGE)

    # request.method == 'POST'
    _id = request.form.get('_id', None)
    if _id is None:
        abort(400)
    file = [ request.files[i] for i in request.files ]
    if len(file) != 1:
        abort(400)
    file = file[0]
    mongo.save_file(_id, file, FILE_STORAGE)
    return jsonify(_id=_id)

@app.route('/_suggestions/', methods=['GET'])
def suggestions():
    """
    Build a suggestion list for requested types.

    GET:
    The request should provide the following args:
    {
        "collection": "the collection to query",
        "on": "the key of the values to be searched",
        "q": "the `query` (i.e. the string to search for)"
    }
    Returns matching values of the given key. Duplicates are removed.
    Result will be sorted using default behaviour.
    Results are limited to 10 distinct matches.
    """

    collection = request.args.get('collection', None)
    if collection is None:
        abort(400)
    
    on = request.args.get('on', None)
    if on is None:
        abort(400)
    
    q = request.args.get('q', None)
    if q is None:
        abort(400)
    
    q = re.escape(q)
    
    try:
        cursor = mongo.db[collection].find({ on: { '$regex': q } })
    except OperationFailure:
        abort(500)
    
    result = set(str(i[on]) for i in cursor)
    result = list(result)[:10]
    result.sort();
    
    return jsonify(data=result)
