# jose-flask-restapi
This REST API is based on Jose Salvatierra Crash Course (with my adaptations) and made with Flask RestFull

## About Docker

### Creation 

```Docker
COPY source dest
COPY hello.txt /absolute/path
COPY hello.txt relative/to/work
```

```Docker
FROM python:3.11
ENV FLASK_APP main.py
EXPOSE 5000
WORKDIR /code
COPY . .
RUN pip install --no-cache-dir --upgrade -r /code/requirements.txt
CMD ["flask", "run", "--host", "0.0.0.0"]
```

### Run

```cmd
docker build -t rest-api-flask-python .
docker run -d -p 5000:5000 rest-api-flask-python
```


## Previous 

```cmd
python -m venv jose-flask-env
pip freeze > requirements.txt
set FLASK_APP=app.py
set FLASK_DEBUG=1
flask run --host 0.0.0.0

```

## Packages
```cmd
pip install flask
pip install black
pip install flask-smorest
pip install python-dotenv
pip install flask-sqlalchemy
```

## Import information

```python
from flask import Flask
from flask import request
```

## Information

We need to retrieve information in a Json format. 

## About python-dotenv and .flaskenv

With this file we can start the server fastest, cause inside the __.flaskenv__ file are all information about the previous steps like "set"

## About flask-smorest

Is for data model, using UUID. Flask smorest help us to the response, is similar to make_response but it has a little because with flask-smorest and flask-marshmallow we can create documentation with OpenAPI, and it is so interesting for our development as programmer. 

```python
abort
```

## Blueprint

Is a way to divide an API into multiple segments.

## MethodViews

It can be used to implement the HTTP methods inside a class and create a documentation

## Marshmallow

We can use marshmallow for create validations (something like pydantic)

## Flask-smorest decorating process

We can use it for decorating our responses

## Flask SQLAlchemy

Example model:

```python
from db import db

class ItemModel(db.Model):
    __tablename__ = "items"
    
    id = db.Column(db.Integer, primary_key=True)
    name = db.Column(db.String(80), unique=False, nullable=False)
    price = db.Column(db.Float(precision=2), nullable=False, unique=False)
    store_id = db.Column(db.Integer, unique=False, nullable=False)
```

### One-to-many relationship

```python
from db import db

class ItemModel(db.Model):
    __tablename__ = "items"
    
    id = db.Column(db.Integer, primary_key=True)
    name = db.Column(db.String(80), unique=False, nullable=False)
    price = db.Column(db.Float(precision=2), nullable=False, unique=False)
    store_id = db.Column(db.Integer, db.ForeignKey("stores.id"), unique=False, nullable=False)
    store = db.relationship("StoreModel", back_populates="items")

class StoreModel(db.Model):
    __tablename__ = "stores"
    
    id = db.Column(db.Integer, primary_key=True)
    name = db.Column(db.String(80), unique=True, nullable=False)
    items = db.relationship("ItemModel", back_populates="store", lazy="dynamic")
```

And is too much important pay atention in the new schema structure

```python
from marshmallow import Schema, fields

class PlainItemSchema(Schema):
    id = fields.Str(dump_only=True)
    name = fields.Str(required=True)
    price = fields.Float(required=True)


class PlainStoreSchema(Schema):
    id = fields.Str(dump_only=True)
    name = fields.Str(required=True)


class ItemUpdateSchema(Schema):
    name = fields.Str()
    price = fields.Float()


class ItemSchema(PlainItemSchema):
    store_id = fields.Int(required=True, load_only=True)
    store = fields.Nested(PlainStoreSchema(), dump_only=True)
    

class StoreSchema(PlainStoreSchema):
    items = fields.List(fields.Nested(PlainItemSchema(), dump_only=True))

```

### Many-to-many relationship