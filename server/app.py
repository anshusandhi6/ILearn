from flask import Flask, request, jsonify, make_response ,send_file
from flask_sqlalchemy import SQLAlchemy
from flask_bcrypt import Bcrypt
from fpdf import FPDF 
from flask_marshmallow import Marshmallow
# from flask.helpers import safe_join
from flask_cors import CORS
# from functools import wraps
import jwt
import json
import datetime
import time
from gtts import gTTS
from googletrans import Translator
from selenium import webdriver
from bs4 import BeautifulSoup
import requests
import urllib.request
from mutagen.mp3 import MP3
import numpy as np
from PIL import Image                                              
import os, sys   
import math  
import time
import sys
import cv2
import glob

from englisttohindi.englisttohindi import EngtoHindi 
import os 
import pytesseract
from moviepy.editor import *

import shutil
import os
import random
import fitz
import nltk
import gensim
import pandas as pd
import PyPDF2
import moviepy.editor as mp

# import os

# import uuid
# import base64
# import re
# from PIL import Image
# import numpy as np 
# import cv2
# import matplotlib.pyplot as plt 
# from parsing import parse
# from posing import pose
# from cpvton_wrapper import *
# from utils_cpvton import *




# model = Model()

app = Flask(__name__)

app.config['SECRET_KEY'] = 'edTechHackathon'
CORS(app)
# database name 
app.config['SQLALCHEMY_DATABASE_URI'] = 'sqlite:///Database1.db'
app.config['SQLALCHEMY_TRACK_MODIFICATIONS'] = True
# creates SQLALCHEMY object 
db = SQLAlchemy(app) 
ma = Marshmallow(app)
bcrypt = Bcrypt(app)



def token_required(func):
    def wrapper(*args,**kwargs):

        token = request.headers['x-auth-token']

        if not token:
            return jsonify({'message':'Token is missing'})
        
        try:
            data = jwt.decode(token,app.config['SECRET_KEY'], algorithms=["HS256"])
            request.data = data
        except:
            return jsonify({'message':'invalid token'})
        return func(*args,**kwargs)
    wrapper.__name__ = func.__name__
    return wrapper



from models import User,user_schema,users_schema

#auth decorator to act as middleware

@app.route("/",methods=["GET"])
def getpost():
    return jsonify({'message':"something"})

@app.route("/allUsers",methods=["GET"])
def printAllUsers():
    users = User.query.all()
    result = users_schema.dump(users)
    return jsonify({"users": result})


@app.route("/register",methods=["POST"])    
def register():
    req = request.json
    if(req.get('first_name') and req.get('email') and req.get('password')):
        # print(req['email'])
        
        user = User.query.filter_by(email= req['email']).first()

        if(user):
            return jsonify({'message':'seems like the email id is already registered'})

        password = bcrypt.generate_password_hash(req['password']).decode('utf-8')
        user1 = User(first_name=req['first_name'],last_name=req['last_name'],email=req['email'],password=password)
        db.session.add(user1)
        db.session.commit()
        token = jwt.encode({'id':user1.id,'exp': datetime.datetime.utcnow() + datetime.timedelta(minutes=180)},app.config['SECRET_KEY'])         
        # print("token:"+token.decode('UTF-8'))
        if token:
            resp = {
                'token': token,
                'user' : user_schema.dump(user1)
            } 
            return jsonify(resp)
        else:
            return jsonify({'message':'Problem in creating a token'})
    else:
        return jsonify({'message': 'please enter all the values required for the creation of a new user'})
    

@app.route("/login",methods=["POST"])
def login():
    req = request.json

    if(req.get('email') and req.get('password')):

        user = User.query.filter_by(email= req['email']).first()

        if(user):
            if(user and bcrypt.check_password_hash(user.password,req['password'])):
                #things to do after checking the email and password
                token = jwt.encode({'id':user.id,'exp': datetime.datetime.utcnow() + datetime.timedelta(minutes=180)},app.config['SECRET_KEY'])         
                # print("token:"+token.decode('UTF-8'))
                if token:
                    resp = {
                        'token': token,
                        'user' : user_schema.dump(user)
                    } 
                    return jsonify(resp)
                else:
                    return jsonify({'message':'Problem in creating a token'})
            else:
                return jsonify({'message':'it seems that this email is not registered'})
        else:
            return jsonify({'message':'Login Unsuccesful.Please check email and password'})


