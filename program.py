from cgitb import reset
from flask import Flask, jsonify, render_template, redirect, url_for, request, flash, json
# from flask_mongoengine import MongoEngine
from flask_pymongo import PyMongo
from numpy import imag, result_type
from pymongo import MongoClient

from werkzeug.utils import secure_filename
import os
import PyPDF2
from PyPDF2 import PdfFileReader

import PIL 
from PIL import Image, ImageDraw
import spacy
import pytesseract as pt
from pdf2image import convert_from_path, convert_from_bytes

from pdf2image.exceptions import (
    PDFInfoNotInstalledError,
    PDFPageCountError,
    PDFSyntaxError
)

from indic_transliteration import sanscript
from indic_transliteration.sanscript import transliterate

from elt import translit
import transliterate


from fuzzywuzzy import fuzz
from fuzzywuzzy import process
# from thefuzz import fuzz, process
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

#specifying the path of tesseract / it can also be dont using environment variable
pt.pytesseract.tesseract_cmd = r'C:\Users\ap888\Desktop\Internship CLIDE\Transliteration_flask\env\Tesseract.exe'  

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
            # for i in range(0, Pdfreader.getNumPages()):
            #     page = Pdfreader.getPage(i)
            #     image = convert_from_path(page)
            #     flash(image)
            #     text = text + page.extractText()
            # db.user.insert_one({'file_name': file.filename, 'content' : text}) 
            # f.close()
            #poppler_path = r'C:\Program Files\poppler-0.68.0\bin'
            images = convert_from_path("C:\\Users\\ap888\\Desktop\\Internship CLIDE\\Transliteration_flask\\static\\saved_files\\" + file.filename)
            text = " "
            for i in range(len(images)):
                text = text + pt.image_to_string(images[i], lang="hin")
            db.user.insert_one({'file_name': file.filename, 'content' : text})

        elif '.' in filename and filename.rsplit('.', 1)[1].lower() == "txt":
                f = open("C:\\Users\\ap888\\Desktop\\Internship CLIDE\\Transliteration_flask\\static\\saved_files\\" + file.filename,'r',encoding = 'utf-8') #if the file is text file
                text = f.read()   #read the entire content, it tet should be UTF-8 text
                db.user.insert_one({'file_name': file.filename, 'content' : text}) #insert content into database
                f.close()

        else: # if file is image file
            img = Image.open("C:\\Users\\ap888\\Desktop\\Internship CLIDE\\Transliteration_flask\\static\\saved_files\\" + file.filename)
            text = pt.image_to_string(img, lang="hin") #only for hindi language
            db.user.insert_one({'file_name': file.filename, 'content' : text})

        #    db.user.insert(text_file_doc)
        flash(file.filename + '  is successfully uploaded to the database!') # flash message 
        #    file_names = db.user.find()
        return redirect('/') # redirect of main page
    else:
       flash('Invalid Uplaod only txt, pdf, png, jpg, jpeg, gif') #flash message,if condition not satisfied 
    return redirect('/')    


# This fucntion is used to get input value from user
@program.route("/search", methods=["POST", "GET"])
def search():
    #Can be found by inspecting http response of google input tools page
    lang = {'hindi':"hi-t-i0-und"}
    if request.method == "POST":
        user_serach = request.form["user_search"]
        output = transliterate.driver(user_serach.strip(), lang['hindi'])
        return redirect(url_for("temp", search = output))
    else:
        return redirect('/')

@program.route("/<search>")
def temp(search):
    search_list = []
    for x in search.split(" "):
        if x != "":
            search_list.append(x)
    matching_content = {}
    result = {}
    for doc in collection.find():
        doc_content = doc["content"].split("\n")
        for x in doc_content:
            if len(x) < len(search):
                doc_content.remove(x)
        res = process.extract(search, doc_content,scorer=fuzz.partial_ratio)
        for x in res:
            if len(x[0]) < len(search):
                res.remove(x)
        best_sub_res = {}
        for sub_res in res:
            count = 0
            for x in search_list:
                if x in sub_res[0]:
                    count += 1
            best_sub_res[sub_res[0]] = count
            sort_best_sub_res = sorted(best_sub_res.items(), key=lambda x: x[1], reverse=True)
            accuracy = fuzz.partial_ratio(sort_best_sub_res[0][0],search)
            if accuracy > 20:
                result[doc["file_name"]] = accuracy
                matching_content[doc["file_name"]] = sort_best_sub_res[0][0]
    sort_result = sorted(result.items(), key=lambda x: x[1], reverse=True)
    return render_template('result.html', file_names = sort_result, searching_for = search, number=len(sort_result), content = matching_content)

if __name__ == '__main__':
    program.run(debug=True)
