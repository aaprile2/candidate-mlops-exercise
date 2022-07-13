''' ENTRYPOINT FOR RUNNING API '''

from api.app import create_app


#### Create and run application
if __name__ == '__main__':
    # Instantiate application
    app = create_app()

    # Run application
    #app.run(host='0.0.0.0', debug=True) # -> USE THIS TO TEST DOCKER IMAGE
    app.run(debug=True) # -> USE THIS TO TEST LOCAL APPLICATION/PYTEST