import os
from flask import Flask, render_template, request
from werkzeug.utils import secure_filename


app = Flask(__name__)

VOLUME_PATH = '/data'


@app.route('/')
def ping():
	return 'Hello!'

@app.route('/upload')
def render_upload_page():
	return render_template('upload.html')

@app.route('/upload-file', methods=['POST'])
def upload_file():
	f = request.files['file']
	f.save(os.path.join(VOLUME_PATH, secure_filename(f.filename)))
	return 'File uploaded successfully!'


if __name__ == '__main__':
	app.debug = True
	app.run(host='0.0.0.0')
