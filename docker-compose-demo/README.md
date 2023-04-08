# Docker networks in docker-compose demo app

This is a sample app is composed of a simple Flask API and a redis instance,
deployed onto docker containers managed by docker-compose.

This folder contains the code for the article on [Half-Stack Full](http://dev.shielasandoval.com/containerisation/guide-to-docker-compose.html) 
demonstrating the use of docker-compose to allow communication between containers
by automatically spinning up a single docker network.

## Python environment

This app was tested on Python 3.10.10. See `requirements.txt` for full list
of python library versions used.


### Run through docker-compose

```
docker build -t my-app .
docker pull redis

docker-compose up
```
