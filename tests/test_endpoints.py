''' PYTEST TEST DEFINITIONS '''
import random

#### Read accepted models from api
with open('api/resources/accepted_models.txt') as f:
    MODELS = [line.strip() for line in f.readlines()]


##############################################
################ INFERENCE ###################
##############################################

#### Test 1: Validating inference input ####
def test_payload(client):
    # Define payload list
    payloads = [
        {'model': 'bert-base-uncased'},    # Expecting 500; 'input' not found in payload
        {'input': "Hello I'm a [MASK] model.", 'model': 'not-a-model'}, # Expecting 500; not a valid 'model'
        {'input': "Hello I'm a model.", 'model': 'bert-base-uncased'}, # Expecting 500; 'input' must contain [MASK] or <mask> token
        {'input': "Hello I'm a [MASK] model.", 'model': 'bert-base-uncased'}, # Expecting 201; valid payload
        {'input': "Hello I'm a <mask> model.", 'model': 'bert-base-uncased'}, # Expecting 201; valid payload (<mask> converted to [MASK])
        {'input': "Hello I'm a <mask> model.", 'model': 'roberta-base'}, # Expecting 201; valid payload
        {'input': "Hello I'm a [MASK] model.", 'model': 'roberta-base'}, # Expecting 201; valid payload ([MASK] converted to <mask>)
        {'input': "Hello I'm a [MASK] model."} # Expecting 201; defaults to 'bert-base-uncased'
    ]

    # Define expected status codes
    true_status = [500, 500, 500, 201, 201, 201, 201]

    # Run tests
    for p, s in list(zip(payloads, true_status)):
        # POST request
        res = client.post('inference', json = p)

        # Assert truth
        assert res.status_code == s


#### Test 2: Checking inference model availability ####
def test_models(client):
    # Define universal payload object
    payload = {'input': "Hello I'm a [MASK] model."}

    # Run tests
    for m in MODELS:
        # Update payload
        payload['model'] = m

        # Post request
        res = client.post('inference', json = payload)

        # Assert truth
        assert res.status_code == 201
        assert 'data' in res.json.keys() and 'inference_time' in res.json.keys()


#### Test 3: Check other random strings for inference output ####
def test_input(client): 
    # Define 'random' input
    rand_input = ['[MASK] are my favorite animals!', 'Did you see <mask> at the store?', 'This is a very long string. It is being tested to see what the [MASK] should be. Hopefully it works!']

    # Define 'random' models
    rand_models = random.sample(MODELS, len(rand_input))

    # Run tests
    for i, m in list(zip(rand_input, rand_models)):
        # Define payload object
        payload = {'input': i, 'model': m}

        # POST request
        res = client.post('inference', json = payload)

        # Assert truth
        assert res.status_code == 201
        assert 'data' in res.json.keys() and 'inference_time' in res.json.keys()



##############################################
################ HEALTHCHECK #################
##############################################

#### Test 1: Validating healthcheck output ####
def test_healthcheck(client):
    # GET request
    get_res = client.get('healthcheck')
    assert get_res.status_code == 200

    # HEAD request
    head_res = client.get('healthcheck')
    assert head_res.status_code == 200


#### Test 2: Validating healthcheck/extracheck output ####
def test_extracheck(client):
    # GET request
    get_res = client.get('healthcheck/extracheck')
    assert get_res.status_code in [200, 404]

    # HEAD request
    head_res = client.get('healtcheck/extracheck')
    assert head_res.status_code in [200, 404]