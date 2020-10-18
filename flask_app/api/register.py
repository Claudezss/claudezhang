from flask_restx import Api
from .example import api as example_api_ns
from .secret import api as secret_api
from flask import url_for, Flask
import os


def register_apis(app: Flask) -> Flask:

    ENV = os.environ.get("ENV", "")

    if ENV == "production":

        @property
        def specs_url(self):
            return url_for(self.endpoint("specs"), _external=True, _scheme="https")

        Api.specs_url = specs_url

    api = Api(title="Example API Docs", version="1.0", doc="/doc/", ordered=True)

    # add namespace to api
    api.add_namespace(example_api_ns, path="/example")
    api.add_namespace(secret_api, path="/sc")
    api.init_app(app)
    return app
