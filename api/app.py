''' DEFINE APP '''

from flask import Flask
from flask_restful import Api
from flasgger import Swagger, swag_from
from api.resources.inference import FillMask, GetModels
from api.resources.healthcheck import HealthCheck, ExtraCheck
from api.resources.docs import Docs


# Application factory
def create_app():
    # Instantiate Flask
    app = Flask(__name__)
    api = Api(app)
    
    # Map SWAGGER
    app.config['SWAGGER'] = {'title': 'Mask Inference'}

    swag = Swagger(app)

    # Attach Resource classes to endpoints
    api.add_resource(Docs, '/')
    api.add_resource(FillMask, '/inference')
    api.add_resource(GetModels, '/inference/models')
    api.add_resource(HealthCheck, '/healthcheck')
    api.add_resource(ExtraCheck, '/healthcheck/extracheck')

    return app