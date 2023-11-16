


def namecheck(filename):
    extensions = {'txt', 'pdf', 'png', 'jpg', 'jpeg'}
    extension = filename.rsplit('.',1)[1].lower()
    return extension in extensions


    #return '.' in filename and filename.rsplit('.', 1)[1].lower() in extensions

print(namecheck("test.gif"))
