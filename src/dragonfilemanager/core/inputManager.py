import sys, os, curses, time

class inputManager():
    def __init__(self, dragonfmManager):
        self.dragonfmManager = dragonfmManager
        self.screen = self.dragonfmManager.getScreen()
        self.settingsManager = self.dragonfmManager.getSettingsManager()
    def get(self):
        if not self.screen:
            return None
        keys = []
        key = curses.ERR
        self.screen.nodelay(False)
        key = self.screen.getch()
        keys.append(chr(key))
        keys.append('sep')
        self.screen.nodelay(True)
        wait = time.time()
        while True:
            key = self.screen.getch()
            if key == curses.ERR:
                break
            keys.append(chr(key))
        self.screen.nodelay(False)
        return str(keys)
            
