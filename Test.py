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
import subprocess
import platform

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
    db = get_db()
    if 'logged_in' in session and session['logged_in']:
        all_entries_cursor = db.execute('SELECT * FROM Orders')
        orders = all_entries_cursor.fetchall()
        image = os.path.join('graphs/','sales_graph.png')
        print(image)
        sales_image = url_for('get_sales_image')
        orders_image = url_for('get_orders_image')
        materials_image = url_for('get_materials_image')
        products_image = url_for('get_products_image')
        return render_template('home.html', user = user, orders= orders, sales_image = sales_image, orders_image = orders_image,materials_image = materials_image, products_image = products_image)
    else:
        return redirect(url_for('login'))
    
@app.route('/salesimage')
def get_sales_image():
    path = os.path.join('graphs/','sales_graph.png')  
    return send_file(path, mimetype='image/png')

@app.route('/ordersimage')
def get_orders_image():
    path = os.path.join('graphs/','order_graph.png')  
    return send_file(path, mimetype='image/png')

@app.route('/materialsimage')
def get_materials_image():
    path = os.path.join('graphs/','materials_pie_day.png')  
    return send_file(path, mimetype='image/png')

@app.route('/productsimage')
def get_products_image():
    path = os.path.join('graphs/','products_chart.png')  
    return send_file(path, mimetype='image/png')    


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
    from OTP import send_OTP
    error = None
    if request.method == 'POST':
        # Retrieve info from the registration form
        username = request.form['username']
        username_upper = username.upper()
        password = request.form['password']
        role = request.form['role']
        role = role.upper().replace(" ", "")
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
            # Store user info in a session
            session['userinfo'] = {
                'firstname': firstname,
                'lastname': lastname,
                'contact': contact,
                'email': email,
                'username': username_upper,
                'password': hashed_password,
                'role': role,
                'admin': admin,
            }
            send_OTP(contact)
            return redirect(url_for('verify_otp'))



    return render_template('register.html')

@app.route('/verify_otp', methods=['GET', 'POST'])
def verify_otp():
    from OTP import checks_OTP
    error = None
    if request.method == 'POST':
        otp_code = request.form.get('otp_code')
        userinfo = session.get('userinfo')

        contact = userinfo.get('contact', None)
        verification_status = checks_OTP(contact, otp_code)
        
        if verification_status == 'approved':
                
                employeedata(userinfo['firstname'], userinfo['lastname'], userinfo['contact'], userinfo['email'], userinfo['username'])
                accountsdata(userinfo['username'], userinfo['password'], userinfo['role'], userinfo['admin'], roleID(userinfo['role']), employeeID(userinfo['username']))
               
                session.pop('userinfo', None)

                return redirect(url_for('login'))  
        else:
              
                error = "Invalid OTP. Please try again."
                return render_template('verify_otp.html', error=error)


    return render_template('verify_otp.html')

@app.route('/Products')
def products():
    user = get_current_user()
    db = get_db()
    if 'logged_in' in session and session['logged_in'] and user['RoleID'] in [2,4,5]:
        all_entries_cursor = db.execute('SELECT * FROM Products')
        products = all_entries_cursor.fetchall()
        
        return render_template('products.html',  user = user, products = products)
    else:
        return redirect(url_for('login'))

@app.route('/Suppliers')
def suppliers():
    user = get_current_user()
    db = get_db()
    if 'logged_in' in session and session['logged_in'] and user['RoleID'] in [2,4,5]:
        all_entries_cursor = db.execute('SELECT * FROM Suppliers')
        suppliers = all_entries_cursor.fetchall()
        
        return render_template('suppliers.html',  user = user, suppliers = suppliers)
    else:
        return redirect(url_for('login'))

@app.route('/Materials')
def materials():
    user = get_current_user()
    db = get_db()
    if 'logged_in' in session and session['logged_in'] and user['RoleID'] in [2,4,5]:
        all_entries_cursor = db.execute('SELECT * FROM Materials')
        materials = all_entries_cursor.fetchall()
        
        return render_template('materials.html',  user = user, materials = materials )
    else:
        return redirect(url_for('login'))


@app.route('/Sales')
def sales():
    user = get_current_user()
    db = get_db()
    if 'logged_in' in session and session['logged_in'] and user['RoleID'] in [2,3,4,5]:
        all_entries_cursor = db.execute('SELECT * FROM Sales')
        sales = all_entries_cursor.fetchall()
        
        return render_template('sales.html',  user = user, sales = sales)
    else:
        return redirect(url_for('login'))

