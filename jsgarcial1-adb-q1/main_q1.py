import subprocess
import time

'''
Sebastian Garcia 201630047
'''

DEVICE_ID = ""
HOME_KEY_EVENT = 3
KEYBOARD_ENTER = 66
CONTACTS_PACKAGE = "com.android.contacts"
REPORT = ""
REPORT_FILE = "report_q1.html"


def execute_process(cmd, process_name):
    process = subprocess.Popen(
        [cmd], shell=True, stdout=subprocess.PIPE, stderr=subprocess.PIPE)
    (output, error) = process.communicate()
    if error:
        raise Exception(
            f"*--> Error Catched at {process_name}::\n{str(error.decode('utf-8'))}")
    else:
        message = "Done" if len(str(output.decode(
            'utf-8'))) <= 0 else str(output.decode('utf-8')[:100] + "\n(...)")
        print(f"--> {process_name} ::\n{message}")

    return str(output.decode('utf-8'))


def start_process():
    # GET DEVICE ID
    cmd = f"adb devices"
    process = execute_process(cmd, "Device ID")
    global DEVICE_ID
    DEVICE_ID = "-s " + process.split()[4]

    global REPORT
    REPORT += f"<p> Device ID: {DEVICE_ID[3:]} </p>"  

    '''
    1. Go to home menu and click on the frist application available on the launcher
    '''
    REPORT += f"<br/> <br/> <p> <strong>1.</strong> &nbsp; Go to home menu</p> <br/> " 
    home()
    take_screenshot("HomeScreen")

    REPORT += f"<br/> <br/> <p> <strong>1.1.</strong> &nbsp; Click on the frist application available on the launcher</p> <br/> "
    swipe_up()
    take_screenshot("Launcher")
    perfom_tap(120, 355)  # first application
    time.sleep(2)
    take_screenshot("FirstApplicationOpen")

    '''
    2. Go to the home menu and long tap the first 3 apps available on the launcher
    '''
    home()
    swipe_up()
    REPORT += f"<br/> <br/> <p> <strong>2.</strong> &nbsp; Long tap on the frist 3 apps on the launcher</p> <br/> "
    perfom_long_tap(120, 355)
    take_screenshot("FirstLongTap")
    perfom_tap(540, 1700)  # white space
    perfom_long_tap(120 + 220, 355)
    take_screenshot("SecondLongTap")
    perfom_tap(540, 1700)  # white space
    perfom_long_tap(120 + 220 + 220, 355)
    take_screenshot("ThirdLongTap")
    home()

    '''
    3. Verify the device's current WiFi status (on/off)
    '''
    wifi_status()
    REPORT += f"<br/> <br/> <p> <strong>3.</strong> &nbsp; Verify WiFi status - ADB checks the status and then prints the result on Google Search Bar.</p> <br/>"
    take_screenshot("WIFI-Status")
    home()

    '''
    4. Verify if the device is in airplane mode
    '''
    airplane_mode_status()
    REPORT += f"<br/> <br/> <p> <strong>4.</strong> &nbsp; Verify Airplane Mode status -  ADB checks the status and then prints the result on Google Search Bar </p> <br/>"
    take_screenshot("AirPlaneMode-Status")
    home()

    '''
    5. Launch the contacts app and add a new contact to the contact's list
    '''
    REPORT += f"<br/> <br/> <p> <strong>5.</strong> &nbsp;Launch Contacts App</p>"
    start_package(CONTACTS_PACKAGE)
    time.sleep(2)
    take_screenshot("ContactsApp")
    add_contact() # screen shot make inside function
    home()
    start_package(CONTACTS_PACKAGE)  # show list of contacts
    time.sleep(2)
    take_screenshot("ContactsList")
    time.sleep(2)
    home()

    REPORT += f"<br/> <br/> <p> <strong>Executed using Python 3.7.4</strong> </p>"

    write_on_file(REPORT_FILE, REPORT)


def perfom_keyevent(for_key):
    cmd = f"adb {DEVICE_ID} shell input keyevent {for_key}"
    execute_process(cmd, "Home Key Event")


def home():
    # PERFORM HOME HEY EVENT
    perfom_keyevent(HOME_KEY_EVENT)
    time.sleep(0.3)


def swipe_up():
    (coordX1, coordY1) = (400, 880)
    (coordX2, coordY2) = (400, 50)
    milliseconds = 180
    cmd = f"adb {DEVICE_ID} shell input swipe {coordX1} {coordY1} {coordX2} {coordY2} {milliseconds}"
    execute_process(cmd, "Swipe Up")
    time.sleep(1)


