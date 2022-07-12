''' HEALTHCHECK RESOURCE '''

from flask import request, abort, Response
from flask_restful import Resource
import json


#### Fill-Mask resource for loading model and filling the mask
#### the mask in the given sentence
class HealthCheck(Resource):
    ''' GET request for health check '''
    def get(self):
        return '', 200
    def head(self):
        return 'blah', 200
        return 'blah', 404