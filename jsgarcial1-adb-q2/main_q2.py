import subprocess
import time
from datetime import datetime


'''
Sebastian Garcia 201630047
'''

# the path is already given inside the Mac in which this program was executed.
# However, in a Windows Machine, it is required to set this variable to "cmd /C"
ADB_PATH = ""

EXTERNAL_APPLICATION_PATH = "../RollerPlanet.apk"
EXTERNAL_PACKAGE = "com.brutumFulmen.RollerPlanet"
PATH_TO_IMAGES_FOLDER = "images/"

REPORT = ""
REPORT_FILE = "report_q2.html"
# ! REPLACE BODY OF HTML FILE WITH THE STRING = INSERT_REPORT_HERE
PLACEHOLDER = "INSERT_REPORT_HERE"

# These are the CORDS for the first application in the Launcher Menu
FIRST_APP_CORD_X = 120
FIRST_APP_CORD_Y = 355
APPS_SEPARATION_PTS = 220
# This is a space inside the Launcher Menu where there are no applications.
WHITE_SPACE_CORD_X = 540
WHITE_SPACE_CORD_Y = 1700
# These are the CORDS of the default Google Searchbar at the home screen.
SEARCHBAR_CORD_X = 542
SEARCHBAR_CORD_Y = 1700

RAW_ID = "201630047"
STUDENT_ID = (int(RAW_ID) % 4 + int(RAW_ID[-1]))  # equals 10
EVENT_COUNTER = 1

DEVICE_ID = ""
HOME_KEY_EVENT = 3
BACK_KEY_EVENT = 4
KEYBOARD_ENTER = 66
# these waits are used to sleep the main thread in order to allow the emulator to react when an action is taking place
LONG_WAIT = 1.5
SHORT_WAIT = 0.3
CONTACTS_PACKAGE = "com.android.contacts"

CONTACTS_APP_ADD_BTN_CORD_X = 950
CONTACTS_APP_ADD_BTN_CORD_Y = 1684
CONTACTS_APP_SAVE_BTN_CORD_X = 990
CONTACTS_APP_SAVE_BTN_CORD_Y = 135


def start_process(n):
    set_device_id()     # the device ID is set using the command 'adb devices'

    install_application(EXTERNAL_APPLICATION_PATH)
    start_package(EXTERNAL_PACKAGE)

    write_report("""
                    <br/> <br/>
                    <p> <strong>0.</strong> &nbsp; Installing external APK</p> 
                    <br/>
                 """)
    time.sleep(LONG_WAIT*5)  # a long wait -> allows the application to launch
    take_screenshot("ExternalAPK-" + datetime.now().strftime('%M:%S.%f')[:-4])

    actions(n)

    stop_package(EXTERNAL_PACKAGE)
    uninstall_application(EXTERNAL_PACKAGE)

    write_on_file(REPORT_FILE, REPORT)


