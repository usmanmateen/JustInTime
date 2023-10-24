
import hashlib  # this allow me to hash my passwords

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

def registation(username="admin", password="admin"):  # Registation Default is admin,admin. 
    
    # Need to check if username exists; If it does return error code (-1) . 
    # # As the DB has not been made - Using a Txt file 

    
    accounts = readtextfile('Database/account.txt')
    for each in accounts:
        if each[0].lower() == username.lower():
            return (-1)
    
    hash_value = encrypt(password)

    value = f'{username},{hash_value}'
    f = open('Database/account.txt', 'a+')
    f.write(value)
    f.close()

    return 0


def login(username="admin", password="admin"):  # this the login subroutine
    
    # Need to check if username exists; If it does return error code (-1) . 
    # # As the DB has not been made - Using a Txt file 

    accounts = readtextfile('Database/account.txt')
    state = False

    for each in accounts:
        if each[0].lower() == username:
            state = True

            break

    if state == False:
        return 0
    
    hash_value = encrypt(password)

    if hash_value == each[1]:
        return 1
    else:
        return -1 




