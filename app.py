from flask import Flask, request, make_response, Response
from db import stores, items
from flask_smorest import abort
import uuid

app = Flask(__name__)

## Store
@app.get("/store")
def get_stores() -> dict:
    return {"stores": list(stores.values())}


@app.post("/store")
def create_store() -> Response:
    store_data = request.get_json()

    # Validation
    if "name" not in store_data:
        return abort(404, message="Store name is required")
    for store in stores.values():
        if store_data["name"] == store["name"]:
            abort(404, message="Store already exists")
    store_id = uuid.uuid4().hex
    store = {**store_data, "id": store_id}
    stores[store_id] = store
    response = make_response(store, 201)
    return response


@app.get("/store/<string:store_id>")
def get_specific_store(store_id: str):
    try:
        return stores[store_id]
    except KeyError:
        return abort(404, message="Store not found")


@app.put("/store/<string:store_id>")
def update_specific_store(store_id: str):
    store_data = request.get_json()
    if "name" not in store_data:
        return abort(404, message="Store's name is required")
    try:
        store = stores[store_id]
        store |= store_data
        return make_response(store, 201)
    except KeyError:
        return abort(404, message="Store not exists")


@app.delete("/store/<string:store_id>")
def delete_specific_store(store_id: str):
    try:
        del stores[store_id]
        return make_response({"message": "Store was deleted correctly"}, 201)
    except KeyError:
        return abort(
            404, message="This Store can not be deleted because does not exist"
        )


## Item
@app.get("/item")
def get_all_items() -> dict:
    return {"items": list(items.values())}


@app.post("/item")
def create_items() -> Response:
    item_data = request.get_json()

    # Validation
    if (
        "store_id" not in item_data
        or "name" not in item_data
        or "price" not in item_data
    ):
        return abort(400, "Some argument is empty.")
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
    response = make_response(item, 201)
    return response


@app.get("/item/<string:item_id>")
def get_specific_item(item_id: str) -> Response:
    try:
        return items[item_id]
    except KeyError:
        return abort(404, message="Item was not found")


@app.put("/item/<string:item_id>")
def update_specific_item(item_id: str):
    item_data = request.get_json()
    if "price" not in item_data or "name" not in item_data:
        return abort(404, message="You need to put all information")
    try:
        item = items[item_id]
        item |= item_data
        return make_response(item, 201)
    except KeyError:
        return abort(404, message="Item not found!")


@app.delete("/item/<string:item_id>")
def delet_specific_item(item_id: str):
    try:
        del items[item_id]
        return make_response({"message": "Item was deleted"}, 201)
    except KeyError:
        return abort(404, message="Item was not found")
