from flask import Flask, render_template, redirect, url_for, request, flash
from flask_mongoengine import MongoEngine
from werkzeug.utils import secure_filename
import os
import urllib.request

program = Flask(__name__)
program.secret_key = "key"

program.config['MONGODB_SETTINGS'] = {
    'db': 'MyDB',
    'host': 'localhost',
    'port': 27017
}
db = MongoEngine()
db.init_app(program)
UPLOAD_FOLDER = 'static/img'
program.config['UPLOAD_FOLDER'] = UPLOAD_FOLDER
program.config['MAX_CONTENT_LENGTH'] = 16 * 1024 * 1024
   
ALLOWED_EXTENSIONS = set(['txt', 'pdf', 'png', 'jpg', 'jpeg', 'gif'])
   
def allowed_file(filename):
 return '.' in filename and filename.rsplit('.', 1)[1].lower() in ALLOWED_EXTENSIONS

class User(db.Document):
    file_name = db.StringField()
    uploaded_file = db.StringField()

@program.route('/')
def index():
    return render_template('upload.html')


@program.route('/upload', methods=['POST'])
def upload():
    file = request.files['inputFile']
    rs_username = request.form['txtusername']
    filename = secure_filename(file.filename)
   
    if file and allowed_file(file.filename):
       file.save(os.path.join(program.config['UPLOAD_FOLDER'], filename))
       usersave = User(file_name=rs_username, uploaded_file=file.filename)
       usersave.save()
       flash('File successfully uploaded ' + file.filename + ' to the database!')
       return redirect('/')
    else:
       flash('Invalid Uplaod only txt, pdf, png, jpg, jpeg, gif') 
    return redirect('/')    
   
if __name__ == '__main__':
    program.run(debug=True)