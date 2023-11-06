import sqlite3 
from flask import g


def connect_database():

    sql =  sqlite3.connect("/Users/muhammadusman/Downloads/django/JustInTime/Floatfry.db")
    sql.row_factory = sqlite3.Row

    return sql

def get_users():
    
    if not hasattr(g, 'FloatFry_db'):
        g.FloatFry_db = connect_database()
    return g.FloatFry_db