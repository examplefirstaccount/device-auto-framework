from pywinauto import Application
from pywinauto.findwindows import ElementNotFoundError


class DolphinGui:
    def __init__(self):
        self.path = r'C:\Users\qwrwe\AppData\Local\Programs\Dolphin Anty\Dolphin Anty.exe'
        self.title = 'Dolphin Anty'
        self.app = self.__start_app()

    def __start_app(self):
        try:
            app = Application(backend='uia').connect(title=self.title)
        except ElementNotFoundError:
            app = Application(backend='uia').start(self.path).connect(title=self.title, timeout=20)
        return app

