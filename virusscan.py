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
