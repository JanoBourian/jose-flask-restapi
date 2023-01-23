from flask import Flask
from flask_smorest import Api

from db import db
import models

from config.config import DEV_CONFIGURATION
from resources.item import blp as ItemBlueprint
from resources.store import blp as StoreBlueprint
from resources.tag import blp as TagBlueprint

def create_app(db_url=None) -> Flask:
    app = Flask(__name__)

    ## Only for test
    if db_url:
        DEV_CONFIGURATION["SQLALCHEMY_DATABASE_URI"] = db_url

    app.config.update(**DEV_CONFIGURATION)
    db.init_app(app)

    api = Api(app)

    @app.before_first_request
    def create_tables():
        db.create_all()

    api.register_blueprint(StoreBlueprint)
    api.register_blueprint(ItemBlueprint)
    api.register_blueprint(TagBlueprint)

    return app
