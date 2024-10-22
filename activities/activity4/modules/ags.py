from flask import render_template, request
from werkzeug.exceptions import Forbidden
from pylti1p3.lineitem import LineItem
from urllib.parse import unquote 
from utils import get_message_launch

def register(app):
    
    @app.route("/ags")
    def ags():
        launch_id, message_launch = get_message_launch(app)

        if not message_launch.has_ags():
            raise Forbidden('AGS not enabled!')

        ags_service = message_launch.get_ags()

        lineitems = ags_service.get_lineitems()

        tpl_kwargs = {
            'page_title': "Assignments and Grades",
            'lineitems': lineitems,
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
