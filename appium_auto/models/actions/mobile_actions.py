import time
import random
from appium_auto.utilities import mouse_actions
from appium_auto.models.elements.mobile import mobile_elements
from appium import webdriver
from appium.webdriver.common.touch_action import TouchAction
from selenium.common.exceptions import TimeoutException


class GoogleAccActions:
    elements = mobile_elements.GoogleAccElements()

    def __init__(self, driver: webdriver.Remote, ):
        self.touches = TouchAction(driver)

    def tap_login_button(self, driver: webdriver.Remote, ):
        self.elements.find_login_button(driver).click()

    def tap_next_button(self, driver: webdriver.Remote, ):
        self.elements.find_next_button(driver).click()

    def tap_point_button(self, driver: webdriver.Remote, ):
        self.elements.find_point_button(driver).click()

    def tap_skip_button(self, driver: webdriver.Remote, ):
        self.elements.find_skip_button(driver).click()

    def tap_throwing_menu(self, driver: webdriver.Remote, multiple=False, i=None):
        if multiple:
            self.elements.find_throwing_menu(driver, multiple=True)[i].click()
        else:
            self.elements.find_throwing_menu(driver).click()

    def tap_menu_item(self, driver: webdriver.Remote, multiple=False, i=None):
        if multiple:
            self.elements.find_menu_item(driver, multiple=True)[i].click()
        else:
            self.elements.find_menu_item(driver).click()

    def write_in_text_input(self, driver: webdriver.Remote, value, multiple=False, i=None):
        if multiple:
            self.elements.find_text_input(driver, multiple=True)[i].send_keys(value)
        else:
            self.elements.find_text_input(driver).send_keys(value)

    def choose_month(self, driver: webdriver.Remote, ):
        month_spinner = self.elements.find_throwing_menu(driver, multiple=True)[0]
        month_spinner.click()
        y = 42 + 85 * random.randrange(1, 6)
        time.sleep(0.2)
        self.touches.tap(month_spinner, 100, y).perform()

    def choose_gender(self, driver: webdriver.Remote, ):
        self.elements.find_throwing_menu(driver, multiple=True)[1].click()
        main_frame = self.elements.find_main_frame(driver)
        self.touches.tap(main_frame, 443, 240).perform()

    def gmail_page_type_is_given(self, driver: webdriver.Remote, ) -> bool:
        try:
            self.elements.find_point_button(driver)
            return True
        except TimeoutException:
            return False

    def choose_gmail_from_given(self, driver: webdriver.Remote, ) -> str:
        option = self.elements.find_point_button(driver)
        option.click()
        return option.text

    def accept_terms_and_conditions(self, driver: webdriver.Remote, ):
        mouse_actions.scroll_down(1000, 500, 8)
        main_frame = self.elements.find_main_frame(driver)
        self.touches.tap(main_frame, 1150, 750).perform()

    def tap_accept_button(self, driver: webdriver.Remote, ):
        mouse_actions.scroll_down(1000, 500, 1)
        self.elements.find_login_button(driver)


class GoogleChromeActions:
    elements = mobile_elements.GoogleChromeElements()

    def set_default_searching_engine(self, driver: webdriver.Remote, ):
        point_button_list = self.elements.find_point_button(driver, True)
        for element in point_button_list:
            if element.text == 'Google':
                element.click()
        self.elements.find_ok_button(driver).click()

    def tap_sign_in_button(self, driver: webdriver.Remote, ):
        mouse_actions.scroll_down(1000, 500, 1)
        self.elements.find_sign_in_button(driver).click()

    def tap_positive_button(self, driver: webdriver.Remote, ):
        self.elements.find_positive_button(driver).click()

    def write_in_url_bar(self, driver: webdriver.Remote, value):
        self.elements.find_url_bar(driver).click()
        self.elements.find_url_bar(driver).send_keys(value)
        driver.press_keycode(66)

    def tap_install_button(self, driver: webdriver.Remote, ):
        self.elements.find_install_button(driver).click()
