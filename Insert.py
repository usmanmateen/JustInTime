from users_database import get_db
from authentication import check_username_password, check_username
from flask import Flask, render_template, request, session, redirect, url_for
import os


def employeedata(firstname, lastname, contact, email, username ):
    get_db().execute('INSERT INTO Employees (FirstName, LastName, ContactNumber, Email, Username) VALUES (?,?,?,?,?) ', [firstname, lastname, contact, email, username])     
    get_db().commit()

def roleID(role):
    cursor = get_db().execute("SELECT RoleID FROM Roles WHERE Role = ?", [role])
    result = cursor.fetchone()
    if result:
        return result['RoleID']
    return None

def employeeID(username):
    employee_cursor = get_db().execute("SELECT EmployeeID FROM Employees WHERE Username = ?", [username])
    employee_id = employee_cursor.fetchone()
    if employee_id:
        return employee_id['EmployeeID']
    return None

def accountsdata(username_upper, hashed_password, role, admin, role_id, employee_id):
    username= username_upper.lower()
    print(username_upper, hashed_password, role, admin, role_id, employee_id)
    get_db().execute("INSERT INTO Accounts (Username, Password, Role, Admin, RoleID, EmployeeID) VALUES (?, ?, ?, ?, ?, ?)", [username_upper, hashed_password, role, admin, roleID(role), employeeID(username)])
    
    get_db().commit()
    

