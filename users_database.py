import sqlite3 
from flask import g


def connect_database():

    sql =  sqlite3.connect("/Users/muhammadusman/Downloads/django/JustInTime/accounts.db")
    sql.row_factory = sqlite3.Row

    return sql

def get_users():
    
    if not hasattr(g, 'accounts_db'):
        g.accounts_db = connect_database()
    return g.accounts_db