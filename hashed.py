
import hashlib  # this allow me to hash my passwords
from users_database import get_users
def readtextfile(filename):
    splitedline = []

    file = open(filename, 'r')
    for each in file.readlines():
        txt_line = each.split(',')
        splitedline.append(txt_line)

    file.close()  # closing the file to ensure file is accessible and not locked.  
    return splitedline

    pass


def encrypt(value="0"):
    #  SHA256 to MD5# x2 then SHA256
    hash_password = hashlib.sha256(value.encode())  
    temp_hash = hash_password.hexdigest()

    hash_pt2 = hashlib.md5(temp_hash.encode())
    temp_hash = hash_pt2.hexdigest()

    hash_pt3 = hashlib.md5(temp_hash.encode())
    temp_hash = hash_pt3.hexdigest()

    hash_pt4 = hashlib.sha256(temp_hash.encode())
    final_hash = hash_pt4.hexdigest()

    return final_hash

def registation(username="admin", password="admin", role="stamper" ):  # Registation Default is admin,admin. 
    # Need to check if username exists; If it does return error code (-1) . 
    # # As the DB has not been made - Using a Txt file 

    db = get_users()

    check_username = db.execute('SELECT * FROM users WHERE username = ?', (username,)).fetchone()
    if check_username:
        return -1 

    hashed_password = encrypt(password)  # Use your custom encrypt function
    role = None

    db.execute('INSERT INTO users (username, password) VALUES (?, ?)', [username, hashed_password])

    db.commit()

    return 0


def login(username="admin", password="admin"):  # this the login subroutine
    
    # Need to check if username exists; If it does return error code (-1) . 
    # # As the DB has not been made - Using a Txt file 

    db = get_users()    
    # Check if the username exists in the database
    user_data = db.execute('SELECT username, password FROM users WHERE username = ?', (username,)).fetchone()
    if user_data is None:
        return -1  # Username does not exist
    
    hash_value = encrypt(password)
    
    hashed_password = encrypt(password)  # Use your custom encrypt function
    if hashed_password == user_data['password']:
        return 1  # Login successful
    else:
        return 0  # Incorrect password




