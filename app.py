# import argparse
# import re
# import requests
# import shutil
# import time
# import cv2
import io
from PIL import Image
import datetime
import torch
import numpy as np
import tensorflow as tf
from re import DEBUG, sub
from flask import Flask, render_template, request, redirect, send_file, url_for, Response,session
from werkzeug.utils import secure_filename, send_from_directory
import os
import subprocess
from subprocess import Popen
import sqlite3
import string
from detect import count
from flask import Flask, render_template, request, url_for, flash, redirect
from tkinter import *
from tkinter import messagebox
import stripe
app = Flask(__name__)
app.secret_key="123"
import sqlite3
public_key = "pk_test_6pRNASCoBOKtIshFeQd4XMUh"
stripe.api_key = "sk_test_BQokikJOvBiI2HlWgH4olfQ2"
conn = sqlite3.connect('./project1.db')
conn.cursor()
print('Connected to Database')
# def myFun():
#    top = Tk()
#    top.geometry("100x100")
#    messagebox.showinfo("informatio1n", "Information1")
#    top.mainloop()

# def myFun2():
#    top = Tk()
#    top.geometry("100x100")
#    messagebox.showinfo("information2", "Information2")
#    top.mainloop()

@app.route('/')
def index():
   # if request.method == "POST":
      # myFun()
   return render_template('splash.html')

@app.route('/aboutus')
def aboutus():
   # if request.method == "POST":
      # myFun()
   return render_template('aboutus.html')

@app.route('/loginPage')
def loginPage():
   return render_template('signinpage.html')


@app.route('/logout')
def logout():
   session.clear()
   return render_template('splash.html')

@app.route('/login',methods=('GET', 'POST'))
def login():
   import sqlite3 as sql
   con = sql.connect("./project1.db")
   if request.method == "POST":
      #if request.form['submit'] == 'Sign In':
         email = request.form['email']
         password = request.form['password']
         cur = con.cursor()
         statement = f"SELECT email from users WHERE email='{email}' AND password = '{password}';"
         cur.execute(statement)
         if not cur.fetchone():  # An empty result evaluates to False.
            print(" wrong output")
            return "<h1> Please Put the correct email and passowrd</h1>"
            #return redirect('signinpage.html')
         else:
            return render_template('u_interface.html')
   else:
      return redirect('signinpage.html')

@app.route('/signup',methods=('GET', 'POST'))
def signup():
   import sqlite3
   conn = sqlite3.connect('./project1.db')
   if request.method == "POST":
      #if request.form['signup'] == 'signup':
      email = request.form['email']
      vehicle = request.form['vehicle']
      password1 = request.form['password']
      phone_no = request.form['phone-no']
      #if password1 == password2:
      conn.execute("INSERT INTO users (email,password,vehicle,phone) VALUES ('"+email+"', '"+password1+"','"+vehicle+"','"+phone_no+"')")
      conn.commit()
      print("SignUp successfully")
      return render_template('signinpage.html')
      #else:
            #print('Please enter valid password.')
            #return render_template('signup.html')
   else:
      return render_template('signup.html')

@app.route('/contactus',methods=('GET', 'POST'))
def contactus():
   # if request.method == "POST":
      # myFun()
   return render_template('contactus.html')

@app.route('/u_interface')
def u_interface():
   return render_template('u_interface.html')

@app.route('/uploadFile')
def uploadFile():
    return render_template('uploadFile.html') 

@app.route("/uploadid", methods=["GET", "POST"])
def predict_image():
    print("this is predict")
    if request.method == "POST":
        if 'file' in request.files:
            f = request.files['file']
            basepath = os.path.dirname(__file__)
            filepath = os.path.join(basepath,'uploads',f.filename)
            print("upload folder is ", filepath)
            f.save(filepath)
            predict_image.imgpath = f.filename
            print("printing predict_img :::::: ", predict_image)
            file_extension = f.filename.rsplit('.', 1)[1].lower()    
            if file_extension == 'jpg' or 'jepg' or 'png':
                process = Popen(["python", "detect.py", '--source', filepath, "--weights","best_246.pt"], shell=True)
                process.wait()
                
            # elif file_extension == 'mp4':
            #     process = Popen(["python", "detect.py", '--source', filepath, "--weights","best_246.pt"], shell=True)
            #     process.communicate()
            #     process.wait()

   #  folder_path = 'runs/detect'
   #  subfolders = [f for f in os.listdir(folder_path) if os.path.isdir(os.path.join(folder_path, f))]    
   #  latest_subfolder = max(subfolders, key=lambda x: os.path.getctime(os.path.join(folder_path, x)))    
    #image_path = folder_path+'/'+latest_subfolder+'/'+f.filename 
    return redirect(url_for('display'))

@app.route('/my-image') 
def myimage():
    return('display_image.html')

def get_image_files(directory):
    image_extensions = ['.jpg', '.jpeg', '.png', '.gif']  
    latest_image=[]
    image_files = [filename for filename in os.listdir(directory) 
                    if filename.lower().endswith(tuple(image_extensions))]
    print(image_files)
    latest_image_path = f"{directory}/{image_files[0]}"
    print(latest_image_path)
    return latest_image_path
def get_latest_directory(directory):

    subdirectories = [os.path.join(directory, name) for name in os.listdir(directory) if os.path.isdir(os.path.join(directory, name))]
    latest_directory = max(subdirectories, key=os.path.getmtime, default=None)
    return latest_directory

@app.route('/display')
def display():
    directory = 'static/runs/detect'
    latest_dir = get_latest_directory(directory)
    latest_dir= latest_dir.replace('\\','/')
    
    print(latest_dir)
    if latest_dir:
        image_file = get_image_files(latest_dir)
        return  render_template('display_image.html',img=str(image_file))
    return "<h1> no file found</h1>"
        
if __name__ == "__main__":
    model = torch.hub.load('.','custom','best_246.pt', source='local')
    model.eval()
    app.debug=True 
    app.run(debug=True, port=8080)  # debug=True causes Restarting with stat
