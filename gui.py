import tkinter as tk

# Import the handler
import handler

root = tk.Tk()

# This is the declaration of the variable associated with the checkbox
cbVariable = tk.IntVar()

# This is the section of code which define the main window
root.geometry('400x400')
root.title('Coding_Assignment')
root.resizable(False, False)

# create all of the main containers
initFrame = tk.Frame(root, width=200, height=200, borderwidth=2, relief="groove")
liveFrame = tk.Frame(root, width=155, height=200, borderwidth=2, relief="groove")
optionsFrame = tk.Frame(root, width=375, height=100, borderwidth=2, relief="groove")

# layout all of the main containers
root.grid_rowconfigure(0, weight=0)
root.grid_columnconfigure(0, weight=1)

initFrame.grid(row=0, column=0, sticky="W", padx=15, pady=15)
liveFrame.grid(row=0, column=1, sticky="E", padx=15, pady=15)
optionsFrame.grid(row=1, columnspan=2, rowspan=3, padx=15)

# Init Frame
tk.Label(root, text='Initialize settings', fg='#000000', font=('arial', 9, 'bold')) \
    .grid(row=0, column=0, sticky="N", pady=20)
tk.Button(root, text='Load Entities', bg='#F0FFFF', font=('arial', 9, 'normal'),
          command=handler.initButtonClick).grid(row=0, column=0, sticky="S", pady=40)

tk.Label(root, text='HP bar position:', fg='#000000', font=('arial', 9, 'normal')).grid(row=0, column=0, sticky="NW",
                                                                                        padx=25, pady=60)
hpBarLabel = tk.Label(root, text='Waiting', fg='#f0ae13', font=('arial', 9, 'normal'))
hpBarLabel.grid(row=0, column=0, sticky="NE", padx=35, pady=60)

tk.Label(root, text='Mini map position:', fg='#000000', font=('arial', 9, 'normal')).grid(row=0, column=0, sticky="NW",
                                                                                          padx=25, pady=85)
miniMapLabel = tk.Label(root, text='Waiting', fg='#f0ae13', font=('arial', 9, 'normal'))
miniMapLabel.grid(row=0, column=0, sticky="NE", padx=35, pady=85)

# Live Frame

tk.Label(root, text='Live information', fg='#000000', font=('arial', 9, 'bold')).grid(row=0, column=1, sticky="N",
                                                                                      pady=20)
tk.Label(root, text='Player health:', fg='#000000', font=('arial', 9, 'normal')).grid(row=0, column=1, sticky="NW",
                                                                                      padx=25, pady=60)
healthLabel = tk.Label(root, text='Waiting', fg='#123fff', font=('arial', 9, 'normal'))
healthLabel.grid(row=0, column=1, sticky="NE", padx=35, pady=60)

tk.Label(root, text='Coordinates:', fg='#000000', font=('arial', 9, 'normal')).grid(row=0, column=1, sticky="NW",
                                                                                    padx=25, pady=85)
coordinatesLabel = tk.Label(root, text='(10,10)', fg='#123fff', font=('arial', 9, 'normal'))
coordinatesLabel.grid(row=0, column=1, sticky="NE", padx=35, pady=85)

# Options Frame

tk.Label(root, text='More options', fg='#000000', font=('arial', 9, 'bold')).grid(row=1, columnspan=2, sticky="N",
                                                                                  pady=5)

# Notification
autoRuneSolver = tk.IntVar()
randomPlayerNotification = tk.IntVar()
friendPlayerNotification = tk.IntVar()

# Set default true
autoRuneSolver.set(1)
randomPlayerNotification.set(1)
friendPlayerNotification.set(1)

autoRuneSolverCheckbutton = tk.Checkbutton(root, text="Auto Rune Solver", variable=autoRuneSolver,
                                           onvalue=1, offvalue=0).grid(row=2, column=0, sticky="W", padx=25)
randomPlayerCheckbutton = tk.Checkbutton(root, text="Random notification", variable=randomPlayerNotification,
                                         onvalue=1, offvalue=0).grid(row=2, column=1, sticky="W", padx=25)
friendPlayerCheckbutton = tk.Checkbutton(root, text="Friend notification", variable=friendPlayerNotification,
                                         onvalue=1, offvalue=0).grid(row=3, column=1, sticky="W", padx=25)

# Start Section
startButton = tk.Button(root, text='Start Botting', bg='#F0FFFF', font=('arial', 12, 'normal'),
                        command=handler.startButtonClick)
startButton.grid(row=4, columnspan=2, sticky="S", pady=10)

tk.Label(root, text='Status:', fg='#000000', font=('arial', 10, 'normal')).grid(row=5, column=0, sticky="SW", padx=10)
botStatusLabel = tk.Label(root, text='not running', fg='#FF0000', font=('arial', 10, 'normal'))
botStatusLabel.grid(row=5, column=0, sticky="SW", padx=55)


def updateHpBarLabel(error=None):
    if error is not None:
        hpBarLabel['fg'] = '#c70c0c'
        hpBarLabel['text'] = error
    else:
        hpBarLabel['text'] = 'Done'
        hpBarLabel['fg'] = '#0aad20'


def updateMiniMapLabel(error=None):
    if error is not None:
        miniMapLabel['fg'] = '#c70c0c'
        miniMapLabel['text'] = error
    else:
        miniMapLabel['text'] = 'Done'
        miniMapLabel['fg'] = '#0aad20'


def updateCurrentHealth(value):
    healthLabel['text'] = '{0}%'.format(value)


def updateCurrentCoordinate(point):
    coordinatesLabel['text'] = '({0}, {1})'.format(point.x, point.y)


def updateBotStatus(isRunning):
    if isRunning:
        botStatusLabel['text'] = 'running..'
        botStatusLabel['fg'] = '#0aad20'
        startButton['text'] = 'Stop Botting'
    else:
        botStatusLabel['text'] = 'not running'
        botStatusLabel['fg'] = '#ff0000'
        startButton['text'] = 'Start Botting'
