import tkinter as tk
from PIL import ImageTk, Image, ImageGrab
import colorsys


# Define geometry utils objects
class Point:
    def __init__(self, x=0, y=0):
        self.x = x
        self.y = y


# Define utils functions
def loadImageWindow(title, onLoadButtonClick, updateImageCallback=None, imagePos=None, retry=False):
    # Set the new window on top the root
    newWindow = tk.Toplevel()
    newWindow.grab_set()

    # This is the section of code which define the new window
    newWindow.geometry("400x400")
    newWindow.resizable(False, False)
    newWindow.wm_attributes("-topmost", 1)

    # Functions
    def loadImageButtonClick():
        newWindow.destroy()
        onLoadButtonClick(title)

    def onApplyButtonClick():
        newWindow.destroy()
        updateImageCallback(imagePos)

    if imagePos is None:  # Before image loaded

        newWindow.geometry("350x200")

        # Objects
        tk.Label(newWindow,
                 text=('Load {0} positions'.format(title) if retry is False else 'Oops, try to load positions again'),
                 fg='#000000', font=('arial', 11, 'normal')).place(relx=0.5, rely=0.1, anchor=tk.CENTER)

        tk.Button(newWindow, text='Load Image', bg='#F0FFFF', font=('arial', 14, 'normal'),
                  command=loadImageButtonClick).place(relx=0.5, rely=0.4, anchor=tk.CENTER)

        tk.Label(newWindow, text='Hint: Set the rectangle image with mouse clicks'.format(title), fg='#000000',
                 font=('arial', 9, 'normal')).place(relx=0.5, rely=0.8, anchor=tk.CENTER)
    else:

        # Labels
        tk.Label(newWindow, text='Loaded {0} positions'.format(title), fg='#000000',
                 font=('arial', 11, 'normal')).place(relx=0.5, rely=0.1, anchor=tk.CENTER)

        # Grab a screenshot according to the positions
        screenShotOfPos = ImageGrab.grab(bbox=(imagePos[0].x, imagePos[0].y, imagePos[1].x, imagePos[1].y))

        resizedImage = None
        try:
            baseWidth = 280
            widthPercent = (baseWidth / float(screenShotOfPos.size[0]))
            heightSize = int((float(screenShotOfPos.size[1]) * float(widthPercent)))
            resizedImage = ImageTk.PhotoImage(screenShotOfPos.resize((baseWidth, heightSize), Image.ANTIALIAS))
        except ValueError and ZeroDivisionError:
            print("An exception occurred")
            newWindow.destroy()
            loadImageWindow(title, onLoadButtonClick, None, None, True)  # Try again

        # Set Image
        loadedImage = tk.Label(newWindow, image=resizedImage, borderwidth=2, relief="solid")
        loadedImage.image = resizedImage
        loadedImage.place(relx=0.5, rely=0.5, anchor=tk.CENTER)

        # Buttons
        tk.Button(newWindow, text='Apply', command=onApplyButtonClick).place(x=100, y=350)
        tk.Button(newWindow, text='Retry', command=loadImageButtonClick).place(x=250, y=350)

    newWindow.mainloop()


def rgbToHsv(coordinate):
    hsvValues = colorsys.rgb_to_hsv(coordinate[0] / 255., coordinate[1] / 255., coordinate[2] / 255.)
    returnValues = hsvValues[0] * 360, hsvValues[1], hsvValues[2]
    return returnValues
