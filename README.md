
# Transliteration-based-search-engine

- Upload some files( pdf/ text/ image) which contain Hindi text then that text will be extracted using OCR ( optical character recognition ) tool and stored in the database.
```bash
        Mongodb is used to store file data, For every file it will create new document with two fields 
        1. file_name - to store name of the file  2. content - to store content of the file
``` 

- Serach for Hindi string using English script, This system do Transliteration of English Script to Hindi script.
```bash
        Transliteration is the process of converting text from one script another script 
        example : "namaste" -->  "नमस्ते" (same pronunciation )
```

- Then it will search for Hindi string in all documents present in database and give file_names, matching accuracy and matching content as result wherever string is best matched. 




## Setup 

- Download and Install [python](https://www.geeksforgeeks.org/download-and-install-python-3-latest-version/)
- Install [python flask](https://pypi.org/project/Flask/)  
- download [mongodb Database](https://www.mongodb.com/try/download/community)  & [Install pymongo](https://pypi.org/project/pymongo/)  
- Install [python Imaging Library](https://pypi.org/project/Pillow/)  
- Download and install  [Tesseract OCR](https://medium.com/@akshit_29/optical-character-recognition-ocr-for-the-hindi-language-single-multiple-files-8f60ca2bfc06) and add path to Environment variable.
- Install [pdf2image](https://pypi.org/project/pdf2image/) / you can use this document also [pdf2image](https://www.geeksforgeeks.org/convert-pdf-to-image-using-python/) by  GFG
- Install [latest version of poppler](https://blog.alivate.com.au/poppler-windows/) then extract into C:\programm files, and add path to system environment 'C:\Program Files\[poppler folder]\bin'. 
- Install [fuzzywuzzy](https://pypi.org/project/fuzzywuzzy/)
- Install [Jinja2](https://pypi.org/project/Jinja2/) / In VisualStudio add jinja2 extension 


## Demonstration 

https://user-images.githubusercontent.com/69907734/165500878-51d08ef1-6512-4cf7-9170-198f7e227c9c.mp4


## Work-flow of system

![Transliteration Based Search Engine Flowchart (1)](https://user-images.githubusercontent.com/69907734/165507103-64162c94-9825-40b2-8f16-c0cb8e4eed7e.jpg)


## Reference

- https://inltk.readthedocs.io/en/latest/index.html
- https://kb.objectrocket.com/mongo-db/how-to-access-and-parse-mongodb-documents-in-python-364#:~:text=a%20MongoDB%20collection-,Use%20Python's%20list()%20function%20to%20return%20a%20list%20of,call%20into%20the%20list%20call
- https://www.geeksforgeeks.org/convert-pdf-to-image-using-python/ 
- https://github.com/Belval/pdf2image#readme
- https://medium.com/@akshit_29/optical-character-recognition-ocr-for-the-hindi-language-single-multiple-files-8f60ca2bfc06
- https://github.com/UB-Mannheim/tesseract/wiki
- https://www.kaggle.com/code/salonikalra/transliterate-using-http-google-input-tools/script
- https://cran.r-project.org/web/packages/fuzzywuzzyR/fuzzywuzzyR.pdf

