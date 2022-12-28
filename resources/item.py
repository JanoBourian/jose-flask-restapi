import uuid
from flask import request, make_response
from flask.views import MethodView
from flask_smorest import Blueprint, abort
from db import stores, items
from schemas import ItemSchema, ItemUpdateSchema

blp = Blueprint("Items", __name__, description="Operations on items")


@blp.route("/item/<string:item_id>")
class Item(MethodView):
    @blp.response(200, ItemSchema)
    def get(self, item_id):
        try:
            return items[item_id]
        except KeyError:
            return abort(404, message="Item was not found")

    @blp.arguments(ItemUpdateSchema)
    @blp.response(201, ItemSchema)
    def put(self, item_data, item_id):
        try:
            item = items[item_id]
            item |= item_data
            return item
        except KeyError:
            return abort(404, message="Item not found!")

    def delete(self, item_id):
        try:
            del items[item_id]
            return make_response({"message": "Item was deleted"}, 201)
        except KeyError:
            return abort(404, message="Item was not found")


@blp.route("/item")
class ItemList(MethodView):
    @blp.response(200, ItemSchema(many=True))
    def get(self):
        return items.values()

    @blp.arguments(ItemSchema)
    @blp.response(201, ItemSchema)
    def post(self, item_data):
        for item in items.values():
            if (
                item_data["name"] == item["name"]
                and item_data["store_id"] == item["store_id"]
            ):
                return abort(404, message="Item already exists!")
        if item_data["store_id"] not in stores:
            return abort(404, message="Store not found")

        item_id = uuid.uuid4().hex
        item = {**item_data, "id": item_id}
        items[item_id] = item
        return item
