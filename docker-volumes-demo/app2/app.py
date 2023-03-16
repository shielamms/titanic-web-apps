import os
import flask


app = flask.Flask(__name__)

VOLUME_PATH = '/data'
TEST_FILENAME = 'hello.txt'


@app.route('/')
def read_file():
	contents = None
	with open(os.path.join(VOLUME_PATH, TEST_FILENAME), 'r') as file:
		contents = file.read()
	return contents


if __name__ == '__main__':
	app.debug = True
	app.run(host='0.0.0.0')
