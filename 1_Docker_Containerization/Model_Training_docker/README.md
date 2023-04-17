# Sample Test to see how we can train the model in docker container 

### 1. Create a Docker File : [Dockerfile](Dockerfile)

```
FROM python:3.9-slim                     # Base image
WORKDIR /opt/src                         # Working directory
COPY requirements.txt requirements.txt   # Copy requirements.txt to working directory
RUN pip3 install -r requirements.txt     # Install the requirements
COPY . .                                 # Copy the current directory to working directory
ENTRYPOINT ["python3", "main.py"]        # Run the main.py file
```

### 2. Build the docker image

```
docker build -t model_training:latest .
```

### 3. Run the docker image

```
docker run --rm -it model_training:latest
```

We can see the model being trained and saved in the docker container

### 4. train.py : [train.py](train.py)

```
Folder where the model training is defined
```

### 5. main.py : [main.py](main.py)

```
Folder where the model training is called and the data is loaded and the neural network is defined
```
