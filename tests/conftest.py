''' PYTEST CLIENT CONFIGURATION '''

import pytest
from api.app import create_app

#### Define client fixture ####
@pytest.fixture
def client():
    # Instantiate application
    app = create_app()
    app.config["TESTING"] = True
    
    # Yield client for testing
    with app.test_client() as client:
        yield client