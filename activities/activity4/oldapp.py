import datetime
import os
import pprint
import json

from tempfile import mkdtemp
from flask import Flask, jsonify, request, render_template, url_for, session, abort, send_from_directory

from flask_caching import Cache
from werkzeug.exceptions import Forbidden
from pylti1p3.contrib.flask import FlaskOIDCLogin, FlaskMessageLaunch, FlaskRequest, FlaskCacheDataStorage
from pylti1p3.deep_link_resource import DeepLinkResource
from pylti1p3.grade import Grade
from pylti1p3.lineitem import LineItem
from pylti1p3.tool_config import ToolConfJsonFile
from pylti1p3.registration import Registration
from flask_session import Session

class ReverseProxied:
    def __init__(self, app):
        self.app = app

    def __call__(self, environ, start_response):
        scheme = environ.get('HTTP_X_FORWARDED_PROTO')
        if scheme:
            environ['wsgi.url_scheme'] = scheme
        return self.app(environ, start_response)

app = Flask(__name__)
app.wsgi_app = ReverseProxied(app.wsgi_app)



config = {
    "DEBUG": True,
    "ENV": "development",
    "CACHE_TYPE": "simple",
    "CACHE_DEFAULT_TIMEOUT": 600,
    "SECRET_KEY": "replace-me",
    "SESSION_TYPE": "filesystem",
    "SESSION_FILE_DIR": mkdtemp(),
    "SESSION_COOKIE_NAME": "lti1p3session-id",
    "SESSION_COOKIE_HTTPONLY": True,
    "SESSION_COOKIE_SECURE": True,   # should be True in case of HTTPS usage (production)
    "SESSION_COOKIE_SAMESITE": "None",  # should be 'None' in case of HTTPS usage (production)
    "SESSION_COOKIE_PARTITIONED ": True,
    "SESSION_PERMANENT": True,
    "PERMANENT_SESSION_LIFETIME": datetime.timedelta(minutes=60), 
    "DEBUG_TB_INTERCEPT_REDIRECTS": False
}
app.config.from_mapping(config)
cache = Cache(app)
# Initialize session extension
Session(app)

def get_lti_config_path():
    return os.path.join(app.root_path, '..', 'configs', 'registrations.json')


def get_launch_data_storage():
    return FlaskCacheDataStorage(cache)


def get_jwk_from_public_key(key_name):
    key_path = os.path.join(app.root_path, '..', 'configs', key_name)
    f = open(key_path, 'r')
    key_content = f.read()
    jwk = Registration.get_jwk(key_content)
    f.close()
    return jwk

@app.route("/home")
def home():
    # Get launch data from session
    launch_data = session.get('launch_data', {})
    launch_id = session.get('launch_id', '')

    
    tpl_kwargs = {
        'page_title': "Home",
        'launch_id': launch_id,
        'target_link_uri': launch_data.get('https://purl.imsglobal.org/spec/lti/claim/target_link_uri', ''),
        'user_data': {
            'sub': launch_data.get('sub', ''),
            'name': launch_data.get('name', ''),
            'family_name': launch_data.get('family_name', ''),
            'given_name': launch_data.get('given_name', ''),
            'email': launch_data.get('email', ''),
            'sourced_id': launch_data.get('https://purl.imsglobal.org/spec/lti/claim/lis', '{}').get('person_sourcedid', ''),
        },
         'context_data': {
            **launch_data.get('https://purl.imsglobal.org/spec/lti/claim/context', {}),
            'sourced_id': launch_data.get('https://purl.imsglobal.org/spec/lti/claim/lis', {}).get('course_section_sourcedid', '')
        },
        'user_roles': launch_data.get('https://purl.imsglobal.org/spec/lti/claim/roles', []),
        'resource_link': launch_data.get('https://purl.imsglobal.org/spec/lti/claim/resource_link', {})
    }
    return render_template("home.html", **tpl_kwargs)