@app.route('/login/user',methods=['GET'])
@token_required
def protected():
    data = request.data

    user = User.query.get(data['id'])
    if user:
        # resp ={
        #     'first_name': user.first_name,
        #     'last_name' : user.last_name,
        #     'email':user.email,
        #     "id":user.id
        # }
        result = user_schema.dump(user)
        return jsonify({'user': result})
    else:
        return jsonify({'message':'This is a protected'})

@app.route('/convertTextToPdf',methods=['POST'])
def convertTextToPdf():
    pdf = FPDF() 
    pdf.add_page()
    req = request.json
    string = req.get('text')
    example =string.split('.')
    pdf.set_font("Arial", size = 14) 
    lnc=1
    for i in example:
        pdf.cell(200, 10, txt = i, 
                ln = lnc, align = 'C') 
        lnc=lnc+1
    pdf.output("anshuman.pdf")
    return send_file(os.getcwd() +'/anshuman.pdf')


@app.route('/api/upload',methods=['POST'])
def handleUpload():
    file = request.files['file']
    print(file)
    
    files_name=os.path.splitext(file.filename)[0]

    language = request.form['language']
    speed = request.form['speed']
    lang=""
    if language == "Hindi" :
        lang="hi"
    elif language == "Bengali":
        lang="bn"
    elif language =="Telugu":
        lang="te"
    elif language =="Kannada":
        lang="kn"
    elif language =="Marathi":
        lang="mr"
    elif language =="Urdu":
        lang="ur"
    elif language =="Engish":
        lang="en"
    else :
        lang="ta"

    file.save(dst='uploads/example.pdf', buffer_size=16384)
    # pytesseract.pytesseract.tesseract_cmd = r'C:/Program Files/Tesseract-OCR/tesseract.exe'
    f1 = open("uploads/example.pdf",'rb')
    read1 = PyPDF2.PdfFileReader(f1)
    n1 = read1.numPages
    import fitz
    page1 = read1.getPage(0)
    text1 = page1.extractText()
    pdf1_text =[0]
    for p in range(0,n1):
        page = read1.getPage(p)
        pdf1_text.append(page.extractText())

    from nltk.tokenize import sent_tokenize, word_tokenize
    nltk.download('punkt')
    tokenized_1 =[]
    for data in pdf1_text:
        token_1 =sent_tokenize(str(data))
        for line in token_1:
            tokenized_1.append(line)
    message = " " 
    from nltk.corpus import stopwords  
    from nltk.tokenize import word_tokenize  
    message = ' '.join([str(elem) for elem in tokenized_1]) 


    stop_words = set(stopwords.words('english'))  

    word_tokens = word_tokenize(message)  
    
    filtered_sentence = [w for w in word_tokens if not w in stop_words]  
    
    filtered_sentence = []  
    
    for w in word_tokens:  
        if w not in stop_words:  
            filtered_sentence.append(w)  

    message= ' '.join([str(elem) for elem in filtered_sentence]) 
    punc = ',#!?.'

    for ele in message:  
        if ele in punc:  
            message =  message.replace(ele, "")  

    filtered_sentence = list(message.split(" "))
    translator = Translator()
    result1 = translator.translate(pdf1_text[1])
    source=result1.src
    print(result1.src)
    while("" in filtered_sentence) : 
        filtered_sentence.remove("") 

    while("0" in filtered_sentence) : 
        filtered_sentence.remove("0") 

    while("The" in filtered_sentence) : 
        filtered_sentence.remove("The") 


    def audio():
        print(pdf1_text[1])
        print(lang)
        
        result = translator.translate(pdf1_text[1], src=source, dest=lang)
        print("ok")
        myobj = gTTS(text=result.text, lang=lang, slow=True) 
        audio_name = files_name+".mp3"
        myobj.save(audio_name) 

    def images():
        count=0
        for download in  filtered_sentence:
        
        
            site = 'https://www.google.com/search?tbm=isch&q='+download

            driver = webdriver.Firefox(executable_path = 'geckodriver.exe')

            driver.get(site)

            i = 0

            while i<2:  
                #for scrolling page
                driver.execute_script("window.scrollBy(0,document.body.scrollHeight)")
                
                try:
                    #for clicking show more results button
                    driver.find_element_by_xpath("/html/body/div[2]/c-wiz/div[3]/div[1]/div/div/div/div/div[5]/input").click()
                except Exception as e:
                    pass
                time.sleep(1)
                i+=1

            #parsing
            soup = BeautifulSoup(driver.page_source, 'html.parser')


            
            driver.close()


            
            img_tags = soup.find_all("img", class_="rg_i")


            lol=0
            if count>9 :
                x="0"
            else:
                x="00"
            for i in img_tags:
                if lol < 1:

                    try:
                        #passing image urls one by one and downloading
                        images="images/"
                        urllib.request.urlretrieve(i['src'], images+x+str(count)+".jpg")
                        lol+=1
                        
                    except Exception as e:
                        pass

            count+=1


                



        path = "images/"
        dirs = os.listdir( path )                                       

        def resize():
            for item in dirs:
                if os.path.isfile(path+item):
                    im = Image.open(path+item)
                    f, e = os.path.splitext(path+item)
                    imResize = im.resize((200,200), Image.ANTIALIAS)
                    imResize.save(f+'.png', 'png', quality=98)

        resize()

        

        video_name = "video3.avi"

        file_list = []
        img_array = []
        for filename in glob.glob('images/*.png'):
            file_list.append(filename)


        
        for i in file_list:
            frame = cv2.imread(i)
            height, width, layers = frame.shape
            frame_size = (width,height)
            img_array.append(frame)

        

        # function to convert the seconds into readable format
        def convert(seconds):
            hours = seconds // 3600
            seconds %= 3600

            mins = seconds // 60
            seconds %= 60

            return hours, mins, seconds

        # Create an MP3 object
        # Specify the directory address to the mp3 file as a parameter
        audio_name = files_name+".mp3"
        audio = MP3(audio_name)
        audio_info = audio.info    
        length_in_secs = int(audio_info.length)
        hours, mins, seconds = convert(length_in_secs)
        sum=len(file_list)/seconds
        video = cv2.VideoWriter(video_name, cv2.VideoWriter_fourcc(*"DIVX"),sum, frame_size)
        for i in range(len(img_array)):
            video.write(img_array[i])



        cv2.destroyAllWindows()
        video.release()


    def combines():
        audio_name = files_name+".mp3"
        audio = mp.AudioFileClip(audio_name)
        video1 = mp.VideoFileClip("video3.avi")
        final = video1.set_audio(audio)
        video_name = files_name+".webm"
        final.write_videofile(video_name,codec= 'libvpx' ,audio_codec='libvorbis')
        
        clip = VideoFileClip(video_name) 
        clip = clip.subclip(0, clip.duration) 
        final = clip.fx( vfx.speedx,float(speed))     
        dir = 'images/'
        for f in os.listdir(dir):
            os.remove(os.path.join(dir, f))

    
    audio()
    images()
    combines()



    return jsonify({'message': "something"})


