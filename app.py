from flask import Flask
from flask_smorest import Api
from config.config import DEV_CONFIGURATION
from resources.item import blp as ItemBlueprint
from resources.store import blp as StoreBlueprint

app = Flask(__name__)
app.config.update(**DEV_CONFIGURATION)

api = Api(app)
api.register_blueprint(StoreBlueprint)
api.register_blueprint(ItemBlueprint)