@app.route('/Shipments')
def shipments():
    user = get_current_user()
    db = get_db()
    if 'logged_in' in session and session['logged_in'] and user['RoleID'] in [1,2,3,4,5]:
        all_entries_cursor = db.execute('SELECT * FROM Shipments')
        shipments = all_entries_cursor.fetchall()
        
        return render_template('shipments.html',  user = user, shipments = shipments)
    else:
        return redirect(url_for('login'))

@app.route('/Orders')
def orders():
    user = get_current_user()
    db = get_db()
    if 'logged_in' in session and session['logged_in'] and user['RoleID'] in [1,2,3,4,5]:
        all_entries_cursor = db.execute('SELECT * FROM Orders')
        orders = all_entries_cursor.fetchall()
        
        return render_template('orders.html',  user = user, orders = orders)
    else:
        return redirect(url_for('login'))


@app. route("/udatestatus/<int:ordid>")
def update(ordid):
    user = get_current_user()
    db = get_db()
    order = db.execute('SELECT * FROM Orders WHERE OrderID = ?', [ordid]).fetchone()

    if order:
        current_status = order['OrderStatus']


        # Check for status transitions based on the current status
        if current_status == 'Shipped':
            db.execute('UPDATE Orders SET OrderStatus = ? WHERE OrderID = ?', ['Delivered', ordid])
            db.commit()
            return redirect(url_for('orders'))
        elif current_status == 'Processing':
            db.execute('UPDATE Orders SET OrderStatus = ? WHERE OrderID = ?', ['Shipped', ordid])
            db.commit()
            return redirect(url_for('orders'))
        else:
            
            return redirect(url_for('orders'))



@app.route('/contact', methods=['GET', 'POST'])
def contact():
    user = get_current_user()
    if 'logged_in' in session and session['logged_in']:
        if request.method == 'POST':
            name = request.form['name']
            email = request.form['email']
            message = request.form['message']

            print(f"Received message from: {name}, Email: {email}, Message: {message}")
        
        return render_template('contact.html', user = user)
    else:
        return redirect(url_for('login'))

@app. route ("/promote")
def promote():
    user = get_current_user()
    db = get_db()
    if 'logged_in' in session and session['logged_in'] and user[ 'admin'] == 1:
        all_entries_cursor = db.execute('SELECT * FROM Accounts')
        employees = all_entries_cursor.fetchall()
        print(all_entries_cursor)
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
    user = get_current_user()
    # Check if a valid login exists and adds security to the upload page
    if 'logged_in' in session and session['logged_in']:
        filename = None
        if 'file' in request.files:
            file = request.files['file']
            filename = secure_filename(file.filename)
                # Here you should save the file
            file.save(os.path.join("uploads/", filename))
        
        return render_template('upload_form.html', filename=filename, user = user) 
    else:

        return redirect(url_for('login'))
        

@app.route('/viewPrinter', methods=['GET','POST'])
def viewPrinter():
    user = get_current_user()
    if 'logged_in' in session and session['logged_in']:
        from printer_test import cleanMac, printer_status
        data = printer_status()
        
        return render_template('viewPrinter.html', user = user, dataToRender = data, len = len(data) )
    else:
        from printer_test import cleanMac, printer_status
        data = printer_status()
        
        return render_template('viewPrinter.html', user = user, dataToRender = data, len = len(data) )
        #return redirect(url_for('login'))

@app.route ('/uploadList', methods=['GET','POST'])
def uploadlist():
    user = get_current_user()
    if 'logged_in' in session and session['logged_in'] and user['RoleID'] in [1,2,3,4,5]:
        uploads_folder = 'uploads' 
        files = {}
        for filename in os.listdir(uploads_folder):
            file_path = os.path.join(uploads_folder, filename)
            if os.path.isfile(file_path):
                files[filename] = os.path.getsize(file_path)
                print(files[filename])
                    
        return render_template('UploadList.html', filenames=files, length = len(files), user = user)
    else:
        return redirect(url_for('login'))
    
    

@app.route('/Print/<string:filename>')
def print(filename):
    from printer_test import doc_to_print
    doc_to_print(filename)
    
    return redirect(url_for('uploadlist'))
        





def main():
    app.run(debug=True)
    print("Code Stopped")

if __name__ == '__main__':
    main()
    print("Bye")

    


