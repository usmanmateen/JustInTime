import platform
import os

system_types = {
    "linux":0,
    "windows":1
}

def check_os():
    return system_types.get(platform.system().lower(),-1)


def linux_printer(filename,printer_name=None):
    import subprocess
    try: 
        if printer_name:
            # pecify a specific printer, use the lpr command with the printer name
            subprocess.run(['lpr', '-P', printer_name, filepath(filename)])
        else: # default Printer 
            subprocess.run(['lpr', filepath(filename)])

        return "File sent to printer."
    except Exception as e:
        return e



def filepath(filename):
    path = f'{os.path.dirname(os.path.abspath(__file__))}\\uploads\\{filename}'
    return path


def windows_printer(filename):
    try:
        os.startfile(filepath(filename),'print')
        return "Sent to Printer."
    except Exception as e:
        return e



def doc_to_print(filename): ## Call the doc_to_print method which allows the user to printer. 
    machine_type = check_os()
    

    if machine_type == 1:
        status = windows_printer(filename)
    

    if machine_type == 0:
        status = linux_printer(filepath)

    return status

