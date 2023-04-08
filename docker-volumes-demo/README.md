# A sample multi-container setup with docker-compose

This is a demo of two Flask apps that share share ephemeral data using Docker Volumes, deployed and managed by docker-compose.

This folder contains the code for the article on [Half-Stack Full](http://dev.shielasandoval.com/containerisation/guide-to-docker-volumes.html) 
demonstrating the use of docker-compose to allow multiple docker containers to share files by mounting a docker volume.

## Python environment

This app was tested on Python 3.10.10. See `requirements.txt` for full list
of python library versions used.

### Run option 1: Native installation

Install python through `pyenv`:

```
pyenv install 3.10.10
pyenv local 3.10.10

``` 

Then set up a virtual environment:

```
virtualenv venv
source venv/bin/activate
pip install -r requirements.txt
```

Run the two apps individually:
```
python app1/app.py
python app2/app.py
```


### Run through docker-compose

```
docker build -t dv-app ./app1
docker build -t dv-app2 ./app2

docker-compose up
```
