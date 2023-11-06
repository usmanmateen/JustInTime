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
        user_cursor = db.execute("select * from Accounts where username = ?", [user])
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
        #hashed_password = encrypt(password)

        if check_username_password(username_upper, password):
            session['user'] = username_upper
            return redirect(url_for("home"))
        else:
            error = "Incorrect username or password"
            print("Incorrect username or password")
            print(password)

        print(f'Username is {username} and Password is {password}')

        #code = hashed.login(username, password)
        #print(f'State Code is {code}')
        

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

        role_cursor = get_users().execute("SELECT RoleID FROM Roles WHERE Role = ?", [role])
        role_id = role_cursor.fetchone()

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
            get_users().execute("INSERT INTO Accounts (Username, Password, Role, Admin, RoleID) VALUES (?, ?, ?, ?, ?)", [username_upper, hashed_password, role, admin, role_id[0]])
            get_users().commit()

        # Redirect to the login page after registration
        return redirect(url_for('login'))

    return render_template('register.html')


@app. route ("/promote")
def promote():
    user = get_current_user()
    db = get_users()
    
    all_entries_cursor = db.execute('SELECT * FROM Accounts')
    employees = all_entries_cursor.fetchall()
    
    return render_template('promote.html', user = user, employees = employees)


@app. route("/promotetoadmin/<int:empid>")
def promotetoadmin(empid):
    user = get_current_user()
    db = get_users()
    db.execute('UPDATE Accounts SET admin = 1 WHERE AccountsID = ?', [empid])
    db.commit()
    return redirect(url_for('promote'))


@app. route("/revoke/ <int:empid>")
def revoke(empid):
    user = get_current_user()
    db = get_users()
    db.execute('UPDATE Accounts SET admin = 0 WHERE AccountsID = ?', [empid])
    db.commit()
    return redirect(url_for('promote'))


@app. route ("/deleteuser/ <int:empid>")
def deleteuser(empid):
    user = get_current_user()
    db = get_users()
    db.execute('DELETE FROM Accounts WHERE AccountsID = ?', [empid])
    db.commit()
    return redirect(url_for('promote'))


@app. route ("/logout")
def logout():
    session.pop('user' , None)
    return redirect(url_for ("splash"))


@app.route('/upload', methods=['GET','POST'])
def upload_file():
    filename = None
    if 'file' in request.files:
        file = request.files['file']
        filename = secure_filename(file.filename)
        # Here you should save the file
        file.save(os.path.join("uploads/", filename)) ## Saves the file to uploads/ 

        print('File uploaded successfully')

    return render_template('upload_form.html', filename=filename)


def main():
    app.run(debug=True)
    print("Code Stopped")


main()
print("Bye")

    
