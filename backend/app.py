from flask import Flask, g, request, session, render_template, jsonify, abort
from flask.json import JSONEncoder
from flask_pymongo import PyMongo, ObjectId
from pymongo.errors import OperationFailure

import re

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

def mongo_one(collection, str_id):
    return mongo.db[collection].find_one_or_404({ '_id': ObjectId(str_id) })

@app.route('/', methods=['GET'])
def index():
    """Render the main application page."""
    return render_template('index.html')

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

    args = { i: request.form[i] for i in request.form }

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

    _id = request.form.get('_id', None)
    if _id is None:
        abort(400)

    if request.method == 'GET':
        return mongo.send_file(_id, FILE_STORAGE)

    # request.method == 'POST'
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
