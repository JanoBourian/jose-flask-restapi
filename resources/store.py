import uuid
from flask import request, make_response
from flask.views import MethodView
from flask_smorest import Blueprint, abort
from schemas import StoreSchema
from models.stores import StoreModel
from db import db
from sqlalchemy.exc import SQLAlchemyError, IntegrityError

blp = Blueprint("Stores", __name__, description="Operations on stores")


@blp.route("/store/<string:store_id>")
class Store(MethodView):
    @blp.response(200, StoreSchema)
    def get(self, store_id: str):
        return StoreModel.query.get_or_404(store_id)

    def delete(self, store_id: str):
        store = StoreModel.query.get_or_404(store_id)
        db.session.delete(store)
        db.session.commit()
        return make_response({"message": f"Store {store_id} was deleted"}, 201)


@blp.route("/store")
class StoreList(MethodView):
    @blp.response(200, StoreSchema(many=True))
    def get(self):
        return StoreModel.query.all()

    @blp.arguments(StoreSchema)
    @blp.response(201, StoreSchema)
    def post(self, store_data):
        store = StoreModel(**store_data)

        try:
            db.session.add(store)
            db.session.commit()
        except IntegrityError as e:
            print(f"ERROR: {e}")
            abort(400, message="A store with that name already exists")
        except SQLAlchemyError as e:
            print(f"ERROR: {e}")
            abort(500, message="An erro ocurred creating the store")

        return store
