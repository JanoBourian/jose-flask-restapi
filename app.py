from flask import Flask, make_response
from flask_smorest import Api
from flask_jwt_extended import JWTManager

from db import db
from blocklist import BLOCKLIST
import models

from config.config import DEV_CONFIGURATION
from resources.item import blp as ItemBlueprint
from resources.store import blp as StoreBlueprint
from resources.tag import blp as TagBlueprint
from resources.user import blp as UserBlueprint

def create_app(db_url=None) -> Flask:
    app = Flask(__name__)

    ## Only for test
    if db_url:
        DEV_CONFIGURATION["SQLALCHEMY_DATABASE_URI"] = db_url

    app.config.update(**DEV_CONFIGURATION)
    db.init_app(app)

    api = Api(app)
    jwt = JWTManager(app)
    
    ## Additional functions
    @jwt.token_in_blocklist_loader
    def check_if_token_in_blocklist(jwt_header, jwt_payload):
        # BLOCKLIST can be some information in a database
        return jwt_payload["jti"] in BLOCKLIST
    
    @jwt.additional_claims_loader
    def add_claims_to_jwt(identity):
        # Look in the databse and see whether the user is an admin
        if identity == 1:
            return {"is_admin": True}
        return {"is_admin": False}
    
    ## Error messages
    @jwt.needs_fresh_token_loader
    def token_not_fresh_callback(jwt_header, jwt_payload):
        return make_response(
            {"description":"The token is not fresh", "error": "fresh_token_required"},
            401
        )
    
    @jwt.revoked_token_loader
    def revoked_token_callback(jwt_header, jwt_payload):
        return make_response(
            {"description":"The token has been revoked", "error": "token_revoked"},
            401
        )
    
    @jwt.expired_token_loader
    def expired_token_callback(jwt_header, jwt_payload):
        return make_response(
            {"message":"The token has expired", "error": "token_expired"},
            401
        )
    
    @jwt.invalid_token_loader
    def invalid_token_callback(error):
        return make_response(
            {"message":"Signature verification failed", "error": "invalid_token"},
            401
        )
        
    @jwt.unauthorized_loader
    def missing_token_callback(error):
        return make_response(
            {"description":"Request does not contain an access token", "error": "authorization_required"},
            401
        )
    

    @app.before_first_request
    def create_tables():
        db.create_all()

    api.register_blueprint(StoreBlueprint)
    api.register_blueprint(ItemBlueprint)
    api.register_blueprint(TagBlueprint)
    api.register_blueprint(UserBlueprint)

    return app
