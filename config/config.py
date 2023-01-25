import os
import secrets 

DEV_CONFIGURATION = {
    "PROPAGATE_EXCEPTIONS": True,
    "API_TITLE": "Stores REST API",
    "API_VERSION": "v1",
    "OPENAPI_VERSION": "3.0.3",
    "OPENAPI_URL_PREFIX": "/",
    "OPENAPI_SWAGGER_UI_PATH": "/docs",
    "OPENAPI_SWAGGER_UI_URL": "https://cdn.jsdelivr.net/npm/swagger-ui-dist/",
    "SQLALCHEMY_DATABASE_URI": os.getenv("DATABASE_URL", "sqlite:///data.db"),
    "SQLALCHEMY_TRACK_ MODIFICATIONS": True,
    "JWT_SECRET_KEY": "295561388835026556267132468178473853209" #secrets.SystemRandom().getrandbits(128)
}
