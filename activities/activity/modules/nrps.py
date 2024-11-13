from flask import render_template, session
from werkzeug.exceptions import Forbidden
from utils import get_message_launch

def register(app):
    @app.route("/nrps/")
    def nrps():
        launch_data = session.get('launch_data')
        
        if not launch_data:
            return render_template("warning.html", message="You must access this application via a valid LTI 1.3 launch.")

        activity_id = int(launch_data.get('https://purl.imsglobal.org/spec/lti/claim/custom', {}).get('activity_id', 1))
        brand = launch_data.get('https://purl.imsglobal.org/spec/lti/claim/custom', {}).get('brand', 'corporate')

        tpl_kwargs = {
            'page_title': "Names and Roles Provisioning Service",
            'activity_id': activity_id,
            'brand': brand,
        }

        return render_template("nrps.html", **tpl_kwargs)
    
    @app.route('/api/nrps/members', methods=['GET'])
    def get_nrps_members():
        launch_id, message_launch = get_message_launch(app)

        if not message_launch.has_nrps():
            raise Forbidden('NRPS not enabled!')
        
        members = message_launch.get_nrps().get_members()
        return members
