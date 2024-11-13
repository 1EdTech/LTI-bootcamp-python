from flask import render_template, request, jsonify, session
from werkzeug.exceptions import Forbidden
from pylti1p3.lineitem import LineItem
from pylti1p3.grade import Grade
from urllib.parse import unquote 
from utils import get_message_launch
from datetime import datetime

def register(app):
    
    @app.route("/ags")
    def ags():
        launch_id, message_launch = get_message_launch(app)
        launch_data = session.get('launch_data')

        if not message_launch.has_ags():
            raise Forbidden('AGS not enabled!')

        ags_service = message_launch.get_ags()

        lineitems = ags_service.get_lineitems()

        activity_id = int(launch_data.get('https://purl.imsglobal.org/spec/lti/claim/custom', {}).get('activity_id', 1))
        brand = launch_data.get('https://purl.imsglobal.org/spec/lti/claim/custom', {}).get('brand', 'corporate')

        tpl_kwargs = {
            'page_title': "Assignments and Grades",
            'lineitems': lineitems,
            'activity_id': activity_id,
            'brand': brand
        }

        return render_template("ags.html", **tpl_kwargs)
    

    @app.route('/api/lineitem/<path:lineitem_id>', methods=['GET'])
    def get_lineitem(lineitem_id):
        lineitem_id = unquote(lineitem_id)  
        launch_id, message_launch = get_message_launch(app)

        if not message_launch.has_ags():
            return {'error': 'AGS not enabled!'}, 403

        ags_service = message_launch.get_ags()
        lineitems = ags_service.get_lineitems()

        lineitem_data = next((item for item in lineitems if item['id'] == lineitem_id), None)
        
        if lineitem_data:
            return {
                'id': lineitem_data.get('id'),
                'label': lineitem_data.get('label'),
                'maxScore': lineitem_data.get('scoreMaximum'),
                'resourceId': lineitem_data.get('resourceId'),
                'resourceLinkId': lineitem_data.get('resourceLinkId'),
                'tag': lineitem_data.get('tag')
            }
        else:
            return {'error': 'Line item not found'}, 404

    @app.route('/api/lineitem', methods=['GET'])
    def list_lineitems():
        
        launch_id, message_launch = get_message_launch(app)

        if not message_launch.has_ags():
            return {'error': 'AGS not enabled!'}, 403

        ags_service = message_launch.get_ags()
        lineitems = ags_service.get_lineitems()

        return lineitems 



    @app.route('/api/lineitem', methods=['POST'])
    def create_lineitem():
        launch_id, message_launch = get_message_launch(app)

        if not message_launch.has_ags():
            return {'error': 'AGS not enabled!'}, 403

        data = request.json 

        if not data:
            return {'error': 'No data provided'}, 400

        ags_service = message_launch.get_ags()

        lineitem = LineItem({
            "label": data.get("label"),
            "scoreMaximum": data.get("maxScore"),
            "resourceId": data.get("resourceId"),
            "tag": data.get("tag"),
        })

        try:
            ags_service.find_or_create_lineitem(lineitem) 
            return {'success': 'Line item created successfully'}, 201
        except Exception as e:
            return {'error': str(e)}, 500  
    

    @app.route('/api/lineitem/<path:lineitem_id>/grades', methods=['GET'])
    def get_grades_for_lineitem(lineitem_id):
        launch_id, message_launch = get_message_launch(app)
        
        if not message_launch.has_ags():
            return {'error': 'AGS not enabled!'}, 403

        ags_service = message_launch.get_ags()

        # Fetch grades associated with the specified line item
        try:
            lineitem = ags_service.find_lineitem_by_id(unquote(lineitem_id) )
            grades = ags_service.get_grades(lineitem)

            return jsonify(grades), 200  # Return the grades in JSON format
            
        except Exception as e:
            return {'error': str(e)}, 500 

    @app.route('/api/lineitem/<path:lineitem_id>/grade', methods=['POST'])
    def add_grade(lineitem_id):
        
        launch_id, message_launch = get_message_launch(app)
        if not message_launch.has_ags():
            return {'error': 'AGS not enabled!'}, 403
        
        lineitem_id = unquote(lineitem_id) 

        # Get the incoming data
        data = request.json

        # Validate incoming data
        if not data or 'scoreGiven' not in data or 'userId' not in data:
            return {'error': 'Invalid data provided'}, 400

        # Create a Grade object
        grade = Grade()
        grade.set_score_given(data['scoreGiven'])
        grade.set_score_maximum(data.get('scoreMaximum', 100))  # Default max score if not provided
        grade.set_user_id(data['userId'])
        grade.set_comment(data.get('comment', ''))  # Optional comment
        grade.set_activity_progress("Completed")  # Hardcoding as per requirement
        grade.set_grading_progress("FullyGraded")  # Hardcoding as per requirement
        grade.set_timestamp(datetime.utcnow().isoformat())  # Set current timestamp in ISO format

        ags_service = message_launch.get_ags()
        try:
            lineitem = ags_service.find_lineitem_by_id(lineitem_id) 
            ags_service.put_grade(grade, lineitem)  # Call to AGS service to add the grade
            return {'success': 'Grade added successfully'}, 201
        except Exception as e:
            return {'error': str(e)}, 500  # Handle any errors appropriately