def actions(n):
    while n >= 0:
        write_report(f"<br/><br/> <h2>Iteration # {n}</h2> <hr/> ")

        '''
        1. Go to home menu and click on the frist application available on the launcher
        '''
        home()  # goes to Home Screen Menu
        time.sleep(SHORT_WAIT)

        write_report("""
                        <br/> 
                        <p> <strong>1.</strong> &nbsp; Go to home menu</p> 
                        <br/>
                    """)
        take_screenshot(
            "HomeScreen-" + datetime.now().strftime('%M:%S.%f')[:-4])

        swipe_up()  # opens Launch Menu
        take_screenshot("Launcher-" + datetime.now().strftime('%M:%S.%f')[:-4])

        # taps first application
        perfom_tap(FIRST_APP_CORD_X, FIRST_APP_CORD_Y)
        time.sleep(LONG_WAIT)

        write_report("""
                        <br/> <br/> 
                        <p> <strong>1.1.</strong> &nbsp; Click on the first application available on the launcher</p> 
                        <br/> 
                    """)
        take_screenshot("FirstApplicationOpen-" +
                        datetime.now().strftime('%M:%S.%f')[:-4])

        n -= 1
        event_counter(n)  # handles the BACK action if needed
        if n == 0:
            break

        '''
        2. Go to the home menu and long tap the first 3 apps available on the launcher
        '''
        home()
        swipe_up()

        write_report("""
                        <br/> <br/> 
                        <p> <strong>2.</strong> &nbsp; Long tap on the frist 3 apps on the launcher</p> 
                        <br/> 
                    """)

        perfom_long_tap(FIRST_APP_CORD_X, FIRST_APP_CORD_Y)
        take_screenshot("FirstLongTap-" +
                        datetime.now().strftime('%M:%S.%f')[:-4])

        perfom_tap(WHITE_SPACE_CORD_X, WHITE_SPACE_CORD_Y)  # white space
        perfom_long_tap(FIRST_APP_CORD_X +
                        APPS_SEPARATION_PTS, FIRST_APP_CORD_Y)
        take_screenshot("SecondLongTap-" +
                        datetime.now().strftime('%M:%S.%f')[:-4])

        perfom_tap(WHITE_SPACE_CORD_X, WHITE_SPACE_CORD_Y)  # white space
        perfom_long_tap(FIRST_APP_CORD_X +
                        (APPS_SEPARATION_PTS * 2), FIRST_APP_CORD_Y)
        take_screenshot("ThirdLongTap-" +
                        datetime.now().strftime('%M:%S.%f')[:-4])

        n -= 1
        event_counter(n)  # handles the BACK action if needed
        if n == 0:
            break

        '''
        3. Verify the current battery percentage and write it in the report.
        '''
        write_report("""
                        <br/> <br/> 
                        <p> <strong>3.</strong> &nbsp; Verify the current battery percentage - ADB checks the status and then prints the result on Google Search Bar. </p> 
                        <br/>
                    """)
        battery_status()
        take_screenshot("Battery-Level-" +
                        datetime.now().strftime('%M:%S.%f')[:-4])
        home()

        n -= 1
        event_counter(n)  # handles the BACK action if needed
        if n == 0:
            break

        '''
        4. Turn on bluetooth
        '''
        write_report("""
                        <br/> <br/> 
                        <p> <strong>4.</strong> &nbsp; Turn on bluetooth - ADB checks the status and then prints the result on Google Search Bar. </p> 
                        <br/>
                    """)
        turn_on_bluetooth()
        take_screenshot("BluetoothOn-Status-" +
                        datetime.now().strftime('%M:%S.%f')[:-4])
        home()

        n -= 1
        event_counter(n)  # handles the BACK action if needed
        if n == 0:
            break

        '''
        5. Launch the contacts app and add a new contact to the contact's list
        '''
        start_package(
            CONTACTS_PACKAGE)  # opens the Contacts Application using the Package Name
        time.sleep(LONG_WAIT)

        write_report("""
                        <br/> <br/> 
                        <p> <strong>5.</strong> &nbsp;Launch Contacts App</p>
                    """)
        take_screenshot("ContactsApp-" +
                        datetime.now().strftime('%M:%S.%f')[:-4])

        add_contact(n)

        n -= 1
        event_counter(n)  # handles the BACK action if needed
        if n == 0:
            break

        home()
        start_package(CONTACTS_PACKAGE)  # show list of contacts
        time.sleep(LONG_WAIT)
        take_screenshot("ContactsList-" +
                        datetime.now().strftime('%M:%S.%f')[:-4])
        time.sleep(LONG_WAIT)
        home()


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
    cmd = f"{ADB_PATH} adb devices"
    process = execute_process(cmd, "Device ID")
    global DEVICE_ID
    DEVICE_ID = "-s " + process.split()[4]
    write_report(f"<p> Device ID: {DEVICE_ID[3:]} </p>")


def perfom_keyevent(for_key):
    cmd = f"{ADB_PATH} adb {DEVICE_ID} shell input keyevent {for_key}"
    execute_process(cmd, f"{for_key} Key Event")


def home():
    # PERFORM HOME HEY EVENT
    perfom_keyevent(HOME_KEY_EVENT)
    time.sleep(SHORT_WAIT)


def swipe_up():
    (coordX1, coordY1) = (400, 880)
    (coordX2, coordY2) = (400, 50)
    milliseconds = 180
    cmd = f"{ADB_PATH} adb {DEVICE_ID} shell input swipe {coordX1} {coordY1} {coordX2} {coordY2} {milliseconds}"
    execute_process(cmd, "Swipe Up")
    time.sleep(SHORT_WAIT)


def perfom_tap(coordX, coordY):
    cmd = f"{ADB_PATH} adb {DEVICE_ID} shell input tap {coordX} {coordY}"
    execute_process(cmd, f"Tap ({coordX}, {coordY})")
    time.sleep(SHORT_WAIT)


def perfom_long_tap(coordX, coordY):
    milliseconds = 1200  # 1.2 seg
    cmd = f"{ADB_PATH} adb {DEVICE_ID} shell input swipe {coordX} {coordY} {coordX} {coordY} {milliseconds}"
    execute_process(cmd, f"Long tap ({coordX}, {coordY})")
    time.sleep(SHORT_WAIT)


def battery_status():
    cmd = f"{ADB_PATH} adb {DEVICE_ID} shell dumpsys battery | grep level"
    process = execute_process(cmd, "Battery Status")
    home()
    time.sleep(SHORT_WAIT)
    perfom_tap(SEARCHBAR_CORD_X, SEARCHBAR_CORD_Y)  # google search bar
    time.sleep(SHORT_WAIT)
    cmd = f"{ADB_PATH} adb {DEVICE_ID} shell \"input keyboard text 'Battery {process}'\""
    write_report(f"<p>{process}</p>")
    execute_process(cmd, "Inserting Input with Battery Status")
    time.sleep(LONG_WAIT)


