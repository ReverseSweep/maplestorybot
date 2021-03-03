import pydirectinput
import win32gui
import handler
import time
import random
from pynput.keyboard import Key, Controller
from PIL import ImageGrab
import pyttsx3

keyboard = Controller()

# Maple window name
MAPLE_WINDOW_NAME = 'Ristonia'

# Global variables
MIN_HP_IN_PERCENTAGE = 40
HP_KEY = 'b'

# MUST DEFINE
OPEN_RUNE_KEY = 'Space'
JUMP_KEY = 'alt'
# TP_KEY = '...' - Use this if you are a mage


BUFF_TIME = 60 * 3  # Seconds

CLEAVE_KEY = 'ctrl'
SWORDS_KEY = 'pageup'
HS = '['
Reign = 'a'
Storm = 'c'
Sharp = ']'
Shard = 'shift'
Infinity = 'x'
Rope = '`'
Totem = 'end'
Ruin = 'd'
Aether = 'home'
step = 's'


def startBot():
    # timeout skills
    buffTimeOut = time.time()
    doBuff()
    while True:
        if handler.botThread.isRunning() and handler.gameMonitorInstance.getPlayerCoords() is not None:

            # Don't touch
            currentTime = time.time()
            checkDefaults()

            # Buffs and sync methods
            if currentTime > buffTimeOut:  # Every 3 minutes
                doBuff()
                buffTimeOut = time.time() + BUFF_TIME



            # Normal loop
            # goTo(x,y,*)
            goTo(194,19,5)
            pydirectinput.press(Infinity)
            pydirectinput.press(Aether)
            print('Using Aether Bloom')
            goTo(194,50,5)
            pydirectinput.press(Reign)
            pydirectinput.press(Aether)
            print('Using Aether Bloom')
            goTo(178,42,5)
            pydirectinput.press(Aether)
            print('Using Aether Bloom')
            pydirectinput.press(Storm)
            print('Using Storm..')
            goTo(53,42,5)
            pydirectinput.press(Ruin)
            print('Using Ruin..')

        print('Bot is running..')


def checkDefaults():
    # Check the hp of the player
    checkHp(handler.gameMonitorInstance.getCurrentHp())

    # Check if there is a rune
    checkRune(handler.gameMonitorInstance.getRuneCoords())

    # Check if there is a random player
    checkRandomPlayer(handler.gameMonitorInstance.isRandomPlayerInMap())

    # Check if there is a random player
    checkFriendPlayer(handler.gameMonitorInstance.isFriendPlayerInMap())  # Check if there is a random player


def checkHp(currentHp):
    if currentHp is not None and currentHp < MIN_HP_IN_PERCENTAGE:
        pydirectinput.press(HP_KEY, 2, 0.2)


def checkRandomPlayer(isRandomPlayerInMap):
    if isRandomPlayerInMap:
        print('RANDOM PLAYER IS IN THE MAP!')
        # pyttsx3.speak("Random player is in the map")


def checkFriendPlayer(isFriendPlayerInMap):
    if isFriendPlayerInMap:
        print('FRIEND PLAYER IS IN THE MAP!')
        # pyttsx3.speak("Friend player is in the map")


def checkRune(runeCoords):
    if handler.gameMonitorInstance.getRuneCoords() is not None:
        print('RUNE HAS BEEN FOUND!')
        # pyttsx3.speak("Rune has been found")

        goTo(runeCoords.x, runeCoords.y, 3, True)

        currentPlayerCoords = handler.gameMonitorInstance.getPlayerCoords()

        # Double check the coords before taking a screenshot
        if not isInRange(runeCoords.x, runeCoords.y, currentPlayerCoords, 5):
            return

        time.sleep(2)
        pydirectinput.press(OPEN_RUNE_KEY)
        time.sleep(2)

        # Search client
        mapleWindow = win32gui.FindWindow(None, MAPLE_WINDOW_NAME)
        if mapleWindow is not None:
            mapleWindowRect = win32gui.GetWindowRect(mapleWindow)
            topLeftX, topLeftY, bottomRightX, bottomRightY = mapleWindowRect

            mapleWindowWidth = bottomRightX - topLeftX
            mapleWindowHeight = bottomRightY - topLeftY

            # Static rune sizes
            RUNE_WIDTH = 450

            runeTopLeftX = (mapleWindowWidth / 2) - (RUNE_WIDTH / 2) + topLeftX
            runeTopLeftY = (mapleWindowHeight / 4) + topLeftY

            runeBottomRightX = runeTopLeftX + RUNE_WIDTH
            runeBottomRightY = runeTopLeftY + (mapleWindowHeight / 4)

            runeScreenshot = ImageGrab.grab(bbox=(runeTopLeftX, runeTopLeftY, runeBottomRightX, runeBottomRightY))
            arrowsTuple = solveRune(runeScreenshot)

            if len(arrowsTuple) == 4:
                for arrow in arrowsTuple:
                    time.sleep(random.uniform(0.6, 1))
                    if arrow[0] == 'RIGHT':
                        keyboard.press(Key.right)
                        keyboard.release(Key.right)
                    if arrow[0] == 'LEFT':
                        keyboard.press(Key.left)
                        keyboard.release(Key.left)
                    if arrow[0] == 'DOWN':
                        keyboard.press(Key.down)
                        keyboard.release(Key.down)
                    if arrow[0] == 'UP':
                        keyboard.press(Key.up)
                        keyboard.release(Key.up)
                handler.gameMonitorInstance.setRuneCoords(None)  # Reset rune flag
                handler.gameMonitorInstance.runeCoords = None  # Hard reset rune flag


