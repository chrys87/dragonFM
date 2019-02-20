import sys, os, curses

class fileManager():
    def __init__(self, dragonfmManager):
        self.dragonfmManager = dragonfmManager
        self.screen = self.dragonfmManager.getScreen()
        self.settingsManager = self.dragonfmManager.getSettingsManager()
    def getInfo(fullPath):
        info = None
        try:
            info = os.stat(fullPath)
        except:
            pass
        entry = {'name': e,
         'full': fullPath,
         'path': path,
         'info': info
        }
        if os.path.isfile(fullPath):
            entry['type'] = 'file'
        elif os.path.isdir(fullPath):
            entry['type'] = 'directory'
        elif os.path.islink(fullPath):
            entry['type'] = 'link'
        elif os.path.ismount(fullPath):
            entry['type'] = 'mountpoint'
        '''
        / 	Directory
        * 	Executable
        | 	Fifo
        = 	Socket
        @ 	Symbolic Link
        @/ 	Symbolic Link to directory
        b 	Block Device
        c 	Character Device
        ? 	Unknown
        '''
