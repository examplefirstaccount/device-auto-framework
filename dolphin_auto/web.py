import time
from dolphin_auto.google_account import GoogleAcc

from playwright.sync_api import sync_playwright


acc = GoogleAcc()


def connect_to_profile_and_create_acc(port, ws_endpoint):
    playwright = sync_playwright().start()
    browser = playwright.chromium.connect_over_cdp(f'ws://127.0.0.1:{port}{ws_endpoint}')
    page = browser.contexts[0].pages[0]
    page.goto('https://accounts.google.com/signup')
    page.locator('#firstName').type(acc.firstName, delay=100)
    page.locator('#lastName').type(acc.lastName, delay=100)
    time.sleep(5)
    page.locator('[name=Passwd]').type(acc.password, delay=100)
    page.locator('[name=ConfirmPasswd]').type(acc.password, delay=100)
    page.locator('#accountDetailsNext').click()
    return acc

