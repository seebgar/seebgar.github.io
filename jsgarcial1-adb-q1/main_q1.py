import subprocess
import time

'''
Sebastian Garcia 201630047
'''

DEVICE_ID = ""
HOME_KEY_EVENT = 3
KEYBOARD_ENTER = 66
CONTACTS_PACKAGE = "com.android.contacts"
FIRST_APP_CORD_X = 120
FIRST_APP_CORD_Y = 355
WHITE_SPACE_CORD_X = 540
WHITE_SPACE_CORD_Y = 1700
LONG_WAIT = 2
SHORT_WAIT = 0.5
SEARCHBAR_CORD_X = 542
SEARCHBAR_CORD_Y = 1700

REPORT = ""
REPORT_FILE = "report_q1.html"
PLACEHOLDER = "INSERT_REPORT_HERE"


def start_process():
    # GET DEVICE ID
    set_device_id()

    '''
    1. Go to home menu and click on the frist application available on the launcher
    '''
    home()

    write_report(
        f"<br/> <br/> <p> <strong>1.</strong> &nbsp; Go to home menu</p> <br/>")
    take_screenshot("HomeScreen")

    swipe_up()
    take_screenshot("Launcher")
    perfom_tap(FIRST_APP_CORD_X, FIRST_APP_CORD_Y)  # first application
    time.sleep(LONG_WAIT)

    write_report(
        f"<br/> <br/> <p> <strong>1.1.</strong> &nbsp; Click on the first application available on the launcher</p> <br/> ")
    take_screenshot("FirstApplicationOpen")

    '''
    2. Go to the home menu and long tap the first 3 apps available on the launcher
    '''
    home()
    swipe_up()

    write_report(
        f"<br/> <br/> <p> <strong>2.</strong> &nbsp; Long tap on the frist 3 apps on the launcher</p> <br/> ")

    perfom_long_tap(FIRST_APP_CORD_X, FIRST_APP_CORD_Y)
    take_screenshot("FirstLongTap")

    perfom_tap(WHITE_SPACE_CORD_X, WHITE_SPACE_CORD_Y)  # white space
    perfom_long_tap(FIRST_APP_CORD_X + 220, FIRST_APP_CORD_Y)
    take_screenshot("SecondLongTap")

    perfom_tap(WHITE_SPACE_CORD_X, WHITE_SPACE_CORD_Y)  # white space
    perfom_long_tap(FIRST_APP_CORD_X + 220 + 220, FIRST_APP_CORD_Y)
    take_screenshot("ThirdLongTap")

    home()

    '''
    3. Verify the device's current WiFi status (on/off)
    '''
    wifi_status()

    write_report(f"<br/> <br/> <p> <strong>3.</strong> &nbsp; Verify WiFi status - ADB checks the status and then prints the result on Google Search Bar.</p> <br/>")
    take_screenshot("WIFI-Status")

    home()

    '''
    4. Verify if the device is in airplane mode
    '''
    airplane_mode_status()

    write_report(f"<br/> <br/> <p> <strong>4.</strong> &nbsp; Verify Airplane Mode status -  ADB checks the status and then prints the result on Google Search Bar </p> <br/>")
    take_screenshot("AirPlaneMode-Status")

    home()

    '''
    5. Launch the contacts app and add a new contact to the contact's list
    '''
    start_package(CONTACTS_PACKAGE)
    time.sleep(LONG_WAIT)

    write_report(
        f"<br/> <br/> <p> <strong>5.</strong> &nbsp;Launch Contacts App</p>")
    take_screenshot("ContactsApp")

    add_contact()  # screen shot made inside function
    home()

    start_package(CONTACTS_PACKAGE)  # show list of contacts
    time.sleep(LONG_WAIT)
    take_screenshot("ContactsList")

    time.sleep(LONG_WAIT)
    home()

    write_report(
        f"<br/> <br/> <p> <strong>Executed using Python 3.7.4</strong> </p>")
    write_report(
        "<p>Android Debug Bridge version 1.0.41 <br/>Version 29.0.6-6198805 <br/>Installed as /usr/local/bin/adb</p>")
    write_on_file(REPORT_FILE, REPORT)


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


def set_device_id():
    cmd = f"adb devices"
    process = execute_process(cmd, "Device ID")
    global DEVICE_ID
    DEVICE_ID = "-s " + process.split()[4]
    write_report(f"<p> Device ID: {DEVICE_ID[3:]} </p>")


def perfom_keyevent(for_key):
    cmd = f"adb {DEVICE_ID} shell input keyevent {for_key}"
    execute_process(cmd, "Home Key Event")


def home():
    # PERFORM HOME HEY EVENT
    perfom_keyevent(HOME_KEY_EVENT)
    time.sleep(SHORT_WAIT)


