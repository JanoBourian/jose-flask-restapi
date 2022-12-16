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
```

## Import information

```python
from flask import Flask
from flask import request
```

## Information

We need to retrieve information in a Json format. 