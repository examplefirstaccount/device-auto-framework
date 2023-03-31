from appium_auto.models.elements.base_elements import BaseElements
from appium_auto.models.locators.mobile_locators import GoogleAccLocators
from appium_auto.models.locators.mobile_locators import GoogleChromeLocators
from appium import webdriver
from selenium.webdriver.support import expected_conditions as ec


class GoogleAccElements(BaseElements):
    def find_main_frame(self, driver: webdriver.Remote, ):
        return self.wait_for_element(driver).until(ec.presence_of_element_located(GoogleAccLocators.MAIN_FRAME))

    def find_login_button(self, driver: webdriver.Remote, ):
        return self.wait_for_element(driver).until(ec.presence_of_element_located(GoogleAccLocators.LOGIN_BUTTON))

    def find_throwing_menu(self, driver: webdriver.Remote, multiple=False):
        if not multiple:
            return self.wait_for_element(driver).until(ec.presence_of_element_located(GoogleAccLocators.THROWING_MENU))
        else:
            return self.wait_for_element(driver).until(ec.presence_of_all_elements_located(GoogleAccLocators.THROWING_MENU))

    def find_menu_item(self, driver: webdriver.Remote, multiple=False):
        if not multiple:
            return self.wait_for_element(driver).until(ec.presence_of_element_located(GoogleAccLocators.MENU_ITEM))
        else:
            return self.wait_for_element(driver).until(ec.presence_of_all_elements_located(GoogleAccLocators.MENU_ITEM))

    def find_text_input(self, driver: webdriver.Remote, multiple=False):
        if not multiple:
            return self.wait_for_element(driver).until(ec.presence_of_element_located(GoogleAccLocators.TEXT_INPUT))
        else:
            return self.wait_for_element(driver).until(ec.presence_of_all_elements_located(GoogleAccLocators.TEXT_INPUT))

    def find_point_button(self, driver: webdriver.Remote, ):
        return self.wait_for_element(driver).until(ec.presence_of_element_located(GoogleAccLocators.POINT_BUTTON))

    def find_next_button(self, driver: webdriver.Remote, ):
        return self.wait_for_element(driver).until(ec.presence_of_element_located(GoogleAccLocators.NEXT_BUTTON))

    def find_skip_button(self, driver: webdriver.Remote, ):
        return self.wait_for_element(driver).until(ec.presence_of_element_located(GoogleAccLocators.SKIP_BUTTON))


class GoogleChromeElements(BaseElements):
    def find_main_frame(self, driver: webdriver.Remote, ):
        return self.wait_for_element(driver).until(ec.presence_of_element_located(GoogleChromeLocators.MAIN_FRAME))

    def find_point_button(self, driver: webdriver.Remote, multiple=False):
        if not multiple:
            return self.wait_for_element(driver).until(ec.presence_of_element_located(GoogleChromeLocators.POINT_BUTTON))
        else:
            return self.wait_for_element(driver).until(ec.presence_of_all_elements_located(GoogleChromeLocators.POINT_BUTTON))

    def find_ok_button(self, driver: webdriver.Remote, ):
        return self.wait_for_element(driver).until(ec.presence_of_element_located(GoogleChromeLocators.OK_BUTTON))

    def find_sign_in_button(self, driver: webdriver.Remote, ):
        return self.wait_for_element(driver).until(ec.presence_of_element_located(GoogleChromeLocators.SIGN_IN_BUTTON))

    def find_positive_button(self, driver: webdriver.Remote, ):
        return self.wait_for_element(driver).until(ec.presence_of_element_located(GoogleChromeLocators.POSITIVE_BUTTON))

    def find_url_bar(self, driver: webdriver.Remote, ):
        return self.wait_for_element(driver).until(ec.presence_of_element_located(GoogleChromeLocators.URL_BAR))

    def find_install_button(self, driver: webdriver.Remote, ):
        return self.wait_for_element(driver, 20).until(ec.presence_of_element_located(GoogleChromeLocators.INSTALL_BUTTON))
