

# ----------- IMPORT ALL NLP LIBRARY -------------------------------------
import os 
import pickle

import numpy as np 
import pandas as pd 
import nltk 
from nltk.tokenize import word_tokenize
from nltk.corpus import stopwords
from string import punctuation
from unidecode import unidecode
from contractions import fix
from nltk.stem import WordNetLemmatizer
from flask import Flask , render_template, request, jsonify
import config

# ---------------- LOAD MODEL AND TFIDF MODEL -----------------------------

with open(config.model_path, 'rb') as file:
    model = pickle.load(file)

with open(config.tfidf_path, 'rb') as file1:
    tfidf = pickle.load(file1)


# ---------------- DATA PREPROCESSING -------------------------------------
def remove_blank(text):
    data = text.replace("\\n","").replace("\t","")
    return data

def expand_text(text):
    data = fix(text)
    return data

stopwords_list = stopwords.words('english')
stopwords_list.remove("nor")
stopwords_list.remove("not")
stopwords_list.remove("no")

def handling_accented_chr(text):
    data = unidecode(text)
    return data

def clean_text(text):
    tokens = word_tokenize(text)
    data = [i.lower() for i in tokens]
    data = [i for i in data if i not in punctuation]
    data = [i for i in data if i not in stopwords_list]
    data = [i for i in data if i.isalpha()]
    data = [i for i in data if len(i)>2]
    return data 


def lemmatization(text_list):
    lemma = WordNetLemmatizer()
    final_text = []
    for i in text_list:
        a = lemma.lemmatize(i)
        final_text.append(a)
    return " ".join(final_text)

# ------------- CODE FOR FLASK APP -------------------------------------------

app = Flask(__name__)

@app.route('/')
def Home_App():
    return render_template("index.html")

@app.route("/prediction" , methods=['POST','GET'])
def predict_disaster_tweet():
    if request.method=='POST':
        data = request.form['text']

        clean_train = remove_blank(data)
        clean_train = expand_text(clean_train)
        clean_train = handling_accented_chr(clean_train)
        clean_train = clean_text(clean_train)
        clean_train = lemmatization(clean_train)

        tfidf_data = tfidf.transform([clean_train])

        y_pred = model.predict(tfidf_data.A)[0]

        if y_pred==1:
            a = f"🚨🚨🚨 Emergency Alert!!..  This Is Real Disaster Tweet 🚨🚨🚨"
        elif y_pred==0:
            a = f"🌟🌟🌟 Great News!... This Tweet is not about a Disaster. Enjoy your day with peace of mind. 🌟🌟🌟"

    return render_template("index.html", result=a)

if __name__=="__main__":
    app.run(debug=True, port = config.PORT, host=config.HOST)

