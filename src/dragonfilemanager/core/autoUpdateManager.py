import threading, time
#import inotify, inotify.adapters
from inotify_simple import INotify, flags


'''
# all events
self.DRAGON_INOTIFY_EVENTS = (inotify.constants.IN_ACCESS |
    inotify.constants.IN_MODIFY |inotify.constants.IN_ATTRIB |
    inotify.constants.IN_CLOSE_WRITE | inotify.constants.IN_CLOSE_NOWRITE |
    inotify.constants.IN_OPEN | inotify.constants.IN_MOVED_FROM |
    inotify.constants.IN_MOVED_TO | inotify.constants.IN_CREATE |
    inotify.constants.IN_DELETE | inotify.constants.IN_DELETE_SELF |
    inotify.constants.IN_MOVE_SELF
)
'''

class autoUpdateManager():
    def __init__(self, dragonfmManager):
        self.dragonfmManager = dragonfmManager
        self.settingsManager = self.dragonfmManager.getSettingsManager()
        #self.DRAGON_INOTIFY_EVENTS = (
        #    inotify.constants.IN_MODIFY |inotify.constants.IN_ATTRIB |
        #    inotify.constants.IN_CLOSE_WRITE |
        #    inotify.constants.IN_MOVED_FROM |
        #    inotify.constants.IN_MOVED_TO | inotify.constants.IN_CREATE |
        #    inotify.constants.IN_DELETE | inotify.constants.IN_DELETE_SELF |
        #    inotify.constants.IN_MOVE_SELF
        #)
        self.DRAGON_INOTIFY_EVENTS = (
            flags.MODIFY |flags.ATTRIB |
            flags.CLOSE_WRITE |
            flags.MOVED_FROM |
            flags.MOVED_TO | flags.CREATE |
            flags.DELETE | flags.DELETE_SELF |
            flags.MOVE_SELF
        )
        self.watchdog = None
        self.watchdogLock = threading.RLock()
        self.notificationLock = threading.RLock()
        self.location = ''
        self.watchdogThread = None

    def startWatch(self, location, callback):
        self.watchdogLock.acquire(True)
        if self.watchdog != None:
            self.watchdogLock.release()
            return
        if self.location != '':
            self.watchdogLock.release()
            return
        self.location = location
        #self.watchdog = inotify.adapters.Inotify(block_duration_s = 0.2)
        #self.watchdog.add_watch(location, mask=self.DRAGON_INOTIFY_EVENTS)
        self.watchdog = INotify(nonblocking=True)
        self.watchdog.add_watch(location, mask=self.DRAGON_INOTIFY_EVENTS)
        self.watchdogLock.release()
        self.watchdogThread = threading.Thread(
            target=self.watchThread, args=[callback]
        )
        self.watchdogThread.start()
    def requestStop(self):
        self.watchdogLock.acquire(True)
        # something wents wrong, fix it
        if self.location == '':
            self.watchdog == None
            self.watchdogLock.release()
            return
        if self.watchdog == None:
            self.location == ''
            self.watchdogLock.release()
            return
        # request the stop
        oldLocation = self.location
        self.location = ''
        if oldLocation != '':
            try:
                #self.watchdog.remove_watch(oldLocation)
                self.watchdog.rm_watch(oldLocation)
            except:
                pass
        self.watchdogLock.release()
    def waitForStopWatch(self):
        try:
            if self.watchdogThread != None:
                self.watchdogThread.join()
        except:
            pass
        self.watchdogLock.acquire(True)
        self.watchdog = None
        self.watchdogThread = None
        self.watchdogLock.release()

    def watchThread(self, callback):
        wasChange = False
        lastChangeTime = time.time()
        while self.dragonfmManager.getRunning():
            self.watchdogLock.acquire(True)
            if self.location == '':
                self.watchdogLock.release()
                return
            #events = self.watchdog.event_gen(yield_nones=False, timeout_s=0.1)
            events = self.watchdog.read(timeout=0.01, read_delay=0.001)
            self.watchdogLock.release()
            if events == None:
                events = []
            elementList = list(events)
            if elementList != []:
                wasChange = True
                lastChangeTime = time.time()
            if wasChange:
                if (time.time() - lastChangeTime) > 0.4:
                    wasChange = False
                    callback()