def custom_swipe_up(coordX1, coordY1, coordX2, coordY2):
    milliseconds = 180
    cmd = f"adb {DEVICE_ID} shell input swipe {coordX1} {coordY1} {coordX2} {coordY2} {milliseconds}"
    execute_process(cmd, "Swipe Up")
    time.sleep(1)


def perfom_tap(coordX, coordY):
    cmd = f"adb {DEVICE_ID} shell input tap {coordX} {coordY}"
    process = execute_process(cmd, f"Tap ({coordX}, {coordY})")
    time.sleep(0.3)


def perfom_long_tap(coordX, coordY):
    milliseconds = 1200  # 1.2 seg
    cmd = f"adb {DEVICE_ID} shell input swipe {coordX} {coordY} {coordX} {coordY} {milliseconds}"
    execute_process(cmd, f"Long tap ({coordX}, {coordY})")
    time.sleep(0.3)


def wifi_status():
    cmd = f"adb {DEVICE_ID} shell dumpsys wifi | grep 'Wi-Fi is'"
    process = execute_process(cmd, "WiFi Status")
    home()
    time.sleep(0.3)
    perfom_tap(542, 1700)  # google search bar
    time.sleep(1)
    cmd = f"adb {DEVICE_ID} shell \"input keyboard text '{process}'\""
    execute_process(cmd, "Inserting Input with Wifi Status")
    time.sleep(2)


def airplane_mode_status():
    cmd = f"adb {DEVICE_ID} shell dumpsys wifi | grep 'mAirplaneModeOn' "
    process = execute_process(cmd, "Airplane Mode Status")
    home()
    time.sleep(0.3)
    perfom_tap(542, 1700)  # google search bar
    time.sleep(1)
    cmd = f"adb {DEVICE_ID} shell \"input keyboard text '{process}'\""
    execute_process(cmd, "Inserting Input with Airplane Mode Status")
    time.sleep(2)


def start_package(package_name):
    cmd = f"adb {DEVICE_ID} shell monkey -p {package_name} -c android.intent.category.LAUNCHER 1"
    try:
        stop_package(CONTACTS_PACKAGE)
        execute_process(cmd, "Launch Contacts App")
    except:
        pass


def add_contact():
    time.sleep(1)
    perfom_tap(950, 1684)  # add button

    # perfom_tap(556, 1047) # add google account alert  -> cancel

    cmd = f"adb {DEVICE_ID} shell \"input keyboard text 'Sebastian'\""
    execute_process(cmd, "Inserting Contact First Name")

    time.sleep(1)
    global REPORT
    REPORT += f"<br/> <br/> <p> <strong>4.1.</strong> &nbsp; Add Contact</p>"
    take_screenshot("Added")

    perfom_keyevent(KEYBOARD_ENTER)

    cmd = f"adb {DEVICE_ID} shell \"input keyboard text 'Garcia'\""
    execute_process(cmd, "Inserting Contact Last Name")

    perfom_keyevent(KEYBOARD_ENTER)

    cmd = f"adb {DEVICE_ID} shell \"input keyboard text '3901234567'\""
    execute_process(cmd, "Inserting Contact Last Name")

    perfom_tap(990, 135)  # save button
    time.sleep(2)


def stop_package(package_name):
    cmd = f"adb {DEVICE_ID} shell am force-stop {package_name}"
    try:
        execute_process(cmd, "Launch Contacts App")
    except:
        pass


def write_on_file(with_name, a_string):
    data = ""
    with open(with_name, "rt") as website:
        data = website.read()
        data = data.replace("IMAGES-HERE", a_string)

    with open(with_name, 'wt') as website:
        website.write(data)

def take_screenshot(capture_name):
    cmd = f"adb {DEVICE_ID} shell screencap /sdcard/{capture_name}.png"
    execute_process(cmd, f"Taking Screenshot {capture_name}")
    time.sleep(1)

    local_image_file = f"images/{capture_name}.png"
    cmd = f"adb {DEVICE_ID} pull /sdcard/{capture_name}.png {local_image_file}"
    process = execute_process(cmd, f"Recovering Screenshot {capture_name}")

    
    global REPORT
    REPORT += f" <img src=\"{local_image_file}\"  alt=\"{capture_name}\" height=300 /> " 
    


if __name__ == "__main__":
    start_process()
