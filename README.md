
# Transliteration-based-search-engine

- In this system user upload some files( pdf/ text/ image) which contain Hindi text then that text will be extracted using OCR ( optical character recognition ) tool and stored in the database.
```bash
Mongodb is used to store file data, for every file it will create new document with two fields 
1. file_name - to store name of the file  2. content - to store content of the file
``` 

- User serach for Hindi string using English script then This system Transliterate string to Hindi string.
```bash
Transliteration is the process of converting text from one script another script 
example : "namaste" -->  "नमस्ते" (same pronunciation )
```

- This system will search for Hindi string in all documents present in database and give file_names and matching content as result where ever string is best matched. 



## Setup 

