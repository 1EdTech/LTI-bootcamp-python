from flask import jsonify
import os
from flask_caching import Cache
from pylti1p3.contrib.flask import FlaskCacheDataStorage


import json

cache = Cache()

def initialize_cache(app):
    cache.init_app(app)

def get_lti_config_path(app):
    return os.path.join(app.root_path, '..', 'configs', 'registrations.json')

def get_launch_data_storage():
    return FlaskCacheDataStorage(cache)

def load_courses():
    courses_path =  os.path.join(app.root_path, '..', 'configs', 'resources.json')
    with open(courses_path) as f:
        courses = json.load(f)
    return courses

class ReverseProxied:
    def __init__(self, app):
        self.app = app

    def __call__(self, environ, start_response):
        scheme = environ.get('HTTP_X_FORWARDED_PROTO')
        if scheme:
            environ['wsgi.url_scheme'] = scheme
        return self.app(environ, start_response)