def swipe_up():
    (coordX1, coordY1) = (400, 880)
    (coordX2, coordY2) = (400, 50)
    milliseconds = 180
    cmd = f"adb {DEVICE_ID} shell input swipe {coordX1} {coordY1} {coordX2} {coordY2} {milliseconds}"
    execute_process(cmd, "Swipe Up")
    time.sleep(SHORT_WAIT)


def custom_swipe_up(coordX1, coordY1, coordX2, coordY2):
    milliseconds = 180
    cmd = f"adb {DEVICE_ID} shell input swipe {coordX1} {coordY1} {coordX2} {coordY2} {milliseconds}"
    execute_process(cmd, "Swipe Up")
    time.sleep(SHORT_WAIT)


def perfom_tap(coordX, coordY):
    cmd = f"adb {DEVICE_ID} shell input tap {coordX} {coordY}"
    process = execute_process(cmd, f"Tap ({coordX}, {coordY})")
    time.sleep(SHORT_WAIT)


def perfom_long_tap(coordX, coordY):
    milliseconds = 1200  # 1.2 seg
    cmd = f"adb {DEVICE_ID} shell input swipe {coordX} {coordY} {coordX} {coordY} {milliseconds}"
    execute_process(cmd, f"Long tap ({coordX}, {coordY})")
    time.sleep(SHORT_WAIT)


def wifi_status():
    cmd = f"adb {DEVICE_ID} shell dumpsys wifi | grep 'Wi-Fi is'"
    process = execute_process(cmd, "WiFi Status")
    home()
    time.sleep(SHORT_WAIT)
    perfom_tap(SEARCHBAR_CORD_X, SEARCHBAR_CORD_Y)  # google search bar
    time.sleep(SHORT_WAIT)
    cmd = f"adb {DEVICE_ID} shell \"input keyboard text '{process}'\""
    execute_process(cmd, "Inserting Input with Wifi Status")
    time.sleep(LONG_WAIT)


def airplane_mode_status():
    cmd = f"adb {DEVICE_ID} shell dumpsys wifi | grep 'mAirplaneModeOn' "
    process = execute_process(cmd, "Airplane Mode Status")
    home()
    time.sleep(SHORT_WAIT)
    perfom_tap(SEARCHBAR_CORD_X, SEARCHBAR_CORD_Y)  # google search bar
    time.sleep(SHORT_WAIT)
    cmd = f"adb {DEVICE_ID} shell \"input keyboard text '{process}'\""
    execute_process(cmd, "Inserting Input with Airplane Mode Status")
    time.sleep(LONG_WAIT)


def start_package(package_name):
    cmd = f"adb {DEVICE_ID} shell monkey -p {package_name} -c android.intent.category.LAUNCHER 1"
    try:
        stop_package(CONTACTS_PACKAGE)
        execute_process(cmd, "Launch Contacts App")
    except:
        pass


def add_contact():
    time.sleep(SHORT_WAIT)
    perfom_tap(950, 1684)  # add button

    # perfom_tap(556, 1047) # add google account alert  -> cancel

    cmd = f"adb {DEVICE_ID} shell \"input keyboard text 'Sebastian'\""
    execute_process(cmd, "Inserting Contact First Name")

    time.sleep(SHORT_WAIT)
    write_report(
        "<br/> <br/> <p> <strong>4.1.</strong> &nbsp; Add Contact</p>")
    take_screenshot("Added")

    perfom_keyevent(KEYBOARD_ENTER)

    cmd = f"adb {DEVICE_ID} shell \"input keyboard text 'Garcia'\""
    execute_process(cmd, "Inserting Contact Last Name")

    perfom_keyevent(KEYBOARD_ENTER)

    cmd = f"adb {DEVICE_ID} shell \"input keyboard text '3901234567'\""
    execute_process(cmd, "Inserting Contact Phone")

    perfom_tap(990, 135)  # save button
    time.sleep(LONG_WAIT)


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
        # placeholder on HTML file to replace with report
        data = data.replace(PLACEHOLDER, a_string)

    with open(with_name, 'wt') as website:
        website.write(data)


def take_screenshot(capture_name):
    cmd = f"adb {DEVICE_ID} shell screencap /sdcard/{capture_name}.png"
    execute_process(cmd, f"Taking Screenshot {capture_name}")
    time.sleep(SHORT_WAIT)

    local_image_file = f"images/{capture_name}.png"
    cmd = f"adb {DEVICE_ID} pull /sdcard/{capture_name}.png {local_image_file}"
    process = execute_process(cmd, f"Recovering Screenshot {capture_name}")

    write_report(
        f" <img src=\"{local_image_file}\"  alt=\"{capture_name}\" height=300 /> ")


def write_report(text):
    global REPORT
    REPORT += text


if __name__ == "__main__":
    start_process()
