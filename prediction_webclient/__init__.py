from flask import Flask
from . import data_lookup
from . import config
app = Flask(__name__, static_url_path='', static_folder='static', template_folder='templates')

# import all routes
from .routes import *

def run():
    conf = config.get()
    app.run(debug=True, host=conf.get('host', '0.0.0.0'), port=conf.get('port', 80))