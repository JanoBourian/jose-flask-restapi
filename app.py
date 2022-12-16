from flask import Flask, request, make_response, Response
from db import stores, items
import uuid 
app = Flask(__name__)


# stores = [{"name": "My Store", "items": [{"name": "Chair", "price": 15.99}]}]

@app.get("/store")
def get_stores() -> dict:
    return {"stores": list(stores.values())}


@app.post("/store")
def create_store() -> Response:
    store_data = request.get_json()
    store_id = uuid.uuid4().hex
    store = {**store_data, "id": store_id}
    stores[store_id] = store
    response = make_response(store, 201)
    return response

@app.get("/store/<string:store_id>")
def get_specific_store(store_id:str):
    try:
        return stores[store_id]
    except KeyError:
        return make_response({"message": "Store not found"}, 404)

@app.post("/item")
def create_items(store_name: str) -> Response:
    item_data = request.get_json()
    if item_data["store_id"] not in stores:
        return make_response({"message": "Store was not found"}, 404)
    item_id = uuid.uuid4().hex
    item = {**item_data, "id":item_id}
    items[item_id] = item
    response = make_response(item, 201)
    return response

@app.get("/item")
def get_all_items() -> dict:
    return {"items": list(items.values())}

@app.get("/item/<string:item_id>")
def get_specific_item(item_id: str) -> Response:
    try:
        return items[item_id]
    except KeyError:
        return make_response({"message": "Item was not found"}, 404)
