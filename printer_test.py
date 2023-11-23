
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
    
    if filename == None or filename == " ":
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



def cleanMac():
    output_list = [
    "CompletedProcess(args=['lpstat', '-p'], returncode=0, stdout=b'printer HP_DeskJet_2700_series is idle.  enabled since Sat 16 Sep 14:11:19 2023\\nprinter HP_DeskJet_2700_series__C8CAC9__20210331212431 is idle.  enabled since Fri  6 Jan 07:43:28 2023\\nprinter HP_DeskJet_3630_series is idle.  enabled since Wed 17 Mar 13:28:20 2021\\nprinter HP_DeskJet_3630_series_2 is idle.  enabled since Wed 31 Mar 21:25:12 2021\\n', stderr=b'')"
    ]


    output_string = output_list[0].split("stdout=b'")[1].split("', stderr=b'")[0]
    printer_statuses = output_string.split('\\n')

    cleaned_printers = []
    for status in printer_statuses:
        if status:
            parts = status.split(' is ')
            if len(parts) == 2:
                printer_name = parts[0].split('printer ')[1]
                printer_status = parts[1].split('.')[0].strip()
                cleaned_printers.append({'printer_name': printer_name, 'printer_status': printer_status})

    # Returning the entire cleaned_printers list as an array
    return cleaned_printers





def printer_status():
    machine_type = check_os()

    if machine_type == 1:
        status = windows_get_printer_status()

    if machine_type == 0:
        status = linux_get_device_status()

    if machine_type <0:
        return cleanMac()

    status= str(status)

    status = status.split("\n")
    
        

    for each in status:
        if each == "":
            status.remove(each)
    
    try:
        status = status.split("\n")
    except Exception as e:
        print(e)
    

    
    return status

