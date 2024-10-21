from flask import session, render_template
from werkzeug.exceptions import Forbidden
from pylti1p3.contrib.flask import FlaskMessageLaunch, FlaskRequest
from pylti1p3.tool_config import ToolConfJsonFile
from utils import get_lti_config_path, get_launch_data_storage


def register(app):
    @app.route("/nrps/")
    def nrps():
        return render_template("nrps.html")
    
    @app.route('/api/nrps/members', methods=['GET'])
    def get_nrps_members():
        launch_id = session.get('launch_id', '')

        tool_conf = ToolConfJsonFile(get_lti_config_path(app))
        flask_request = FlaskRequest()
        launch_data_storage = get_launch_data_storage()
        message_launch = FlaskMessageLaunch.from_cache(launch_id, flask_request, tool_conf,
                                                            launch_data_storage=launch_data_storage)
        if not message_launch.has_nrps():
            raise Forbidden('NRPS not enabled!')
        
        members = message_launch.get_nrps().get_members()
        return members
