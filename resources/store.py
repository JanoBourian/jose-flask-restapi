import uuid
from flask import request, make_response
from flask.views import MethodView
from flask_smorest import Blueprint, abort
from db import stores
from schemas import StoreSchema

blp = Blueprint("Stores", __name__, description="Operations on stores")


@blp.route("/store/<string:store_id>")
class Store(MethodView):
    @blp.response(200, StoreSchema)
    def get(self, store_id: str):
        try:
            return stores[store_id]
        except KeyError:
            return abort(404, message="Store not found")

    def put(self, store_id: str):
        store_data = request.get_json()
        if "name" not in store_data:
            return abort(404, message="Store's name is required")
        try:
            store = stores[store_id]
            store |= store_data
            return make_response(store, 201)
        except KeyError:
            return abort(404, message="Store not exists")

    def delete(self, store_id: str):
        try:
            del stores[store_id]
            return make_response({"message": "Store was deleted correctly"}, 201)
        except KeyError:
            return abort(
                404, message="This Store can not be deleted because does not exist"
            )


@blp.route("/store")
class StoreList(MethodView):
    @blp.response(200, StoreSchema(many=True))
    def get(self):
        return stores.values()

    @blp.arguments(StoreSchema)
    @blp.response(201, StoreSchema)
    def post(self, store_data):
        for store in stores.values():
            if store_data["name"] == store["name"]:
                abort(404, message="Store already exists")
        store_id = uuid.uuid4().hex
        store = {**store_data, "id": store_id}
        stores[store_id] = store
        return store
