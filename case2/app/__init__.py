from flask import Flask
from bson.json_util import dumps


app = Flask(__name__, instance_relative_config=True)
app.config.from_object('config')
app.config.from_pyfile('config.py')




from .api.routes import mod as apiMod

app.register_blueprint(apiMod, url_prefix='/api/v1.0')

@app.route('/')
def index():
    return dumps("Python Successfully Running")