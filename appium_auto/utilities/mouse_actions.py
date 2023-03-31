import time

from pywinauto import mouse


def scroll_down(x, y, distance):
    for i in range(distance):
        mouse.scroll((x, y), -1 * distance)
        time.sleep(0.5)


def scroll_up(x, y, distance):
    for i in range(distance):
        mouse.scroll((x, y), -1 * distance)
        time.sleep(0.5)