# Load the courses from the JSON file
def load_courses():
    courses_path =  os.path.join(app.root_path, '..', 'configs', 'resources.json')
    with open(courses_path) as f:
        courses = json.load(f)
    return courses


def deeplink():
    # Get launch data from session
    launch_data = session.get('launch_data', {})
    launch_id = session.get('launch_id', '')

    courses = load_courses()
    
    tpl_kwargs = {
        'page_title': "Deeplinking",
        "courses": courses,
        'launch_id': launch_id,
        'target_link_uri': launch_data.get('https://purl.imsglobal.org/spec/lti/claim/target_link_uri', ''),
        'user_data': {
            'sub': launch_data.get('sub', ''),
            'name': launch_data.get('name', ''),
            'family_name': launch_data.get('family_name', ''),
            'given_name': launch_data.get('given_name', ''),
            'email': launch_data.get('email', ''),
            'sourced_id': launch_data.get('https://purl.imsglobal.org/spec/lti/claim/lis', '{}').get('person_sourcedid', ''),
        },
         'context_data': {
            **launch_data.get('https://purl.imsglobal.org/spec/lti/claim/context', {}),
            'sourced_id': launch_data.get('https://purl.imsglobal.org/spec/lti/claim/lis', {}).get('course_section_sourcedid', '')
        },
        'user_roles': launch_data.get('https://purl.imsglobal.org/spec/lti/claim/roles', []),
        'resource_link': launch_data.get('https://purl.imsglobal.org/spec/lti/claim/resource_link', {})
    }
    return render_template("deeplink.html", **tpl_kwargs)

@app.route("/")
def basic():
    return render_template("basic.html")

@app.route('/jwks/', methods=['GET'])
def get_jwks():
    tool_conf = ToolConfJsonFile(get_lti_config_path())
    return jsonify(tool_conf.get_jwks())


@app.route("/nrps")
def nrps():
    return render_template("nrps.html")

@app.route("/ags")
def ags():
    launch_id = session.get('launch_id', '')

    tool_conf = ToolConfJsonFile(get_lti_config_path())
    flask_request = FlaskRequest()
    launch_data_storage = get_launch_data_storage()
    message_launch = FlaskMessageLaunch.from_cache(launch_id, flask_request, tool_conf,
                                                   launch_data_storage=launch_data_storage)

    if not message_launch.has_ags():
        raise Forbidden('AGS not enabled!')

    ags_service = message_launch.get_ags()

    # Fetch members and line items
    members = get_nrps_members()
    lineitems = ags_service.get_lineitems()

    # Create a dictionary to store grades by user and lineitem id for fast lookup
    grade_lookup = {}
    for item in lineitems:
        lineitem = ags_service.find_lineitem_by_id(item['id'])
        grades = ags_service.get_grades(lineitem)
        if grades:
            for grade in grades:
                grade_lookup[(grade['userId'], item['id'])] = grade['resultScore']

    # Create gradebook data
    gradebook = []
    for member in members:
        row = [member['user_id'], member['name']]
        for item in lineitems:
            # Use the grade_lookup dictionary for fast access to grades
            grade = grade_lookup.get((member['user_id'], item['id']), '')
            row.append(grade)
        gradebook.append(row)

    # Pretty print the gradebook for debugging
    pprint.pprint(gradebook)

    # Render the template with gradebook data
    tpl_kwargs = {
        'page_title': "Assignments and Grades",
        'lineitems': lineitems,
        'gradebook': gradebook
    }

    return render_template("ags.html", **tpl_kwargs)


# @app.route("/assignments_grades")
# def assignments_grades():
#     return render_template("assignments_grades.html")

@app.route("/id_token")
def id_token():
    # Get launch data from session
    launch_data = session.get('launch_data', {})
    launch_id = session.get('launch_id', '')
    
    tpl_kwargs = {
        'page_title': "ID Token",
        'launch_id': launch_id,
        'launch_data': launch_data
    }

    return render_template("id_token.html", **tpl_kwargs)


