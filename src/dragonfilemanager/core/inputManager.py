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
        self.screen.timeout(0)
        while True:
            key = self.screen.getch()
            if key == curses.ERR:
                break
            key = curses.keyname(key).decode("utf-8")
            keys += key
        self.screen.timeout(150)
        #keys = self.unifyKey(keys)
        return str(keys)
    def unifyKey(self, keys):
        newKey = ''
        if not keys:
            return newKey
        if keys == '':
            return newKey
        for k in keys:
            if ord(k) == 9:
                newKey += 'KEY_TAB'
            elif (len(keys) > 1) and (ord(k) == 33):
                newKey += 'KEY_TAB'
            else:
                newKey += k
        return newKey
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
