import sys, os, curses, time

class inputManager():
    def __init__(self, dragonfmManager):
        self.dragonfmManager = dragonfmManager
        self.screen = self.dragonfmManager.getScreen()
        self.settingsManager = self.dragonfmManager.getSettingsManager()
    def get(self):
        if not self.screen:
            return None
        keys = ''
        key = self.screen.getch()
        if key == curses.ERR:
            return None
        keys = curses.keyname(key).decode("utf-8") 
        self.screen.timeout(1)
        while True:
            key = self.screen.getch()
            if key == curses.ERR:
                break
            key = curses.keyname(key).decode("utf-8")
            keys += ',{0}'.format(key)
        self.screen.timeout(150)

        return str(keys)
    def getKey(self):
        if not self.screen:
            return None
        key = self.screen.getch()
        key = curses.keyname(key).decode("utf-8")
        return key
    def getSequenceAsList(self):
        if not self.screen:
            return None
        keys = []
        key = curses.ERR
        self.screen.nodelay(False)
        key = self.screen.getch()
        keys.append(chr(key))
        self.screen.nodelay(True)
        while True:
            key = self.screen.getch()
            if key == curses.ERR:
                break
            keys.append(chr(key))
        self.screen.nodelay(False)
        return str(keys)
            
