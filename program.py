from distutils.command.config import LANG_EXT
from flask import Flask, jsonify, render_template, redirect, url_for, request, flash, json
# from flask_mongoengine import MongoEngine
from flask_pymongo import PyMongo
from pymongo import MongoClient

from werkzeug.utils import secure_filename
import os
import PyPDF2
from PyPDF2 import PdfFileReader

import PIL 
from PIL import Image, ImageDraw
import spacy
import pytesseract as pt
from pdf2image import convert_from_path

from indic_transliteration import sanscript
from indic_transliteration.sanscript import transliterate
# import easyocr
# import cv2 as cv
#import urllib.request

program = Flask(__name__)  #program is a variable that contains a website and load in memory 
program.secret_key = "key" #If app.secret_key isn't set, Flask will not allow you to set or access the session dictionary.

# program.config['MONGODB_SETTINGS'] = {
#     'db': 'MyDB',
#     'host': 'localhost',
#     'port': 27017
# }
# db = MongoEngine() #Initialization of MongoEngine object
# db.init_app(program)
program.config["MONGO_URI"] = "mongodb://localhost:27017/MyDB"
# mongodb_client = PyMongo(program)
# db = mongodb_client.db
client = MongoClient()
db = client.MyDB        #database MyDB
collection = db.user    #inside MyDB, a collection called user

UPLOAD_FOLDER = 'static/saved_files' #The file will be stored here 
program.config['UPLOAD_FOLDER'] = UPLOAD_FOLDER 
# program.config['MAX_CONTENT_LENGTH'] = 16 * 1024 * 1024 #maximum size a file can have i.e. 16 MB
   
ALLOWED_EXTENSIONS = set(['txt', 'pdf', 'png', 'jpg', 'jpeg', 'gif'])  # These are allowed extensions 
   
def allowed_file(filename):  # This function is used to check file extenstion 
 return '.' in filename and filename.rsplit('.', 1)[1].lower() in ALLOWED_EXTENSIONS

# class User(db.Document): #database 
#     file_name = db.StringField()

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
        #    usersave = User(file_name=file.filename) #calling user class
        #    usersave.save() #to save file name in db
        if '.' in filename and filename.rsplit('.', 1)[1].lower() == "pdf": #checking whether the  file is pdf or not  
            # f = open("C:\\Users\\ap888\\Desktop\\Internship CLIDE\\Transliteration_flask\\static\\saved_files\\" + file.filename,'rb') #pdf files with images are not allowed
            # Pdfreader = PyPDF2.PdfFileReader(f) #pdf reader object 
            # text = ""
            # for i in range(0):
            #     page = Pdfreader.getPage(i)
            #     text = text + page.extractText()
            # db.user.insert_one({'file_name': file.filename, 'content' : text}) 
            # f.close()
            images = convert_from_path('C:\\Users\\ap888\\Desktop\\Internship CLIDE\\Transliteration_flask\\static\\saved_files\\" + file.filename')
            flash(images)
        elif '.' in filename and filename.rsplit('.', 1)[1].lower() == "txt":
                f = open("C:\\Users\\ap888\\Desktop\\Internship CLIDE\\Transliteration_flask\\static\\saved_files\\" + file.filename,'r',encoding = 'utf-8') #if the file is text file
                text = f.read()   #read the entire content, it tet should be UTF-8 text
                db.user.insert_one({'file_name': file.filename, 'content' : text}) #insert content into database
                f.close()
        else: # if file is image file
            pt.pytesseract.tesseract_cmd = r'C:\Users\ap888\Desktop\Internship CLIDE\Transliteration_flask\env\Tesseract.exe' #specifying the path of tesseract / it can also be dont using environment variable 
            img = Image.open("C:\\Users\\ap888\\Desktop\\Internship CLIDE\\Transliteration_flask\\static\\saved_files\\" + file.filename)
            text = pt.image_to_string(img, lang="hin") #only working for hindi language
            db.user.insert_one({'file_name': file.filename, 'content' : text})

        #    db.user.insert(text_file_doc)
        flash('File successfully uploaded ' + file.filename + ' to the database!') # flash message 
        #    file_names = db.user.find()
        return redirect('/') # redirect of main page
    else:
       flash('Invalid Uplaod only txt, pdf, png, jpg, jpeg, gif') #flash message,if condition not satisfied 
    return redirect('/')    








# This fucntion is used to get input value from user
@program.route("/search", methods=["POST", "GET"])
def search():
    if request.method == "POST":
        user_serach = request.form["user_search"]
        return(transliterate(user_serach, sanscript.ITRANS, sanscript.DEVANAGARI)) 
    else:
        return redirect('/')
   
if __name__ == '__main__':
    program.run(debug=True)
