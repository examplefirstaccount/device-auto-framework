from appium.webdriver.webdriver import AppiumBy


class AndroidLocators:
    MAIN_FRAME = (AppiumBy.ID, 'android:id/content')
    SWITCH_WIDGET = (AppiumBy.ID, 'android:id/switch_widget')


class GoogleAccLocators(AndroidLocators):
    APP_NAME = 'com.android.vending'
    APP_ACTIVITY = 'com.google.android.finsky.activities.MainActivity'
    LOGIN_BUTTON = (AppiumBy.CLASS_NAME, 'android.widget.Button')
    THROWING_MENU = (AppiumBy.CLASS_NAME, 'android.widget.Spinner')
    MENU_ITEM = (AppiumBy.CLASS_NAME, 'android.view.MenuItem')
    TEXT_INPUT = (AppiumBy.CLASS_NAME, 'android.widget.EditText')
    POINT_BUTTON = (AppiumBy.CLASS_NAME, 'android.widget.RadioButton')
    NEXT_BUTTON = (AppiumBy.XPATH, '/hierarchy/android.widget.FrameLayout/android.widget.LinearLayout/android.widget'
                                   '.FrameLayout/android.widget.FrameLayout/android.widget.FrameLayout/android.webkit'
                                   '.WebView/android.webkit.WebView/android.view.View/android.view.View['
                                   '3]/android.view.View[4]/android.view.View')
    SKIP_BUTTON = (AppiumBy.XPATH, '/hierarchy/android.widget.FrameLayout/android.widget.LinearLayout/android.widget'
                                   '.FrameLayout/android.widget.FrameLayout/android.widget.FrameLayout/android.webkit'
                                   '.WebView/android.webkit.WebView/android.view.View/android.view.View['
                                   '3]/android.view.View[5]/android.view.View')


class GoogleChromeLocators(AndroidLocators):
    APP_NAME = 'com.android.chrome'
    APP_ACTIVITY = 'com.google.android.apps.chrome.Main'
    POINT_BUTTON = (AppiumBy.CLASS_NAME, 'android.widget.RadioButton')
    OK_BUTTON = (AppiumBy.ID, APP_NAME + ':id/button_primary')
    SIGN_IN_BUTTON = (AppiumBy.ID, APP_NAME + ':id/signin_promo_signin_button')
    POSITIVE_BUTTON = (AppiumBy.ID, APP_NAME + ':id/positive_button')
    URL_BAR = (AppiumBy.ID, APP_NAME + ':id/url_bar')
    INSTALL_BUTTON = (AppiumBy.XPATH, '/hierarchy/android.widget.FrameLayout/android.widget.LinearLayout/android.widget'
                                      '.FrameLayout/android.widget.FrameLayout/android.widget.FrameLayout/android.view'
                                      '.ViewGroup/android.widget.FrameLayout[1]/android.widget.FrameLayout[2]/android'
                                      '.webkit.WebView/android.view.View/android.view.View[2]/android.view.View/android'
                                      '.view.View/android.view.View/android.view.View[3]/android.widget.Button')