@app.route('/login/', methods=['GET', 'POST'])
def login():
    tool_conf = ToolConfJsonFile(get_lti_config_path())
    launch_data_storage = get_launch_data_storage()

    flask_request = FlaskRequest()
    launch_url = url_for('launch', _external=True)
    target_link_uri = flask_request.get_param('target_link_uri')
    if not target_link_uri:
        raise Exception('Missing "target_link_uri" param')

    oidc_login = FlaskOIDCLogin(flask_request, tool_conf, launch_data_storage=launch_data_storage)
    return oidc_login\
        .enable_check_cookies()\
        .redirect(launch_url)


@app.route('/launch/', methods=['POST'])
def launch():
    tool_conf = ToolConfJsonFile(get_lti_config_path())
    flask_request = FlaskRequest()
    launch_data_storage = get_launch_data_storage()
    message_launch = FlaskMessageLaunch(flask_request, tool_conf, launch_data_storage=launch_data_storage)
    message_launch_data = message_launch.get_launch_data()
    # pprint.pprint(message_launch_data)

     # Store the launch data in the session
    session['launch_data'] = message_launch_data
    session['launch_id'] = message_launch.get_launch_id()   

    if message_launch.is_deep_link_launch():
        return deeplink()
    return home()



@app.route('/api/nrps/members', methods=['GET'])
def get_nrps_members():
    launch_id = session.get('launch_id', '')

    tool_conf = ToolConfJsonFile(get_lti_config_path())
    flask_request = FlaskRequest()
    launch_data_storage = get_launch_data_storage()
    message_launch = FlaskMessageLaunch.from_cache(launch_id, flask_request, tool_conf,
                                                           launch_data_storage=launch_data_storage)
    if not message_launch.has_nrps():
        raise Forbidden('NRPS not enabled!')
    
    members = message_launch.get_nrps().get_members()
    return members

@app.route('/dl/<resource_id>/', methods=['GET', 'POST'])
def deeplink_response(resource_id):


    launch_id = session.get('launch_id', '')
    tool_conf = ToolConfJsonFile(get_lti_config_path())
    flask_request = FlaskRequest()
    launch_data_storage = get_launch_data_storage()
    message_launch = FlaskMessageLaunch.from_cache(launch_id, flask_request, tool_conf,
                                                   launch_data_storage=launch_data_storage)

    if not message_launch.is_deep_link_launch():
        raise Forbidden('Must be a deep link!')

    courses = load_courses()
    course = next((course for course in courses if course['id'] == int(resource_id)), None)
    
    if not course:
        abort(404, description=f"Course with ID {resource_id} not found")
    

    launch_url = url_for('home', _external=True) + '/resource/' + resource_id + '/'

    resource = DeepLinkResource()
    resource.set_url(launch_url) \
        .set_title(course.get("title", "Resource " + resource_id))
    
    # Get the optional 'model_id' from query parameters
    model_id = request.args.get('model_id', 'default')
    
    if model_id:
        resource.set_custom_params({'model_id': model_id})
    

    html = message_launch.get_deep_link().output_response_form([resource])
    return html


# @app.route('/api/ags/gradebook', methods=['GET'])
# def get_gradebook():
#     launch_id = session.get('launch_id', '')

#     tool_conf = ToolConfJsonFile(get_lti_config_path())
#     flask_request = FlaskRequest()
#     launch_data_storage = get_launch_data_storage()
#     message_launch = FlaskMessageLaunch.from_cache(launch_id, flask_request, tool_conf,
#                                                            launch_data_storage=launch_data_storage)
#     if not message_launch.has_ags():
#         raise Forbidden('AGS not enabled!')
#     ags_service = message_launch.get_ags()

#     lineitems = ags_service.get_lineitems()
    
#     return lineitems



if __name__ == '__main__':
    app.run(host='0.0.0.0', port=3000, debug=True)
