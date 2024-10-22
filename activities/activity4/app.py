from flask import Flask

from flask_session import Session
from utils import ReverseProxied, initialize_cache
from modules.lti import register as register_lti
from modules.home import register as register_home
from modules.nrps import register as register_nrps
from modules.dl import register as register_dl
from modules.ags import register as register_ags

app = Flask(__name__)
app.wsgi_app = ReverseProxied(app.wsgi_app)

app.config.from_object('config.Config')
initialize_cache(app)

Session(app)

register_home(app)
register_lti(app)
register_nrps(app)
register_dl(app)
register_ags(app)

if __name__ == "__main__":
    app.run(host='0.0.0.0', port=3000, debug=True)
