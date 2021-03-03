from PIL import Image
import screenManager
import gui
import handler
import utils
import numpy
import time

playerIcon = Image.open('pics\\playerIcon.png')
friendIcon = Image.open('pics\\friendIcon.png')
runeIcon = Image.open('pics\\runeIcon.png')
randomIcon = Image.open('pics\\randomIcon.png')

RANDOM_PLAYER_NOTIFICATION = 10


class GameMonitor:
    def __init__(self, currentHp=None, currentPlayerCoords=None):
        self.currentHp = currentHp
        self.currentPlayerCoords = currentPlayerCoords
        self.runeCoords = None
        self.randomPlayerInMap = False
        self.randomPlayerTimer = None
        self.friendPlayerInMap = None
        self.friendPlayerTimer = None

    def setCurrentHp(self, currentHp):
        self.currentHp = currentHp

    def getCurrentHp(self):
        return self.currentHp

    def setPlayerCoords(self, currentPlayerCoords):
        self.currentPlayerCoords = currentPlayerCoords

    def getPlayerCoords(self):
        return self.currentPlayerCoords

    def setRuneCoords(self, runeCoords):
        self.runeCoords = runeCoords

    def getRuneCoords(self):
        return self.runeCoords

    def setRandomPlayerInMap(self, randomPlayerInMap):
        self.randomPlayerInMap = randomPlayerInMap

    def isRandomPlayerInMap(self):
        return self.randomPlayerInMap

    def setFriendPlayerInMap(self, friendPlayerInMap):
        self.friendPlayerInMap = friendPlayerInMap

    def isFriendPlayerInMap(self):
        return self.friendPlayerInMap

    def start(self):

        while True:
            if handler.gameMonitorThread.isRunning():  # While the running flag is True

                # Player HP
                currentHpInPercentage = getHpInPercentageFromImage()
                if currentHpInPercentage is not None:
                    self.setCurrentHp(currentHpInPercentage)  # Update the hp to the private member
                    gui.updateCurrentHealth(currentHpInPercentage)  # Update the live hp of the player in percentages

                # Player Coords
                currentPlayerLocation = findCoordsOnMiniMap(playerIcon)
                if currentPlayerLocation is not None:
                    self.setPlayerCoords(currentPlayerLocation)
                    gui.updateCurrentCoordinate(currentPlayerLocation)  # Update the live coords in gui

                if gui.autoRuneSolver.get() == 1:  # Check if checkbutton is checked
                    # Search for rune
                    runeCoords = findCoordsOnMiniMap(runeIcon)
                    if runeCoords is not None:
                        self.setRuneCoords(runeCoords)

                if gui.randomPlayerNotification.get() == 1:
                    # Search for random players
                    randomPlayerCoords = findCoordsOnMiniMap(randomIcon)
                    if randomPlayerCoords is not None:
                        if self.randomPlayerTimer is None:
                            self.randomPlayerTimer = time.time()  # First time when random player is in map
                        else:
                            if time.time() - RANDOM_PLAYER_NOTIFICATION > self.randomPlayerTimer:
                                self.setRandomPlayerInMap(True)
                    else:
                        self.randomPlayerTimer = None
                        self.setRandomPlayerInMap(False)

                if gui.friendPlayerNotification.get() == 1:
                    # Search for friends players
                    friendPlayerCoords = findCoordsOnMiniMap(friendIcon)
                    if friendPlayerCoords is not None:
                        if self.friendPlayerTimer is None:
                            self.friendPlayerTimer = time.time()  # First time when random player is in map
                        else:
                            if time.time() - RANDOM_PLAYER_NOTIFICATION > self.friendPlayerTimer:
                                self.setFriendPlayerInMap(True)
                    else:
                        self.friendPlayerTimer = None
                        self.setFriendPlayerInMap(False)


def getHpInPercentageFromImage():
    hpBarImage = screenManager.getHpBarScreenshot()
    width, height = hpBarImage.size
    hpBarHeight = None
    hpBarFirst = None
    hpBarLast = None
    rgbPixel = None
    for x in range(width):
        if hpBarHeight is None:
            for y in range(height):
                coordinate = x, y
                rgbPixel = hpBarImage.getpixel(coordinate)
                hsvPixel = utils.rgbToHsv(rgbPixel)
                if 342 >= hsvPixel[0] >= 333 and hsvPixel[1] > .5:
                    hpBarHeight = y
                    hpBarFirst = x
                    break
        elif hpBarLast is None:
            coordinate = x, hpBarHeight
            hsvPixel = utils.rgbToHsv(hpBarImage.getpixel(coordinate))
            if not (342 >= hsvPixel[0] >= 333 and hsvPixel[1] > .5):
                if 100 > rgbPixel[1] < 150 and hsvPixel[0] < 300:
                    hpBarLast = x
                    break
        else:
            break

    # If couldn't find end of red bar
    if hpBarLast is None:
        hpBarLast = width

    if hpBarHeight is not None and hpBarLast is not None and width > 0:
        return int((hpBarLast - hpBarFirst) * 100 / int(width - hpBarFirst))
    return None


def findCoordsOnMiniMap(innerIcon):
    miniMapImage = screenManager.getMiniMapScreenshot()
    innerIconArr = numpy.asarray(innerIcon)
    miniMapArr = numpy.asarray(miniMapImage)

    innerIconArr_y, innerIconArr_x = innerIconArr.shape[:2]
    miniMapArr_y, miniMapArr_x = miniMapArr.shape[:2]

    stopX = miniMapArr_x - innerIconArr_x + 1
    stopY = miniMapArr_y - innerIconArr_y + 1

    for x in range(0, stopX):
        for y in range(0, stopY):
            x2 = x + innerIconArr_x
            y2 = y + innerIconArr_y
            pic = miniMapArr[y:y2, x:x2]
            test = (pic == innerIconArr)
            if test.all():
                return utils.Point(x, y)
    return None
