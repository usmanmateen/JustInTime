import sqlite3 
from flask import g
import os

def connect_database():
    db_filename = 'FloatFry.db'

    sql =sqlite3.connect(os.path.join('database/', "FloatFry.db"))
   
    sql.row_factory = sqlite3.Row
    return sql

def get_db():
    
    if not hasattr(g, 'FloatFry_db'):
        g.FloatFry_db = connect_database()
    return g.FloatFry_db
