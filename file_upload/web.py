from flask import Flask
from flask import render_template
from flask import request
from flask import redirect
from flask import url_for
from flask import flash
from flask import send_from_directory
import os
from uuid import uuid4
from werkzeug.utils import secure_filename
from flask_bootstrap import Bootstrap


UPLOAD_FOLDER = '/tmp/'
ALLOWED_EXTENSIONS = set(['txt', 'pdf', 'png', 'jpg', 'jpeg', 'gif'])


def create_app():
    app = Flask(__name__)
    Bootstrap(app)

    return app


app = create_app()
app.config['UPLOAD_FOLDER'] = UPLOAD_FOLDER
app.config['SESSION_TYPE'] = 'memcached'
app.config['SECRET_KEY'] = str(uuid4())


@app.route('/', methods=['POST', 'GET'])
def hello_world():
    if request.method == 'GET':
        return render_template('index_new.html')
    if request.method == 'POST':
        if 'file' not in request.files:
            flash('No file part')
            #return redirect(request.url)

        data_file = request.files['file']

        # if user does not select file, browser also
        # submit a empty part without filename
        if data_file.filename == '':
            flash('No selected file')
            #return redirect(request.url)

        if data_file:
            filename = secure_filename(data_file.filename)
            data_file.save(os.path.join(app.config['UPLOAD_FOLDER'], filename))
            return redirect(request.url)
            #return redirect(url_for('uploaded_file', filename=filename))


@app.route('/uploads/<filename>')
def uploaded_file(filename):
    return send_from_directory(app.config['UPLOAD_FOLDER'],
                               filename)


if __name__ == "__main__":
    app.run(host='0.0.0.0', port=8000, debug=True)
