from users_database import get_db
from authentication import check_username_password, check_username
from flask import Flask, render_template, request, session, redirect, url_for
import os


def employeedata(firstname, lastname, contact, email, username ):
   
    get_db().execute('INSERT INTO Employees (FirstName, LastName, ContactNumber, Email, Username) VALUES (?,?,?,?,?) ', [firstname, lastname, contact, email, username])     
    get_db().commit()

def accountsdata(username_upper, hashed_password, role, admin, role_id, employee_id):
    get_db().execute("INSERT INTO Accounts (Username, Password, Role, Admin, RoleID, EmployeeID) VALUES (?, ?, ?, ?, ?, ?)", [username_upper, hashed_password, role, admin, role_id[0], employee_id[0]])
    get_db().commit()

