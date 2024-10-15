
from flask import Flask

from .views import blue
from App.exts import *


def create_app():
    app = Flask(__name__)
    cors.init_app(app, resources={r'/*': {'origins': '*'}})
    app.register_blueprint(blue)

    db_uri = 'mysql+pymysql://root:123456@localhost:3306/bigdemo'
    app.config['SQLALCHEMY_DATABASE_URI'] = db_uri
    app.config['SQLALCHEMY_TRACK_MODIFICATIONS'] = False

    init_ext(app)


    return app