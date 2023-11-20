import platform
import os

system_types = {
    "linux":0,
    "windows":1
}

def check_os():
    return system_types.get(platform.system().lower(),-1)






def filepath(filename):
    path = f"{os.path.dirname(os.path.abspath(__file__))}\\uploads\\{filename}"
    return path


def windows_printer(filename):
    try:
        os.startfile(filepath(filename),'print')
        return "Sent to Printer."
    except Exception as e:
        return e
        
def linux_printer(filename,printer_name=None):
    import subprocess
    try: 
        if printer_name:
            # Specify a specific printer, use the lpr command with the printer name
            subprocess.run(['lpr', '-P', printer_name, filepath(filename)])
        else: # default Printer 
            subprocess.run(['lpr', filepath(filename)])

        return "File sent to printer."
    except Exception as e:
        return e


def doc_to_print(filename = None): ## Call the doc_to_print method which allows the user to printer. 
    machine_type = check_os()
    
    if filename == None or " ":
        return "No File Given"

    if machine_type == 1:
        status = windows_printer(filename)
    

    if machine_type <= 0:
        status = linux_printer(filepath)

    return status




def linux_get_device_status():
    import subprocess
    try: 
        # Specify a specific printer, use the lpr command with the printer name
        status = subprocess.run(['lpstat', '-p'], capture_output=True)
        print(status)

 
        return status
    except Exception as e:
        return e    



def windows_get_printer_status():
    # Run the WMIC command to get printer status
    command = 'wmic printer list brief'
    result = os.popen(command).read()
    print("Printer Status:")
    return (result)

def windows_get_device_status():
    # Run the WMIC command to get device status
    command = 'wmic logicaldisk get caption,description'
    result = os.popen(command).read()
    print("Device Status:")
    print(result)

    return result


def printer_status():
    machine_type = check_os()

    if machine_type == 1:
        status = windows_get_printer_status()

    if machine_type <= 0:
        status = linux_get_device_status()

    status= str(status)

    status = status.split("\n")
    

    for each in status:
        if each == "":
            status.remove(each)
    

    return status


x = printer_status()[0]
print(x)
