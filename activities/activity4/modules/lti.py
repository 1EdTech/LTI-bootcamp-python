from flask import session, render_template, redirect, url_for, jsonify
from pylti1p3.contrib.flask import FlaskOIDCLogin, FlaskMessageLaunch, FlaskRequest
from pylti1p3.tool_config import ToolConfJsonFile

from utils import get_lti_config_path, get_launch_data_storage, find_course_by_id

def register(app):
    @app.route("/home")
    def home():
        # Check if launch data exists in the session
        launch_data = session.get('launch_data')
        
        if not launch_data:
            return render_template("warning.html", message="You must access this application via a valid LTI 1.3 launch.")

        # Get necessary data from the session
        launch_id = session.get('launch_id', '')
        target_link_uri = launch_data.get('https://purl.imsglobal.org/spec/lti/claim/target_link_uri', '')
        user_data = {
            'name': launch_data.get('name', ''),
            'sub': launch_data.get('sub', ''),
            'email': launch_data.get('email', ''),
            'sourced_id': launch_data.get('https://purl.imsglobal.org/spec/lti/claim/lis', {}).get('person_sourcedid', ''),
        }
        user_roles = launch_data.get('https://purl.imsglobal.org/spec/lti/claim/roles', [])
        resource_link = launch_data.get('https://purl.imsglobal.org/spec/lti/claim/resource_link', {})
        context_data = launch_data.get('https://purl.imsglobal.org/spec/lti/claim/context', {})
        
        # Lookup resource details if the target_link_uri is a valid resource
        resource_details = {}
        if "resource/" in target_link_uri:
            # Extract the resource ID from the target_link_uri
            resource_id = target_link_uri.split('/')[-2]  # Getting the second to last part
            resource_details = find_course_by_id(app, resource_id)

        # Check if model_id exists in custom claims
        model_id = launch_data.get('https://purl.imsglobal.org/spec/lti/claim/custom', {}).get('model_id')

        tpl_kwargs = {
            'page_title': "Home",
            'launch_id': launch_id,
            'target_link_uri': target_link_uri,
            'user_data': user_data,
            'user_roles': user_roles,
            'resource_link': resource_link,
            'context_data': context_data,
            'resource_details': resource_details,
            'model_id': model_id,
        }
        return render_template("home.html", **tpl_kwargs)

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
        tool_conf = ToolConfJsonFile(get_lti_config_path(app))
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
        tool_conf = ToolConfJsonFile(get_lti_config_path(app))
        flask_request = FlaskRequest()
        launch_data_storage = get_launch_data_storage()
        message_launch = FlaskMessageLaunch(flask_request, tool_conf, launch_data_storage=launch_data_storage)
        message_launch_data = message_launch.get_launch_data()
        # pprint.pprint(message_launch_data)

        # Store the launch data in the session
        session['launch_data'] = message_launch_data
        session['launch_id'] = message_launch.get_launch_id()   

        if message_launch.is_deep_link_launch():
            return redirect(url_for('deeplink'))  
        return redirect(url_for('home'))
    
    @app.route('/jwks/', methods=['GET'])
    def get_jwks():
        tool_conf = ToolConfJsonFile(get_lti_config_path(app))
        return jsonify(tool_conf.get_jwks())

