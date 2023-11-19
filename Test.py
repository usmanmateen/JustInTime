import time
import random
from flask import Flask, render_template, url_for, request,send_file, redirect, session
from functools import wraps
from flask import request, redirect, url_for, session
from hashed import encrypt
from werkzeug.utils import secure_filename
import os
from users_database import get_db
import hashlib
from authentication import check_username_password, check_username
from Insert import employeedata, accountsdata, roleID, employeeID

app = Flask(__name__, static_folder="static")
app.config['SECRET_KEY'] = os.urandom(24).hex()

def get_current_user():
    user = None
    if "user" in session:
        user = session['user']
        print(user)
        db = get_db()
        user_cursor = db.execute("select * from Accounts where Username = ?", [user])
        user = user_cursor. fetchone()
    return user


@app.route('/')
def splash():
    return render_template('splash.html')

@app.route('/home')
def home():
    user = get_current_user()
    if 'logged_in' in session and session['logged_in']:
        return render_template('home.html', user = user)
    else:
        return redirect(url_for('login'))
    


@app.route('/login',methods=['GET', 'POST']) # Added method
def login():
    error = None
    if request.method == 'POST':
        username = request.form['username']
        username_upper = username.upper()
        password = request.form['password']
        #hashed_password = encrypt(password)

        if check_username_password(username_upper, password):
            session['user'] = username_upper
            session['logged_in'] = True
            return redirect(url_for("home"))
        else:
            error = "Incorrect username or password"
            print("Incorrect username or password")
            print(password)

        print(f'Username is {username} and Password is {password}')

        

    return render_template ('login.html', error = error)

@app.route('/register', methods=['GET', 'POST'])
def register():
    error = None
    if request.method == 'POST':
        # Retrieve info from the registration form
        username = request.form['username']
        username_upper = username.upper()
        password = request.form['password']
        role = request.form['role']
        role = role.upper()
        token = request.form.get('token', None)
        firstname = request.form['firstname']
        lastname = request.form['lastname']
        email = request.form['email']
        contact = request.form['contact']

        admin = '0'  # Default to non-admin

        if token == '4dm1nr0l3':
            admin = '1'

        print(f'Username is {username} and Password is {password}')

        hashed_password = encrypt(password)

        # Connect to the database
        if check_username(username_upper):
            error = "That username is taken"
            return render_template('register.html', error=error)
        else:
            employeedata(firstname, lastname, contact, email, username)
            accountsdata(username_upper, hashed_password, role, admin, roleID(role), employeeID(username))

        # Redirect to the login page after registration
        return redirect(url_for('login'))

    return render_template('register.html')


@app. route ("/promote")
def promote():
    user = get_current_user()
    db = get_db()
    if 'logged_in' in session and session['logged_in'] and user[ 'admin'] == 1:
        all_entries_cursor = db.execute('SELECT * FROM Accounts')
        employees = all_entries_cursor.fetchall()
        return render_template('promote.html',  user = user, employees = employees)
    else:
        return redirect(url_for('login'))


@app. route("/promotetoadmin/<int:empid>")
def promotetoadmin(empid):
    user = get_current_user()
    db = get_db()
    db.execute('UPDATE Accounts SET admin = 1 WHERE AccountsID = ?', [empid])
    db.commit()
    return redirect(url_for('promote'))


@app. route("/revoke/ <int:empid>")
def revoke(empid):
    user = get_current_user()
    db = get_db()
    db.execute('UPDATE Accounts SET admin = 0 WHERE AccountsID = ?', [empid])
    db.commit()
    return redirect(url_for('promote'))


@app. route ("/deleteuser/ <int:empid>")
def deleteuser(empid):
    user = get_current_user()
    db = get_db()
    db.execute('DELETE FROM Accounts WHERE AccountsID = ?', [empid])
    db.commit()
    return redirect(url_for('promote'))


@app. route ("/logout")
def logout():
    session.pop('logged_in' , None)
    return redirect(url_for ("splash"))


@app.route('/upload', methods=['GET','POST'])
def upload_file():
    # Check if a valid login exists and adds security to the upload page
    if 'logged_in' in session and session['logged_in']:
        filename = None
        if 'file' in request.files:
            file = request.files['file']
            filename = secure_filename(file.filename)
                # Here you should save the file
            file.save(os.path.join("uploads/", filename))
        
        return render_template('upload_form.html', filename=filename) 
    else:

        return redirect(url_for('login'))
        


def main():
    app.run(debug=True)
    print("Code Stopped")


main()
print("Bye")

    


