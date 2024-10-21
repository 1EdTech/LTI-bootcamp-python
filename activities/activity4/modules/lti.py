from flask import session, render_template, redirect, url_for, jsonify
from pylti1p3.contrib.flask import FlaskOIDCLogin, FlaskMessageLaunch, FlaskRequest, FlaskCacheDataStorage
from pylti1p3.tool_config import ToolConfJsonFile

from utils import get_lti_config_path, get_launch_data_storage

def register(app):
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

