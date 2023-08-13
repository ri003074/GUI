import ctypes
import time

import pygetwindow
import win32api
import win32gui


def get_window_titles():
    # return [title for title in pygetwindow.getAllTitles() if title != ""]
    return list(filter(lambda x: x != "", pygetwindow.getAllTitles()))


def print_active_window_title():
    for _ in range(0, 10):
        active_window_title = win32gui.GetWindowText(
            win32gui.GetForegroundWindow()
        )
        print(active_window_title)
        print(get_window_rect(window_title=active_window_title))
        time.sleep(1)


def get_window_rect(window_title):
    hwnd = win32gui.FindWindow(None, window_title)
    rect = win32gui.GetWindowRect(hwnd)
    return rect


def get_window_rect_adj(window_title):
    hwnd = win32gui.FindWindow(None, window_title)

    f = ctypes.windll.dwmapi.DwmGetWindowAttribute
    rect = ctypes.wintypes.RECT()
    dw_mwa_extended_frame_bounds = 9
    f(
        ctypes.wintypes.HWND(hwnd),
        ctypes.wintypes.DWORD(dw_mwa_extended_frame_bounds),
        ctypes.byref(rect),
        ctypes.sizeof(rect),
    )
    win32gui.SetForegroundWindow(hwnd)

    tmp = (rect.left, rect.top, rect.right, rect.bottom)
    return tmp


def set_foreground_window(window_title):
    hwnd = win32gui.FindWindow(None, window_title)
    win32gui.SetForegroundWindow(hwnd)


def get_active_window_title():
    return win32gui.GetWindowText(win32gui.GetForegroundWindow())


def move_window(window_title, x, y, width, height):
    hwnd = win32gui.FindWindow(None, window_title)
    win32gui.MoveWindow(hwnd, x, y, width, height, True)


def get_monitor_info():
    return win32api.EnumDisplayMonitors()


def get_monitor_full_size_info():
    monitors = win32api.EnumDisplayMonitors()

    x_left = 0
    x_right = 0
    y_bottom = 0
    for monitor in monitors:

        if x_left > monitor[2][0]:
            x_left = monitor[2][0]

        if y_bottom < monitor[2][3]:
            y_bottom = monitor[2][3]

        if x_right < monitor[2][2]:
            x_right = monitor[2][2]

    lst1 = [i for i in range(x_left - 10, x_right + 10)]
    lst2 = [i for i in range(0 - 10, len(lst1))]
    dic = dict(zip(lst1, lst2))

    return dic, x_left, x_right


if __name__ == "__main__":
    app_title = "リモート デスクトップ接続"

    # print(get_window_rect(window_title=app_title))
    print(get_window_titles())