@app.route('/api/uploadformText',methods=['POST'])
def handleUpload1():

    
    files_name="anshuman"


    language = request.form['language']
    speed = request.form['speed']
    lang=""
    if language == "Hindi":
        lang="hi"
    elif language == "Bengali":
        lang="bn"
    elif language =="Telugu":
        lang="te"
    elif language =="Kannada":
        lang="kn"
    elif language =="Marathi":
        lang="mr"
    elif language =="Urdu":
        lang="ur"
    elif language =="Engish":
        lang="en"
    else :
        lang="ta"

    
    # pytesseract.pytesseract.tesseract_cmd = r'C:/Program Files/Tesseract-OCR/tesseract.exe'
    f1 = open("anshuman.pdf",'rb')
    
    read1 = PyPDF2.PdfFileReader(f1)
    n1 = read1.numPages
    import fitz
    page1 = read1.getPage(0)
    text1 = page1.extractText()
    pdf1_text =[0]
    for p in range(0,n1):
        page = read1.getPage(p)
        pdf1_text.append(page.extractText())

    from nltk.tokenize import sent_tokenize, word_tokenize
    nltk.download('punkt')
    tokenized_1 =[]
    for data in pdf1_text:
        token_1 =sent_tokenize(str(data))
        for line in token_1:
            tokenized_1.append(line)
    message = " " 
    from nltk.corpus import stopwords  
    from nltk.tokenize import word_tokenize  
    message = ' '.join([str(elem) for elem in tokenized_1]) 


    stop_words = set(stopwords.words('english'))  

    word_tokens = word_tokenize(message)  
    
    filtered_sentence = [w for w in word_tokens if not w in stop_words]  
    
    filtered_sentence = []  
    
    for w in word_tokens:  
        if w not in stop_words:  
            filtered_sentence.append(w)  

    message= ' '.join([str(elem) for elem in filtered_sentence]) 
    punc = ',#!?.'

    for ele in message:  
        if ele in punc:  
            message =  message.replace(ele, "")  

    filtered_sentence = list(message.split(" "))
    translator = Translator()
    result1 = translator.translate(pdf1_text[1])
    source=result1.src
    print(result1.src)
    while("" in filtered_sentence) : 
        filtered_sentence.remove("") 

    while("0" in filtered_sentence) : 
        filtered_sentence.remove("0") 

    while("The" in filtered_sentence) : 
        filtered_sentence.remove("The") 


    def audio():
        print(pdf1_text[1])
        print(lang)
        
        result = translator.translate(pdf1_text[1], src=source, dest=lang)
        print("ok")
        myobj = gTTS(text=result.text, lang=lang, slow=True) 
        audio_name = files_name+".mp3"
        myobj.save(audio_name) 

    def images():
        count=0
        for download in  filtered_sentence:
        
        
            site = 'https://www.google.com/search?tbm=isch&q='+download

            driver = webdriver.Firefox(executable_path = 'geckodriver.exe')

            driver.get(site)

            i = 0

            while i<2:  
                #for scrolling page
                driver.execute_script("window.scrollBy(0,document.body.scrollHeight)")
                
                try:
                    #for clicking show more results button
                    driver.find_element_by_xpath("/html/body/div[2]/c-wiz/div[3]/div[1]/div/div/div/div/div[5]/input").click()
                except Exception as e:
                    pass
                time.sleep(1)
                i+=1

            #parsing
            soup = BeautifulSoup(driver.page_source, 'html.parser')


            
            driver.close()


            
            img_tags = soup.find_all("img", class_="rg_i")


            lol=0
            if count>9 :
                x="0"
            else:
                x="00"
            for i in img_tags:
                if lol < 1:

                    try:
                        #passing image urls one by one and downloading
                        images="images/"
                        urllib.request.urlretrieve(i['src'], images+x+str(count)+".jpg")
                        lol+=1
                        
                    except Exception as e:
                        pass

            count+=1


                



        path = "images/"
        dirs = os.listdir( path )                                       

        def resize():
            for item in dirs:
                if os.path.isfile(path+item):
                    im = Image.open(path+item)
                    f, e = os.path.splitext(path+item)
                    imResize = im.resize((200,200), Image.ANTIALIAS)
                    imResize.save(f+'.png', 'png', quality=98)

        resize()

        

        video_name = "video3.avi"

        file_list = []
        img_array = []
        for filename in glob.glob('images/*.png'):
            file_list.append(filename)


        
        for i in file_list:
            frame = cv2.imread(i)
            height, width, layers = frame.shape
            frame_size = (width,height)
            img_array.append(frame)

        

        # function to convert the seconds into readable format
        def convert(seconds):
            hours = seconds // 3600
            seconds %= 3600

            mins = seconds // 60
            seconds %= 60

            return hours, mins, seconds

        # Create an MP3 object
        # Specify the directory address to the mp3 file as a parameter
        audio_name = files_name+".mp3"
        audio = MP3(audio_name)
        audio_info = audio.info    
        length_in_secs = int(audio_info.length)
        hours, mins, seconds = convert(length_in_secs)
        sum=len(file_list)/seconds
        video = cv2.VideoWriter(video_name, cv2.VideoWriter_fourcc(*"DIVX"),sum, frame_size)
        for i in range(len(img_array)):
            video.write(img_array[i])



        cv2.destroyAllWindows()
        video.release()


    def combines():
        audio_name = files_name+".mp3"
        audio = mp.AudioFileClip(audio_name)
        video1 = mp.VideoFileClip("video3.avi")
        final = video1.set_audio(audio)
        video_name = files_name+".webm"
        final.write_videofile(video_name,codec= 'libvpx' ,audio_codec='libvorbis')
        
        clip = VideoFileClip(video_name) 
        clip = clip.subclip(0, clip.duration) 
        final = clip.fx( vfx.speedx,float(speed))     
        dir = 'images/'
        for f in os.listdir(dir):
            os.remove(os.path.join(dir, f))

    
    audio()
    images()
    combines()


    f1.close()
    
    return jsonify({'message': "something"})

@app.route('/generate/<filename>',methods=['GET'])
def hostFiles(filename):
    # filename = safe_join(app.root_path,"some_image")
    print(filename)

    return send_file(os.getcwd()  +'/' + filename)


def getApp():
    return app



if __name__ == "__main__":
    app.run(debug=True)