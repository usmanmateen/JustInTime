import time
import random
from flask import Flask, render_template, url_for, request,send_file
import hashed
from werkzeug.utils import secure_filename
import os


app = Flask(__name__)

@app.route('/')
def home():
    return render_template('home.html')

@app.route('/login',methods=['GET', 'POST']) # Added method
def login():
    if request.method == 'POST':
        username = request.form['username']
        password = request.form['password']
        
        print(f'Username is {username} and Password is {password}')

        code = hashed.login(username, password)
        print(f'State Code is {code}')
        

    return render_template ('login.html')

@app.route('/register',methods=['GET', 'POST'])
def register():
    if request.method == 'POST':
        username = request.form['username']
        password = request.form['password']
        
        print(f'Username is {username} and Password is {password}')
        
        # Calling Hashed - if -1 account in system 
        # 0 - All good - account made. 

        code = hashed.registation(username, password)
        print(f'State Code is {code}')


    return render_template ('register.html')



@app.route('/upload', methods=['GET','POST'])
def upload_file():
    if 'file' in request.files:
        file = request.files['file']
        filename = secure_filename(file.filename)
        # Here you should save the file
        file.save(os.path.join("uploads/", filename)) ## Saves the file to uploads/ 

        print('File uploaded successfully')

    return render_template('upload_form.html')


def main():
    app.run(debug=True)
    print("Code Stopped")


main()
print("Bye")

    
