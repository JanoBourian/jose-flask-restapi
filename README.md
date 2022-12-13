# jose-flask-restapi
This REST API is based on Jose Salvatierra Crash Course (with my adaptations) and made with Flask RestFull

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
```

## Import information

```python
from flask import Flask
from flask import request
```

## Information

We need to retrieve information in a Json format. 