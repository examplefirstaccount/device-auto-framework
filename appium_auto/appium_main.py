import time
import random
import string
import names
from appium_auto.models.actions import mobile_actions


class GoogleAccount:
    def __init__(self):
        self.firstName = names.get_first_name(gender='male')
        self.lastName = names.get_last_name()
        self.bornDay = random.randrange(1, 31)
        self.bornYear = random.randrange(1990, 2004)
        self.username = self.lastName + self.firstName + str(random.randrange(100, 1000)) + ''.join(
            random.choice(string.ascii_uppercase) for i in range(2))
        chars = string.ascii_letters + string.digits + string.punctuation
        self.password = ''.join(random.choice(chars) for i in range(12))


def reg_google_acc(driver):
    google_account = GoogleAccount()
    google_acc_actions = mobile_actions.GoogleAccActions(driver)
    google_acc_actions.tap_login_button(driver)
    google_acc_actions.tap_throwing_menu(driver)
    time.sleep(0.5)
    google_acc_actions.tap_menu_item(driver, multiple=True, i=0)
    time.sleep(2)
    google_acc_actions.write_in_text_input(driver, google_account.firstName, multiple=True, i=0)
    google_acc_actions.write_in_text_input(driver, google_account.lastName, multiple=True, i=1)
    google_acc_actions.tap_next_button(driver)
    time.sleep(2)
    google_acc_actions.write_in_text_input(driver, google_account.bornDay, multiple=True, i=0)
    time.sleep(0.5)
    google_acc_actions.choose_month(driver)
    time.sleep(0.5)
    google_acc_actions.write_in_text_input(driver, google_account.bornYear, multiple=True, i=1)
    time.sleep(0.5)
    google_acc_actions.choose_gender(driver)
    time.sleep(0.5)
    google_acc_actions.tap_next_button(driver)
    time.sleep(0.5)
    is_given = google_acc_actions.gmail_page_type_is_given(driver)
    if is_given:
        google_account.gmail = google_acc_actions.choose_gmail_from_given(driver)
        time.sleep(0.5)
        google_acc_actions.tap_next_button(driver)
    else:
        google_acc_actions.write_in_text_input(driver, google_account.username)
        time.sleep(0.5)
        google_acc_actions.tap_next_button(driver)
    time.sleep(0.5)
    google_acc_actions.write_in_text_input(driver, google_account.password)
    time.sleep(0.5)
    google_acc_actions.tap_next_button(driver)
    time.sleep(0.5)
    google_acc_actions.tap_skip_button(driver)
    time.sleep(0.5)
    google_acc_actions.tap_next_button(driver)
    time.sleep(0.5)
    google_acc_actions.accept_terms_and_conditions(driver)
    time.sleep(0.5)
    google_acc_actions.tap_accept_button(driver)
    return google_account


def log_in_google_acc(driver, username, password):
    google_acc_actions = mobile_actions.GoogleAccActions(driver)
    google_acc_actions.write_in_text_input(driver, username)
    google_acc_actions.tap_login_button(driver)
    time.sleep(0.5)
    google_acc_actions.write_in_text_input(driver, password)
    google_acc_actions.tap_login_button(driver)
    time.sleep(0.5)
    google_acc_actions.tap_next_button(driver)


def install_app_through_referral_link(driver, referral_link):
    google_chrome_actions = mobile_actions.GoogleChromeActions()
    google_chrome_actions.set_default_searching_engine(driver)
    time.sleep(0.5)
    google_chrome_actions.tap_sign_in_button(driver)
    time.sleep(1)
    google_chrome_actions.tap_positive_button(driver)
    time.sleep(1)
    google_chrome_actions.write_in_url_bar(driver, value=referral_link)
    google_chrome_actions.tap_install_button(driver)
