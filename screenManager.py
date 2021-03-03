from PIL import ImageGrab


class Screen:
    def __init__(self, hpBarPos=None, miniMapPos=None):
        self.hpBarPos = hpBarPos
        self.miniMapPos = miniMapPos

    def setHpBarPos(self, pos):
        self.hpBarPos = pos

    def getHpBarPos(self):
        return self.hpBarPos

    def setMiniMapPos(self, pos):
        self.miniMapPos = pos

    def getMiniMapPos(self):
        return self.miniMapPos


screen = Screen()


def getHpBarScreenshot():
    if screen.getHpBarPos() is None:
        print('ERROR: HPbar object is None')
    else:
        hpBarPos = screen.getHpBarPos()
        screenshotOfPos = ImageGrab.grab(bbox=(hpBarPos[0].x, hpBarPos[0].y, hpBarPos[1].x, hpBarPos[1].y))
        return screenshotOfPos


def getMiniMapScreenshot():
    if screen.getMiniMapPos() is None:
        print('ERROR: MiniMap object is None')
    else:
        miniMapPos = screen.getMiniMapPos()
        screenshotOfPos = ImageGrab.grab(bbox=(miniMapPos[0].x, miniMapPos[0].y, miniMapPos[1].x, miniMapPos[1].y))

        return screenshotOfPos