def turn_on_bluetooth():
    cmd = f"{ADB_PATH} adb {DEVICE_ID} shell settings put global bluetooth_disabled_profiles 1"
    process = execute_process(cmd, "Turning On Bluetooth")
    home()
    time.sleep(SHORT_WAIT)
    perfom_tap(SEARCHBAR_CORD_X, SEARCHBAR_CORD_Y)  # google search bar
    time.sleep(SHORT_WAIT)
    cmd = f"{ADB_PATH} adb {DEVICE_ID} shell \"input keyboard text 'Bluetooth: {process}'\""
    write_report(f"<p>{process}</p>")
    execute_process(cmd, "Inserting Input with Bluetooth Status Status")
    time.sleep(LONG_WAIT)


def start_package(package_name):
    cmd = f"{ADB_PATH} adb {DEVICE_ID} shell monkey -p {package_name} -c android.intent.category.LAUNCHER 1"
    try:
        stop_package(package_name)
        execute_process(cmd, f"Launch App {package_name}")
    except:
        pass


def add_contact(n):
    time.sleep(SHORT_WAIT)
    perfom_tap(CONTACTS_APP_ADD_BTN_CORD_X,
               CONTACTS_APP_ADD_BTN_CORD_Y)  # add button

    # perfom_tap(556, 1047) # add google account alert  -> cancel

    sec = datetime.now().strftime("%S")
    cmd = f"{ADB_PATH} adb {DEVICE_ID} shell \"input keyboard text 'Seeb-{ sec }'\""
    execute_process(cmd, "Inserting Contact First Name")

    time.sleep(SHORT_WAIT)
    write_report(
        "<br/> <br/> <p> <strong>4.1.</strong> &nbsp; Add Contact</p>")
    take_screenshot("Added-" + datetime.now().strftime('%M:%S.%f')[:-4])

    perfom_keyevent(KEYBOARD_ENTER)

    cmd = f"{ADB_PATH} adb {DEVICE_ID} shell \"input keyboard text 'Gar-{ sec }'\""
    execute_process(cmd, "Inserting Contact Last Name")

    perfom_keyevent(KEYBOARD_ENTER)

    cmd = f"{ADB_PATH} adb {DEVICE_ID} shell \"input keyboard text '3901234567'\""
    execute_process(cmd, "Inserting Contact Phone")

    perfom_tap(CONTACTS_APP_SAVE_BTN_CORD_X,
               CONTACTS_APP_SAVE_BTN_CORD_Y)  # save button
    time.sleep(LONG_WAIT)


def stop_package(package_name):
    cmd = f"{ADB_PATH} adb {DEVICE_ID} shell am force-stop {package_name}"
    try:
        execute_process(cmd, f"Stop App {package_name}")
    except:
        pass


def write_on_file(with_name, a_string):
    data = ""
    try:
        with open(with_name, "rt") as website:
            data = website.read()
            # placeholder on HTML file to replace with report
            data = data.replace(PLACEHOLDER, a_string)

        with open(with_name, 'wt') as website:
            website.write(data)
    except IOError:
        name = input("Enter a valid report file.\n")
        write_on_file(name, REPORT)


def take_screenshot(capture_name):
    capture_name += "-Event-" + str(EVENT_COUNTER)
    cmd = f"{ADB_PATH} adb {DEVICE_ID} shell screencap /sdcard/{capture_name}.png"
    execute_process(cmd, f"Taking Screenshot {capture_name}")
    time.sleep(SHORT_WAIT)

    local_image_file = f"{PATH_TO_IMAGES_FOLDER + capture_name}.png"
    cmd = f"{ADB_PATH} adb {DEVICE_ID} pull /sdcard/{capture_name}.png {local_image_file}"
    execute_process(cmd, f"Recovering Screenshot {capture_name}")

    write_report(
        f" <img src=\"{local_image_file}\"  alt=\"{capture_name}\" height=300 /> ")


def write_report(text):
    global REPORT
    REPORT += text


def install_application(with_path):
    cmd = f"{ADB_PATH} adb {DEVICE_ID} install {with_path}"
    try:
        execute_process(cmd, "Installing Application")
    except:
        pass
    time.sleep(LONG_WAIT*3)


def uninstall_application(with_package_name):
    cmd = f"{ADB_PATH} adb {DEVICE_ID} uninstall {with_package_name}"
    try:
        execute_process(cmd, "Uninstalling Application")
    except:
        pass
    time.sleep(LONG_WAIT)


def event_counter(n):
    if n % STUDENT_ID == 0:
        print("\n*--> SE HACE BACK\n")
        perfom_keyevent(BACK_KEY_EVENT)
        write_report('''
                        <br/>
                        <p class="back"><strong> A back action was made here. </strong></p>
                        <br/>
                    ''')
        time.sleep(SHORT_WAIT)


if __name__ == "__main__":
    n = input("Enter positive amount of actions to perfom:\n")
    n = int(n) if int(n) > 0 else 1
    start_process(n)
