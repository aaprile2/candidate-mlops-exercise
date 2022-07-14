''' DOCS RESOURCES '''

from flask import request, abort, Response
from flask_restful import Resource
from flasgger import Swagger, swag_from


#### API Docs Resource
class Docs(Resource):
    ''' Stand-In GET request '''
    @swag_from('api/api_doc.yml')
    def get(self):
        return '', 200