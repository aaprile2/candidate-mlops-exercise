''' HEALTHCHECK RESOURCES '''

from flask import request, abort, Response
from flask_restful import Resource
import requests
from flasgger import Swagger, swag_from


#### HealthCheck Resource for checking the health
#### - Returns HTTP 200
class HealthCheck(Resource):
    ''' GET (HEAD) request for health check '''
    @swag_from('api/api_doc.yml')
    def get(self):
        return 'HEALTHY', 200

#### Extra HealthCheck Resource for checking the health
#### of the 'transformers' model download page
#### - Returns HTTP 200 if up and running, HTTP 404 otherwise
class ExtraCheck(Resource):
    ''' GET (HEAD) request for Additional HealthCheck for https://huggingface.co/models status '''
    @swag_from('api/api_doc.yml')
    def get(self):
        # Check URL
        resp = requests.head('https://huggingface.co/models')

        # Return health
        if resp.status_code in [200, 201, 202]:
            return 'HEALTHY', 200
        else:
            return 'UNHEALTHY', 404