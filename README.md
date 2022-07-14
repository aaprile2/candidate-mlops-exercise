# mask_fill 
API to perform Mask Inference against various HuggingFace models. 

There are two versions of the source code in the _api_ directory; the **MAIN branch** is for local builds from source and the **DOCKERIZED branch** is a containerized build. Switch to the **DOCKERIZED** branch to build the Docker image. 

## Running the API 
### Local build from source
Clone the **MAIN** branch. Install dependencies in a virtual environment using either `requirements.txt` or `Pipfile`. Then, run:
```
python main.py
```

**Note:** Make sure you are in the **MAIN** branch. Alteratively, use the **DOCKERIZED** branch but update _main.py_ so that line 12 is commented out; i.e., the host IP address is localhost (default). 


### Local Docker build 
Clone the **DOCKERIZED** branch. Build the image:
```
docker image build -t [name] . 
```

Then, run the application:
```
docker run -rm -it -p 8080:5000 [name]
```

**Note:** Make sure you are in the **DOCKERIZED** branch. Alternatively, use the **MAIN** branch but update _main.py_ so that line 13 is commented out; i.e., the host IP address is unspecified (0.0.0.0). 


### Docker Image (Docker Hub)
Pull the image from Docker Hub:

```
docker pull aaprile22/mask_fill:latest
```

Then, run the application:
```
docker run --rm -it -p 8080:5000 aaprile22/mask_fill:latest
```


## Making Requests
A full demonstration of calls using the Python requests library is provided in _demo_test.ipynb_.


### Hosts
As noted above, hosting the API with a Docker image versus a locally run Python application requires different IP addresses. 

* For the Docker applications, requests should be sent to **http://127.0.0.1:8080/[endpoint]**. Otherwise, there will be a 403 (Forbidden) error.

* For the locally run applications, requests should be sent to **http://127.0.0.1:5000/[endpoint]**. Otherwise, there will be a HTTPConnectionPool (Failed) error.


**Note:** These IP addresses may vary depending on your system. Edit accordingly.


### /inference
**POST:** Performs mask inference with given string against a HuggingFace model. Returns a list of JSON objects containing a probability score, a token string (value to fill in [MASK]), and the original string with [MASK] replaced. Also returns inference time. 

'input' is required, but 'model' defaults to 'bert-base-uncased'. See _api/resources/accepted_models.txt_ or the **/inference/models** endpoint for 'model' values. 
* 'input' only:
```
curl -X POST -d '{"input": "Hello Im a [MASK] model."}' -H 'Content-Type: application/json' http://127.0.0.1:[port]/inference
```

* `input' and `model`:
```
curl -X POST -d '{"input": "Hello Im a [MASK] model.", "model": "roberta-base"}' -H 'Content-Type: application/json' http://127.0.0.1:[port]/inference
```

### /inference/models
**GET:** Lists the HuggingFace inference models (formatted as expected in the POST payload) currently supported by the API, as outlined in _api/resources/accepted_models.txt_. 

```
curl http://127.0.0.1:[port]/inference/models
```


### /healthcheck
**GET:** Basic check to see if API is functioning. Returns a HTTP 200.

```
curl http://127.0.0.1:[port]/healthcheck
```

**HEAD Alternative:**

```
curl -I http://127.0.0.1:[port]/healthcheck
```


### /healthcheck/extracheck
**GET:** Extra check to see if HuggingFace models download page is functioning. Returns a HTTP 200 if healthy and HTTP 404 if unhealthy.

```
curl http://127.0.0.1:[port]/healthcheck/extracheck
```

**HEAD Alternative:**

```
curl -I http://127.0.0.1:[port]/healthcheck/extracheck
```


## Unit Testing
As an extra feature, some unit tests were defined to ensure correct response. This was implemented using Pytest. 

To run the tests, clone either branch repository and navigate to the root of the project directory, then run:

```
python -m pytest
```

You should see the following, indiciating all tests were passed:
**(LOCAL BUILD)**:
![Screen Shot 2022-07-14 at 3 01 57 PM](https://user-images.githubusercontent.com/49654275/179072941-54989803-6da2-4b23-85ee-21ef3277dc3a.png)

**(DOCKER BUILD)**:
![Screen Shot 2022-07-14 at 3 03 48 PM](https://user-images.githubusercontent.com/49654275/179072963-508b8d54-7acb-4ba0-b775-d3b8d140fe6e.png)


## Implementation Notes
* I decided on Flask RESTful mostly because I am familiar with it, and I prefer the object-oriented approach over the standard Flask.
* Some, but not all, cases of incorrect request arguments for **inference** are handled by error codes. 
* In the interest of time, I only made the Dockerfile run the API service, and didn't include the testing.
* Some models (namely 'roberta-large' and 'xlm-roberta-base') caused ConnectionIssues when used with the Dockerized version. I'm not sure why, but I would love to learn about it!

### Extra Features
* **/inference** allows for different models to be used besides 'bert-base-uncased', which is flexible to update in _api/resources/accepted_models.txt_ and _api/resources/inference.py_. 
* **/inference** also returns the inference time, which can be used to compare response time amongst models. This is demonstrated in _demo_test.ipynb_. 
* **/inference** includes input validation, so it will respond with a 500 ValueError if the payload is not valid. Also, some models require `<mask>` instead of `[MASK]` tokens, so that is autocorrected for the user as well depending on their model selection.
* **/healthcheck/extracheck** checks if the HuggingFace model download page (https://huggingface.co/models) is available, because otherwise, the application would be unusable as-is.
* _api_doc.yml_ provides API Documentation in the Swagger format. This should display the documentation for all endpoints, including '/' (the dedicated documentation endpoint), when visiting them in a browser. For some reason, my browser was not rendering this, so it can be viewed in a [Swagger Editor](https://editor.swagger.io/). 
* As seen above, I also dockerized the application and added unit tests (can be viewed in the _test_ directory). 


### Future Improvements
* I would love to hit the other bonus point (creating a pipeline to automatically build and deploy the application to a server). I was reading about it at [this resource](https://docs.docker.com/language/golang/configure-ci-cd/) and would have tried it out given more time. I've never done that from scratch before (only shadowed it), so I will probably try this out soon!
* Because NLP models are constantly being changed and removed, etc., I would think that some **DELETE** and **PUT** methods would be cool to incorporate for the accepted models list.
* The model downloads are tedious, and definitely too heavy/not suitable for production. Instead of using the transformers library, I would include the model architectures and the corresponding Hugging Face weights in, say, a _models_ directory, and run the inference against that. That being said, the previous point about **DELETE** and **PUT** methods would also have to be revised.
* Based on my tests, it seems like only one Mask token is processed even if there are multiple in a sentence (which even sometimes breaks the models). I would love to see if there is anything out there or any changes I could make to the code to handle this situation.
* Because of my issues with viewing my Swagger documentation, I would like to try out Flask RESTPlus, which provides it automatically. 


Thank you!!
