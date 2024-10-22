from flask import render_template
from werkzeug.exceptions import Forbidden
from utils import get_message_launch

def register(app):
    @app.route("/nrps/")
    def nrps():
        return render_template("nrps.html")
    
    @app.route('/api/nrps/members', methods=['GET'])
    def get_nrps_members():
        launch_id, message_launch = get_message_launch(app)

        if not message_launch.has_nrps():
            raise Forbidden('NRPS not enabled!')
        
        members = message_launch.get_nrps().get_members()
        return members
