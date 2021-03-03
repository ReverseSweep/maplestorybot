from pynput import keyboard
import pyautogui
import utils
import handler


def loadImageClick(title):
    REQUIRED_POS = 2
    positions = []

    def on_release(key):
        if key == keyboard.Key.ctrl_l:  # Press left ctrl
            mousePos = pyautogui.position()
            positions.append(utils.Point(mousePos.x, mousePos.y))
            if len(positions) == REQUIRED_POS:
                return False

    # The event listener will be running in this block
    with keyboard.Listener(on_release=on_release) as listener:
        listener.join()

    utils.loadImageWindow(title, loadImageClick, submitImageClick, positions)


def submitImageClick(pos):
    handler.updateLoadedImageToScreen(pos)