def getArrowsKey(arrowsKey):
    return arrowsKey[1]


def solveRune(runeScreenshot):
    width, height = runeScreenshot.size
    arrows = []

    for currentX in range(width):
        for currentY in range(height):
            addable = True
            rgbPixel = runeScreenshot.getpixel((currentX, currentY))
            if 235 <= rgbPixel[1] <= 255 and 0 < rgbPixel[0] < 50:
                for arrow in arrows:  # Check if this arrow already has been solved
                    if abs(arrow[1] - currentX) <= 25:
                        addable = False
                if addable:
                    direction = findArrowDirection(runeScreenshot, currentX, currentY)
                    if direction is not None:
                        arrows.append((direction, currentX))

    return sorted(arrows, key=getArrowsKey)


def findArrowDirection(runeScreenshot, x, y):
    maxX, maxY = runeScreenshot.size

    for i in range(1, 20, 1):
        if x + i < maxX:
            rightPixel = runeScreenshot.getpixel((x + i, y))
            if rightPixel[1] == 255 and 150 < rightPixel[0] < 230:
                return 'RIGHT'

        leftPixel = runeScreenshot.getpixel((x - i, y))
        if leftPixel[1] == 255 and 150 < leftPixel[0] < 230:
            return 'LEFT'

        upPixel = runeScreenshot.getpixel((x, y - i))
        if upPixel[1] == 255 and 150 < upPixel[0] < 230:
            return 'UP'

        if y + i < maxY:
            downPixel = runeScreenshot.getpixel((x, y + i))
            if downPixel[1] == 255 and 150 < downPixel[0] < 230:
                return 'DOWN'
    return None


def doBuff():
    pydirectinput.press(HS)
    print('Doing Holy Symbol')
    time.sleep(0.407)
    pydirectinput.press(Sharp)
    time.sleep(0.407)
    print('Using Sharp Eyes')
    time.sleep(0.407)
    pydirectinput.press(Totem)
    time.sleep(0.407)
    print('Using Totem')
    print('Doing buffs')
    # Define your buffs

    # pydirectinput.press('pageup')


def attack():
    pydirectinput.press(CLEAVE_KEY, 1, 0.1)
    pydirectinput.press(SWORDS_KEY, 1, 0)


def isInRange(targetX, targetY, playerCoords, wantedRange):
    xRange = abs(targetX - playerCoords.x)
    yRange = abs(targetY - playerCoords.y)
    return xRange < wantedRange and yRange < wantedRange


def goTo(targetX, targetY, rangeFromCoords, isRune=False):
    WANTED_RANGE = rangeFromCoords
    if handler.gameMonitorInstance.getPlayerCoords() is not None:

        # Get the updated coordinates from the monitor gui
        currentPlayerLocation = handler.gameMonitorInstance.getPlayerCoords()

        xDistance = targetX - currentPlayerLocation.x
        while abs(xDistance) > WANTED_RANGE and handler.botThread.isRunning():  # Check the X axis
            goToDirection('RIGHT', xDistance) if xDistance > 0 else goToDirection('LEFT', xDistance)
            currentPlayerLocation = handler.gameMonitorInstance.getPlayerCoords()
            xDistance = targetX - currentPlayerLocation.x

        yDistance = targetY - currentPlayerLocation.y
        while abs(yDistance) > WANTED_RANGE and handler.botThread.isRunning():  # Check the Y Axis
            goDown() if yDistance > 0 else goUp(yDistance)
            if isRune:
                time.sleep(1)
            currentPlayerLocation = handler.gameMonitorInstance.getPlayerCoords()
            yDistance = targetY - currentPlayerLocation.y


def goToDirection(direction, distance):
    if abs(distance) >= 30:  # Check if this is long enough for double jump
        pydirectinput.keyDown(direction.lower())
        # pydirectinput.press(JUMP_KEY, 1, 0.05)
        pydirectinput.press(JUMP_KEY, 2, 0.05)
        attack()
        # pydirectinput.press(TP_KEY) - Use me if you are using teleport (Kanna, Mage...)
        pydirectinput.keyUp(direction.lower())
    else:
        holdKey(direction.lower(), 0.5)


def holdKey(key, hold_time):
    startTime = time.time()
    while time.time() - startTime < hold_time:
        pydirectinput.keyDown(key)
    pydirectinput.keyUp(key)


def goUp(distance):
    if abs(distance) >= 30:
        pydirectinput.press(JUMP_KEY)

    pydirectinput.press(Rope)
    time.sleep(1)


def goDown():
    pydirectinput.keyDown('down')
    pydirectinput.press(JUMP_KEY)
    pydirectinput.keyUp('down')
    pydirectinput.keyDown('left')
    pydirectinput.press(JUMP_KEY)
    pydirectinput.keyUp('left')
    time.sleep(1)