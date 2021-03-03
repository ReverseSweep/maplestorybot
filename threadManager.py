import threading


class Thread(threading.Thread):
    def __init__(self, name, func, args=()):
        super().__init__()
        self.name = name
        self.running = False
        self.isStarted = False
        self.func = func
        self.args = args

        self.setDaemon(True)  # Daemon is true

    def isRunning(self):
        return self.running

    def run(self):
        print('{0} thread has started!'.format(self.name))
        self.isStarted = True  # Thread has been started (at least once) flag
        self.running = True  # Start bot flag
        threads.append(self)
        self.func(*self.args)

    def setIsRunning(self, isRunning):
        self.running = isRunning
        threadMessage = 'started' if isRunning else 'stopped'
        print('{0} thread has {1}!'.format(self.name, threadMessage))


threads = []


def stopThread(name):
    for t in threads:
        if t.name == name:
            print('{0} thread has stopped!'.format(t.name))
            t.running = False
