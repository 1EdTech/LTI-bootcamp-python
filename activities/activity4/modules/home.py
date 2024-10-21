# app/modules/home/routes.py
from flask import session, render_template


def register(app):
    @app.route("/")
    def landing_page():
        return render_template("landing_page.html")

    @app.route("/home")
    def home():
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
                'sourced_id': launch_data.get('https://purl.imsglobal.org/spec/lti/claim/lis', {}).get('person_sourcedid', ''),
            },
            'context_data': {
                **launch_data.get('https://purl.imsglobal.org/spec/lti/claim/context', {}),
                'sourced_id': launch_data.get('https://purl.imsglobal.org/spec/lti/claim/lis', {}).get('course_section_sourcedid', '')
            },
            'user_roles': launch_data.get('https://purl.imsglobal.org/spec/lti/claim/roles', []),
            'resource_link': launch_data.get('https://purl.imsglobal.org/spec/lti/claim/resource_link', {})
        }
        return render_template("home.html", **tpl_kwargs)
