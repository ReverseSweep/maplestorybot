import imageloader
import utils
import screenManager
import gui
import gameMonitor
import botHandler
import threadManager

# Instance
gameMonitorInstance = gameMonitor.GameMonitor()

# Threads
gameMonitorThread = threadManager.Thread('monitor', gameMonitorInstance.start)
botThread = threadManager.Thread('bot', botHandler.startBot)


def startButtonClick():
    if screenManager.screen.getHpBarPos() is None or screenManager.screen.getMiniMapPos() is None:
        print('You have to initialize the required fields..')

    else:
        if gameMonitorThread.isRunning() and gameMonitorThread.isStarted:  # Started and running
            threadManager.stopThread('monitor')  # Stopping the while loop by changing the inner property of the thread
            threadManager.stopThread('bot')  # Stopping the while loop by changing the inner property of the thread
        else:
            if not gameMonitorThread.isStarted:
                gameMonitorThread.start()
                botThread.start()
            else:
                gameMonitorThread.setIsRunning(True)
                botThread.setIsRunning(True)

        # Update status to gui
        gui.updateBotStatus(gameMonitorThread.isRunning())


def initButtonClick():
    if screenManager.screen.getHpBarPos() is None:
        utils.loadImageWindow("HP bar", imageloader.loadImageClick, None, None)
    elif screenManager.screen.getMiniMapPos() is None:
        utils.loadImageWindow("Mini map", imageloader.loadImageClick, None, None)
    else:
        print('Everything is already loaded...')


def updateLoadedImageToScreen(imagePos):
    if screenManager.screen.getHpBarPos() is None:
        screenManager.screen.setHpBarPos(imagePos)
        gui.updateHpBarLabel()
    elif screenManager.screen.getMiniMapPos() is None:
        screenManager.screen.setMiniMapPos(imagePos)
        gui.updateMiniMapLabel()
    else:
        print('ERROR: how did you got here?')
