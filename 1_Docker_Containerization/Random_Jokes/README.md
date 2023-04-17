# Steps to run this app

## Jokes API used in this app is from 

```bash 
https://v2.jokeapi.dev/joke/
```

## Clone

```bash
git clone https://github.com/seepala98/MLOps.git
cd MLops/1_Docker_Containerization/Random_Jokes
```

## Build the container image

```bash
docker build --tag randomjokes:latest .
```

## Run the container image on port 80

```bash
docker run -p 80:5000 randomjokes:latest
```

## Open the app in browser

```bash
http://localhost
```
Refresh the page to get a new joke

<img src="img\Webpage_jokes.png" width=50% height=50%>

## Stop the container

```bash
docker stop <container_id>
```

## Remove the container

```bash
docker rm <container_id>
```

## Remove the image

```bash
docker rmi <image_id>
```

## Push the image to Docker Hub

```bash
docker login
docker tag <image_id> <docker_hub_username>/randomjokes:latest
docker push <docker_hub_username>/randomjokes:latest
```