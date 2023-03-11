import flask
import os
import redis


app = flask.Flask(__name__)

host = os.getenv('REDIS_HOST', 'redis')
client = redis.Redis(host=host, port=6379)


@app.route('/')
def ping():
	return 'Hello!'

@app.route('/cache/<key>/<data>')
def add_data(key, data):
	client.set(key, data)
	return f'Data added into {key}'

@app.route('/retrieve/<key>')
def get_data(key):
	result = client.get(key)
	return result


if __name__ == '__main__':
	app.debug = True
	app.run(host='0.0.0.0')
