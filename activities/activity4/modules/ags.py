from flask import session, render_template
from werkzeug.exceptions import Forbidden
from pylti1p3.contrib.flask import FlaskMessageLaunch, FlaskRequest
from pylti1p3.tool_config import ToolConfJsonFile
from utils import get_lti_config_path, get_launch_data_storage
import pprint

def register(app):
    
    @app.route("/ags")
    def ags():
        launch_id = session.get('launch_id', '')

        tool_conf = ToolConfJsonFile(get_lti_config_path(app))
        flask_request = FlaskRequest()
        launch_data_storage = get_launch_data_storage()
        message_launch = FlaskMessageLaunch.from_cache(launch_id, flask_request, tool_conf,
                                                    launch_data_storage=launch_data_storage)

        if not message_launch.has_ags():
            raise Forbidden('AGS not enabled!')

        ags_service = message_launch.get_ags()

        # Fetch members and line items
        members = [] # get_nrps_members()
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
