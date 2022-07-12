''' DEFINE APP '''

from flask import Flask
from flask_restful import Api
from api.resources.inference import FillMask
from api.resources.healthcheck import HealthCheck


# Application factory
def create_app():
# Instantiate Flask
    app = Flask(__name__)
    api = Api(app)

    # Attach Resource classes to endpoints
    api.add_resource(FillMask, '/inference')
    api.add_resource(HealthCheck, '/healthcheck')

    return app