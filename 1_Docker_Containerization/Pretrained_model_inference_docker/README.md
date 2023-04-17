# Pretrained model inference using docker containers
## 1. Introduction

-   Create Dockerfile that uses https://github.com/rwightman/pytorch-image-models Links to an external site and build an image.
-   Create an Inference Python Script that takes a model name and image path/url and outputs json like {"predicted": "dog", "confidence": "0.89"}
-   MODEL and IMAGE must be configurable while inferencing
-   Model Inference will be done like: docker run $IMAGE_NAME --model $MODEL --image $IMAGE
-   Try to bring the docker image size as less as possible (maybe try out slim/alpine images?) (use architecture and linux specific -   CPU wheel from here  https://download.pytorch.org/whl/torch_stable.htmlLinks to an external site.)
-   Pull from DockerHub and run on Play With Docker to verify yourself
-   Tests for github classroom can be run with   bash ./tests/all_tests.sh

## 2. Dockerfile 

-   The dockerfile is in Dockerfile [Dockerfile](Dockerfile)
-   Goal is to reduce the size of the docker image as much as possible 
-   Dockerfile uses multi-stage build to reduce the size of the image 

```
FROM python:3.9-slim-buster as compile-image

RUN apt-get update -y && apt install -y --no-install-recommends git\
    && pip install --no-cache-dir -U pip

COPY requirements.txt .

RUN pip install --user --no-cache-dir https://download.pytorch.org/whl/cpu/torch-1.11.0%2Bcpu-cp39-cp39-linux_x86_64.whl \
    && pip install --user --no-cache-dir https://download.pytorch.org/whl/cpu/torchvision-0.12.0%2Bcpu-cp39-cp39-linux_x86_64.whl \
    && pip install --user --no-cache-dir -r requirements.txt && rm -rf /root/.cache/pip

FROM python:3.9-slim-buster as runtime-image
COPY --from=compile-image /root/.local /root/.local
WORKDIR /src
COPY . .
ENTRYPOINT ["python3", "app.py"]
```

## 3. Inference Python Script

-   The inference script is in app.py [app.py](app.py)
-  The script takes 2 arguments: model and image
-  The script outputs a json file with the predicted class and confidence
-  The script uses timm library to load the model and predict the class
-  The script uses requests library to download the image from the url

## 4. Docker Image Size
-  The docker image size is 885MB
-  This is achieved cause of using slim image of python along with multi-stage build.
-  rm -rf /root/.cache/pip is used to remove the cache of pip to reduce the size of the image 

## 5. How to run the docker image 
-   Build the docker image using the command: 
```
docker build -t pretrained_tim:v1 .
```
-   Run the docker image using the command: 
```
docker run pretrained_timm:v1 model=resnet18 filename=https://www.pngall.com/wp-content/uploads/4/Golden-Retriever-PNG-Transparent-HD-Photo.png
```
-   The output is: 
```
{'prediction': 'golden retriever', 'confidence': '0.96'}
```

## 6. Tests 
-  The tests are in tests folder [tests](tests)
-  The tests are run using bash ./tests/all_tests.sh [all_tests.sh](tests/all_tests.sh), ./tests/bonus_test.sh [bonus_test.sh](tests/bonus_test.sh) (Works only on Linux/MacOS)

## Reference: 
https://huggingface.co/docs/timm/models/resnet
https://github.com/facebookresearch/hydra
https://pythonspeed.com/articles/multi-stage-docker-python/
https://www.cynnovative.com/simple-multi-stage-docker-builds/
