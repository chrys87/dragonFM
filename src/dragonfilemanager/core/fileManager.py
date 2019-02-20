import sys, os, curses

class fileManager():
    def __init__(self, dragonfmManager):
        self.dragonfmManager = dragonfmManager
        self.screen = self.dragonfmManager.getScreen()
        self.settingsManager = self.dragonfmManager.getSettingsManager()
    def self.getInfo(fullPath):
        info = None
        cleanFullPath = fullPath
        if cleanFullPath.endswith('/'):
            cleanFullPath = cleanFullPath[:-1]
        name = os.path.basename(cleanFullPath)
        entry = {'name': name,
         'full': fullPath,
         'path': path,
        }
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
        if os.path.isfile(fullPath):
            entry['type'] = 'file'
        elif os.path.isdir(fullPath):
            entry['type'] = 'directory'
        elif os.path.islink(fullPath):
            entry['type'] = 'link'
        elif os.path.ismount(fullPath):
            entry['type'] = 'mountpoint'
