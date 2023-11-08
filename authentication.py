from hashed import encrypt
from users_database import get_db

def check_username_password(username, password):
    db = get_db()
    user = db.execute('SELECT * FROM Accounts WHERE username = ? ', (username,)).fetchone()

    if user and user['password'] == encrypt(password):
        return True
    else:
        return False

def check_username(username):
    db = get_db()
    user = db.execute('SELECT * FROM Accounts WHERE username = ? ', (username,)).fetchone()

    if user:
        return True
    else:
        return False
