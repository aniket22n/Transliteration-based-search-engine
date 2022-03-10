from flask import Flask, render_template, redirect, url_for, request, flash
#from flask_mongoengine import MongoEngine
from werkzeug.utils import secure_filename
import os
#import urllib.request

program = Flask(__name__)  #program is a variable that contains a website and load in memory 
program.secret_key = "key" #If app.secret_key isn't set, Flask will not allow you to set or access the session dictionary.

# program.config['MONGODB_SETTINGS'] = {
#     'db': 'MyDB',
#     'host': 'localhost',
#     'port': 27017
# }
# db = MongoEngine()
# db.init_app(program)

UPLOAD_FOLDER = 'static/saved_files' #The file will be stored here 
program.config['UPLOAD_FOLDER'] = UPLOAD_FOLDER 
program.config['MAX_CONTENT_LENGTH'] = 16 * 1024 * 1024 #maximum size a file can have i.e. 16 MB
   
ALLOWED_EXTENSIONS = set(['txt', 'pdf', 'png', 'jpg', 'jpeg', 'gif'])  # These are allowed extensions 
   
def allowed_file(filename):  # This function is used to check file extenstion 
 return '.' in filename and filename.rsplit('.', 1)[1].lower() in ALLOWED_EXTENSIONS

# class User(db.Document):
#     file_name = db.StringField()
#     uploaded_file = db.StringField()

@program.route('/') #main page http://127.0.0.1:5000/
def index():
    return render_template('upload.html')


@program.route('/upload', methods=['POST']) #upload page
def upload():
    file = request.files['inputFile']
    #rs_username = request.form['txtusername']
    filename = secure_filename(file.filename) #secure_filename to make sure data can't be forged
   
    if file and allowed_file(file.filename): #file shouldn't empty and shoudn't be any other extension 
       file.save(os.path.join(program.config['UPLOAD_FOLDER'], filename))  #save() method to save file on location 
       #usersave = User(file_name=rs_username, uploaded_file=file.filename) #calling user class
       #usersave.save() #to save file name in db
       flash('File successfully uploaded ' + file.filename + ' to the database!') # flash message  
       return redirect('/') # redirect of main page
    else:
       flash('Invalid Uplaod only txt, pdf, png, jpg, jpeg, gif') #flash message,if condition not satisfied 
    return redirect('/')    
   
if __name__ == '__main__':
    program.run(debug=True)