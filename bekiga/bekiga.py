from flask import Flask, g, request, session, render_template, jsonify, abort
from flask_pymongo import PyMongo, ObjectId
from pymongo.errors import OperationFailure

# TODO remove for production
from functools import update_wrapper
from datetime import timedelta
from flask import make_response, current_app
# end

app = Flask(__name__, instance_relative_config=True)
app.config.from_object('bekiga.settings')
app.config.from_envvar('BEKIGA_SETTINGS', silent=True)

mongo = PyMongo(app)

def mongo_one(collection, str_id):
    return mongo.db[collection].find_one_or_404({ '_id': ObjectId(str_id) })

# TODO remove for production
def crossdomain(origin=None, methods=None, headers=None,
                max_age=21600, attach_to_all=True,
                automatic_options=True):
    """
    ONLY FOR DEV
    """
    if methods is not None:
        methods = ', '.join(sorted(x.upper() for x in methods))
    if headers is not None and not isinstance(headers, str):
        headers = ', '.join(x.upper() for x in headers)
    if not isinstance(origin, str):
        origin = ', '.join(origin)
    if isinstance(max_age, timedelta):
        max_age = max_age.total_seconds()

    def get_methods():
        if methods is not None:
            return methods

        options_resp = current_app.make_default_options_response()
        return options_resp.headers['allow']

    def decorator(f):
        def wrapped_function(*args, **kwargs):
            if automatic_options and request.method == 'OPTIONS':
                resp = current_app.make_default_options_response()
            else:
                resp = make_response(f(*args, **kwargs))
            if not attach_to_all and request.method != 'OPTIONS':
                return resp

            h = resp.headers

            h['Access-Control-Allow-Origin'] = origin
            h['Access-Control-Allow-Methods'] = get_methods()
            h['Access-Control-Max-Age'] = str(max_age)
            if headers is not None:
                h['Access-Control-Allow-Headers'] = headers
            return resp

        f.provide_automatic_options = False
        return update_wrapper(wrapped_function, f)
    return decorator
#end

@app.route('/', methods=['GET'])
def index():
    """Render the main application page."""
    return render_template('index.html')


@app.route('/_uploads/flaws/', methods=['GET', 'POST'])
@crossdomain(origin='*')
def pictures():
    """
    Handles up-/downloads of flawInformation.
    
    POST:
    The request should provide the flawInformation and may provide
    a file `pic`.
    Returns the id of the stored record.

    GET:
    The request should provide an `id` corresponding to the picture to 
    download.
    """

    if request.method == 'POST':
        meta = { i: request.form[i] for i in request.form }
        _id = str(mongo.db.flaw_information.insert_one(meta).inserted_id)

        fil = request.files.get('pic', None)
        if fil is not None:
            mongo.save_file(_id, request.files['pic'], 'flaw_pictures')
        return jsonify(id=_id)

    _id = request.args.get('id', None)
    flaw = mongo_one('flaw_information', _id)
    fname = str(flaw['_id'])

    return mongo.send_file(fname, 'flaw_pictures')


@app.route('/_uploads/facilities/', methods=['GET', 'POST'])
@crossdomain(origin='*')
def pictures():
    """
    Handles up-/downloads of facilities.
    
    POST:
    The request should provide the flawInformation and may provide
    a file `pic`.
    Returns the id of the stored record.

    GET:
    The request should provide an `id` corresponding to the picture to 
    download.
    """

    if request.method == 'POST':
        meta = { i: request.form[i] for i in request.form }
        _id = str(mongo.db.facilities.insert_one(meta).inserted_id)

        fil = request.files.get('pic', None)
        if fil is not None:
            mongo.save_file(_id, request.files['pic'], 'facility_pictures')
        return jsonify(id=_id)

    _id = request.args.get('id', None)
    facility = mongo_one('facilities', _id)
    fname = str(facility['_id'])

    return mongo.send_file(fname, 'facility_pictures')

@app.route('/_suggestions/', methods=['GET'])
@crossdomain(origin='*')
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
        abort(404)
    
    on = request.args.get('on', None)
    if on is None:
        abort(404)
    
    q = request.args.get('q', None)
    if q is None:
        abort(404)
    
    try:
        cursor = mongo.db[collection].find({ on: { '$regex': q } })
    except OperationFailure:
        abort(404)
    result = set(str(i[on]) for i in cursor)
    result = list(result)[:10]
    result.sort();
    
    return jsonify(data=result)


@app.route('/_data/', methods=['GET', 'POST'])
@crossdomain(origin='*')
def data():
    """
    Request or store data.

    POST:
    The request should provide a json object of the form:
    {
        "collection": "the collection to query",
        "data": "the data to be stored"
    }
    Returns the id of the created record.

    GET:
    The request should provide the following args:
    {
        "collection": "the collection to query",
        "id": "the id of the desired object"
    }
    Returns the data if it exists, 404 if not.
    """
    

    if request.method == 'POST':
        collection = request.json.get('collection', None)
        if collection is None:
            abort(404)
        data = request.json.get('data', None)
        print(data)
        if data is None:
            abort(404)
        
        if isinstance(data, list):
            _id = list(map(str, mongo.db[collection].insert_many(data).inserted_id))
        else:
            _id = str(mongo.db[collection].insert_one(data).inserted_id)
        return jsonify({ 'id': _id })

    #GET
    collection = request.args.get('collection', None)
    if collection is None:
        abort(404)
    _id = request.args.get('id', None)

    return jsonify(mongo_one(collection, _id))


@app.route('/api/protocols/', methods=['GET', 'POST', 'PATCH', 'DELETE'])
@crossdomain(origin='*')
def data():

    args = dict(request.args)
    
    if request.method == 'POST':
        id_ = mongo.db.protocols.insert_one(args).inserted_id
        return jsonify(id_=str(id_))
    elif request.method == 'PATCH':
        
        pass
    elif request.method == 'DELETE':
        pass
    
    #else request.method == 'GET'
    cursor = mongo.db.protocols.find(args)
    result = list(cursor)
    for i in result:
        i.update({ '_id': str(i['_id']) })
    
    return jsonify(data=result)
    

