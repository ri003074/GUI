import os
from functools import partial

import pyautogui
from PIL import ImageGrab

ImageGrab.grab = partial(ImageGrab.grab, all_screens=True)


def get_screen_shot(
    save_file_path,
    x_top_left,
    y_top_left,
    x_bottom_right,
    y_bottom_right,
):
    region = (
        x_top_left,
        y_top_left,
        x_bottom_right - x_top_left,
        y_bottom_right - y_top_left,
    )

    screen_shot = pyautogui.screenshot(region=region)
    screen_shot.save(save_file_path)


if __name__ == "__main__":
    get_screen_shot(
        save_file_path=os.getcwd() + "//b.png",
        x_top_left=400,
        y_top_left=400,
        x_bottom_right=1176,
        y_bottom_right=900,
    )
