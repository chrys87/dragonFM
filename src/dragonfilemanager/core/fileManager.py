import sys, os, curses

class fileManager():
    def __init__(self, dragonfmManager):
        self.dragonfmManager = dragonfmManager
        self.screen = self.dragonfmManager.getScreen()
        self.settingsManager = self.dragonfmManager.getSettingsManager()
    def getInfo(self, fullPath):
        # basic
        name = os.path.basename(fullPath)
        path = os.path.dirname(fullPath)
        entry = {'name': name,
         'full': fullPath,
         'path': path,
        }
        # type
        if os.path.isfile(fullPath):
            entry['type'] = 'file'
        elif os.path.isdir(fullPath):
            entry['type'] = 'directory'
        elif os.path.islink(fullPath):
            entry['type'] = 'link'
        elif os.path.ismount(fullPath):
            entry['type'] = 'mountpoint'
        # details
        info = None
        try:
            info = os.stat(fullPath)
        except:
            info = None
        if info:
            try:
                entry['info'] = info
            except:
                pass
    def openFile(self, fullPath):
        try:
            os.execlp('nano', 'nano', fullPath)
        except:
            return False
        return True
