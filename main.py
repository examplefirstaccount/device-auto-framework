import os
import sys
import time
import ctypes

from appium import webdriver

from dolphin_auto.api import start_browser_profile, close_browser_profile, DolphinRemoteApi
from dolphin_auto.web import connect_to_profile_and_create_acc
from dolphin_auto.gui import DolphinGui
from appium_auto import appium_main
from emulator.memu import Memuc

# ------------------------------------------------------------
# Preparing part
# ------------------------------------------------------------

LINK = 'SOME_REFERRAL_LINK'
APK_PATH = 'path/to/apk'
APK_PACKAGE_NAME = 'com.example.com'
DOLPHIN_USER = 'your_user'
DOLPHIN_PASS = 'your_pass'

with open('dolphin_cookies.txt', 'r') as file:
    cookies = eval(file.read())

dolphin = DolphinGui()
api = DolphinRemoteApi(username=DOLPHIN_USER, password=DOLPHIN_PASS)


# ------------------------------------------------------------
# Repeating part
# ------------------------------------------------------------


# Checking if ur admin or not
def is_admin():
    try:
        return ctypes.windll.shell32.IsUserAnAdmin()
    except Exception as e:
        print("Error occurred:", e)
        return False


# Creating browser profile
def create_browser_profile():
    profile = api.create_browser_profile('test')
    api.import_cookies(profile, cookies)
    port, ws_endpoint = start_browser_profile(profile_id=profile)
    return profile, port, ws_endpoint


# Registering Google Account
def register_google_acc(port, ws_endpoint):
    acc = connect_to_profile_and_create_acc(port=port, ws_endpoint=ws_endpoint)
    time.sleep(10)
    return acc


# Deleting browser profile
def delete_browser_profile(profile):
    close_browser_profile(profile_id=profile)
    api.delete_browser_profile(profile_id=profile)


# Creating emulator
def create_emulator():
    emu = Memuc()
    emu_index = emu.create_emu()
    return emu, emu_index


# Launching emulator profile
def launch_emulator(emu: Memuc, emu_index):
    emu.start_emu(vm_index=emu_index)


# Getting emulator properties
def get_emulator_properties(emu: Memuc, emu_index):
    platform_version = emu.exec_android_cmd(command='getprop ro.build.version.release', vm_index=emu_index)
    device_name = emu.exec_android_cmd(command='getprop ro.product.model', vm_index=emu_index)
    return platform_version, device_name


# Starting Appium server
def start_appium_server():
    os.system("start /B start cmd.exe @cmd /k appium")


# Connecting to emulator with Appium
def connect_emulator_to_appium(device_name, platform_version):
    desired_capabilities = {
        'platformName': 'android',
        'platformVersion': platform_version,
        'deviceName': device_name,
        'appPackage': 'com.android.vending',
        'appActivity': 'com.google.android.finsky.activities.MainActivity'
    }
    return webdriver.Remote('http://localhost:4723/wd/hub', desired_capabilities=desired_capabilities)


# Log in Google Account
def log_in_g_acc(driver, account):
    appium_main.log_in_google_acc(driver, account.username, account.password)
    time.sleep(3)


# Loading apk file into emulator with Appium
def import_apk_to_emulator(driver: webdriver.Remote, apk_path, app_package_name):
    driver.install_app(apk_path)
    while True:
        if driver.is_app_installed(app_package_name):
            break
        else:
            time.sleep(1)


# Downloading app with referral link
def download_app_via_referral_link(driver: webdriver.Remote, link):
    driver.start_activity('com.android.chrome', 'com.google.android.apps.chrome.Main')
    time.sleep(5)
    appium_main.install_app_through_referral_link(driver, link)


# Working with downloaded app
def work_with_downloaded_app():
    pass
    # ------------------------------------------------------------
    # ------------------------------------------------------------
    # ------------------------------------------------------------


# Offing Appium Server
def turn_off_appium_server():
    os.system("taskkill /F /IM node.exe")
    os.system("taskkill /F /IM cmd.exe")


# Closing and deleting emulator profile
def close_and_wipe_emulator(emu: Memuc, emu_index):
    emu.stop_emu(vm_index=emu_index)


# ------------------------------------------------------------
# Ending part
# ------------------------------------------------------------

# dolphin.app.kill()


if __name__ == '__main__':

    profile_id, browser_port, browser_endpoint = create_browser_profile()
    g_account = register_google_acc(port=browser_port, ws_endpoint=browser_endpoint)
    delete_browser_profile(profile=profile_id)

    config = {'cpus': 2, 'memory': 2048, 'fps': 30, 'is_customed_resolution': 1,
              'resolution_width': 360, 'resolution_height': 640, 'enable_audio': 0, "linenum": "+79375606754"}

    emulator, index = create_emulator()
    launch_emulator(emulator, index)
    emu_platform_version, emu_device_name = get_emulator_properties(emulator, index)
    start_appium_server()
    time.sleep(30)
    appium_driver = connect_emulator_to_appium(device_name=emu_device_name, platform_version=emu_platform_version)

    # input()

    log_in_g_acc(driver=appium_driver, account=g_account)

    # Work with preinstalled app OR download app from Play Store and interact with it
    import_apk_to_emulator(driver=appium_driver, apk_path=APK_PATH, app_package_name=APK_PACKAGE_NAME)
    #  <--OR-->
    download_app_via_referral_link(driver=appium_driver, link=LINK)
    work_with_downloaded_app()
    turn_off_appium_server()
    close_and_wipe_emulator(emulator, index)


if is_admin():
    pass
else:
    ctypes.windll.shell32.ShellExecuteW(None, 'runas', sys.executable, ' '.join(sys.argv), None, 1)
