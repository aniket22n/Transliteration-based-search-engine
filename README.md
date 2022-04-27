
# Transliteration-based-search-engine

- Upload some files( pdf/ text/ image) which contain Hindi text then that text will be extracted using OCR ( optical character recognition ) tool and stored in the database.
```bash
        Mongodb is used to store file data, for every file it will create new document with two fields 
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
- Download and install  [Tesseract OCR](https://medium.com/@akshit_29/optical-character-recognition-ocr-for-the-hindi-language-single-multiple-files-8f60ca2bfc06) and set path Environment variable
- Install [pdf2image](https://pypi.org/project/pdf2image/) / you can use this document also [pdf2image](https://www.geeksforgeeks.org/convert-pdf-to-image-using-python/) by  GFG
- Install [fuzzywuzzy](https://pypi.org/project/fuzzywuzzy/)
- Install [Jinja2](https://pypi.org/project/Jinja2/) / In VisualStudio add jinja2 extension 


## demonstration 

https://user-images.githubusercontent.com/69907734/165500878-51d08ef1-6512-4cf7-9170-198f7e227c9c.mp4


