''' INFERENCE RESOURCE '''

from flask import request, abort, Response
from flask_restful import Resource
import json
import time
from transformers import pipeline

#### Accepted models
with open('api/resources/accepted_models.txt') as f:
    MODELS = [line.strip() for line in f.readlines()]

#### Fill-Mask resource for loading model and filling the mask
#### the mask in the given sentence
class FillMask(Resource):
    ''' Initialization; validate input '''
    def __init__(self):
        # Get form data
        data = request.get_json()

        ''' Unpack and check arguments '''
        if 'input' not in data.keys():
            abort(500, 'ValueError: input string is required.')
        
        # Unpack values
        self.input = str(data['input']) # Typecast to string for safety

        # Get model
        if 'model' in data.keys():
            # Unpack value
            temp = data['model']

            if temp in MODELS:
                self.model = temp
            else:
                abort(500, 'ValueError: model is not accepted. Please select from the following: {}.'.format(MODELS))
        else:
            self.model = 'bert-base-uncased' # Default model if not specified

        # Check for corresponding MASK token
        if '[MASK]' not in self.input and '<mask>' not in self.input:
            abort(500, 'ValueError: input must contain [MASK] or <mask> tokens.')
        else:
            if self.model in ['bert-base-uncased', 'distilbert-base-uncased']:
                if '[MASK]' not in self.input:
                    if '<mask>' in self.input:
                        self.input = self.input.replace('<mask>', '[MASK]')
                    else: # Not necessary to include due to parent 'if' condition, but fail-safe
                        abort(500, 'ValueError: input must contain [MASK] (preferred for {}) or <mask> token.'.format(self.model))

            elif self.model in ['roberta-base', 'roberta-large', 'xlm-roberta-base']:
                if '<mask>' not in self.input:
                    if '[MASK]' in self.input:
                        self.input = self.input.replace('[MASK]', '<mask>')
                    else: # Not necessary to include due to parent 'if' condition, but fail-safe
                        abort(500, 'ValueError: input must contain [MASK] or <mask> (preferred for {}) token.'.format(self.model))
        

    ''' POST request for filling the mask '''
    def post(self):
        #  Load model into pipeline
        unmasker = pipeline('fill-mask', model = self.model)

        # Start timer
        start = time.time()

        # Get output
        output = unmasker(self.input)

        # End timer
        end = time.time()

        # Return output
        return {'data': output, 'inference_time': round(end - start, 5)}, 201

