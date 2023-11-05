import time
import random
from flask import Flask, render_template, url_for, request,send_file, redirect, session
from hashed import encrypt
from werkzeug.utils import secure_filename
import os
from users_database import get_users
import hashlib
from authentication import check_username_password, check_username

app = Flask(__name__, static_folder="static")
app.config['SECRET_KEY'] = os.urandom(24).hex()

def get_current_user():
    user = None
    if "user" in session:
        user = session['user']
        db = get_users()
        user_cursor = db.execute("select * from users where username = ?", [user])
        user = user_cursor. fetchone()
    return user

@app.route('/')
def splash():
    
    return render_template('splash.html')

@app.route('/home')
def home():
    user = get_current_user()
    return render_template('home.html', user = user)

@app.route('/login',methods=['GET', 'POST']) # Added method
def login():
    error = None
    if request.method == 'POST':
        username = request.form['username']
        username_upper = username.upper()
        password = request.form['password']

        if check_username_password(username_upper, password):
            session['user'] = username_upper
            return redirect(url_for("home"))
        else:
            error = "Incorrect username or password"
            print("Incorrect username or password")

        print(f'Username is {username} and Password is {password}')

        #code = hashed.login(username, password)
        #print(f'State Code is {code}')
        

    return render_template ('login.html', error = error)

@app.route('/register',methods=['GET', 'POST'])

def register():
    error = None
    if request.method == 'POST':

        #retrieve info from registration form
        username = request.form['username']
        username_upper = username.upper()
        password = request.form['password']
        role = request.form['role']
        role = role.upper()

        print(f'Username is {username} and Password is {password}')

        hashed_password = encrypt(password)
        

        #connect to db 
        if check_username(username_upper):
            error = "That username is taken"
            return render_template('register.html', error=error)
        else:
            get_users().execute("insert into users (username, password, role,  admin) VALUES(?,?,?,?)",[username_upper,hashed_password, role,  '1'])
            get_users().commit()
        # Calling Hashed - if -1 account in system 
        # 0 - All good - account made. 

        #code = hashed.registation(username, password)
        #print(f'State Code is {code}')
        return redirect(url_for('login'))


    return render_template ('register.html')

@app. route ("/promote")
def promote():
    user = get_current_user()
    db = get_users()
    
    all_entries_cursor = db.execute('SELECT * FROM users')
    employees = all_entries_cursor.fetchall()
    
    return render_template('promote.html', user = user, employees = employees)


@app. route("/promotetoadmin/<int:empid>")
def promotetoadmin(empid):
    user = get_current_user()
    db = get_users()
    db.execute('UPDATE users SET admin = 1 WHERE id = ?', [empid])
    db.commit()
    return redirect(url_for('promote'))

@app. route("/revoke/ <int:empid>")
def revoke(empid):
    user = get_current_user()
    db = get_users()
    db.execute('UPDATE users SET admin = 0 WHERE id = ?', [empid])
    db.commit()
    return redirect(url_for('promote'))

@app. route ("/deleteuser/ <int:empid>")
def deleteuser(empid):
    user = get_current_user()
    db = get_users()
    db.execute('DELETE FROM users WHERE id = ?', [empid])
    db.commit()
    return redirect(url_for('promote'))

@app. route ("/logout")
def logout():
    session.pop('user' , None)
    return redirect(url_for ("splash"))

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

    
