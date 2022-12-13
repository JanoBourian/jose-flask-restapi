from flask import Flask, request, make_response, Response

app = Flask(__name__)


stores = [{"name": "My Store", "items": [{"name": "Chair", "price": 15.99}]}]


@app.get("/store")
def get_stores() -> dict:
    return {"stores": stores}


@app.post("/store")
def create_store() -> Response:
    data = request.get_json()
    new_store = {"name": data.get("name", ""), "items": []}
    stores.append(new_store)
    response = make_response(new_store, 201)
    return response


@app.get("/store/<string:store_name>/item")
def get_items(store_name: str) -> Response:
    response = make_response({"message": "Store was not found"}, 404)
    for store in stores:
        print(store)
        if store.get("name", "") == store_name:
            response = make_response(store, 200)
    return response


@app.post("/store/<string:store_name>/item")
def create_items(store_name: str) -> Response:
    print(request.args)
    request_data = request.get_json()
    response = make_response({"message": "Store was not found"}, 404)
    for store in stores:
        if store.get("name", "") == store_name:
            new_item = {
                "name": request_data.get("name", ""),
                "price": request_data.get("price", ""),
            }
            store["items"].append(new_item)
            response = make_response(new_item, 201)
    return response
