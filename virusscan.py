from flask import Flask, request, jsonify, render_template, redirect, url_for, session
from werkzeug.utils import secure_filename
import subprocess
import os

def namecheck(filename):

    extensions = {'txt', 'pdf', 'png', 'jpg', 'jpeg'}
    extension = filename.rsplit('.',1)[1].lower()
    return extension in extensions

print(namecheck("test.gif"))


def scan_file(filepath):
    try:
        result = subprocess.check_output(['clamscan', '--no-summary', filepath])
        result = result.decode('utf-8').strip()
        if "Infected files: 0" in result:
            return True, "File is clean."
        else:
            return False, "Virus detected: " + result
    except subprocess.CalledProcessError as e:
        return False, "Error during virus scan: " + str(e)




def change_hosts():
    
    command = 'powershell -Command "(Get-Content C:\\Windows\\System32\\drivers\\etc\\hosts) -replace \'127.0.0.1\s+localhost\', \'127.0.0.1 floatfry.com\' | Set-Content C:\\Windows\\System32\\drivers\\etc\\hosts"'
    subprocess.run(["powershell.exe", "-Command", command], shell=True)

def restore_host():
    
    command = 'powershell -Command "(Get-Content C:\\Windows\\System32\\drivers\\etc\\hosts) -replace \'127.0.0.1\s+floatfry.com\', \'127.0.0.1 localhost\' | Set-Content C:\\Windows\\System32\\drivers\\etc\\hosts"'
    subprocess.run(["powershell.exe", "-Command", command], shell=True)


@app.before_request
def modify_host():
    if not hasattr(request, 'seen'):
        request.seen = True
        current_os = platform.system()
        if current_os == 'Windows':
            change_hosts()


@app.teardown_request
def restoreHostsDefault(exception=None):
    current_os = platform.system()
    if current_os == 'Windows':
        restore_host()


        
