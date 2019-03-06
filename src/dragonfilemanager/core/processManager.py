import sys, os, curses

class processManager():
    def __init__(self, dragonfmManager):
        self.dragonfmManager = dragonfmManager
        self.screen = self.dragonfmManager.getScreen()
        self.settingsManager = self.dragonfmManager.getSettingsManager()
        self.externalStarted = False
        self.internalProcesses = {}
    def startInternal(self, type, description = '', process = None, postProcess = None):
        if process == None:
            return None
    def getNewProcessID(self):
        return 1
    def stopInternal(self, id):
        pass
    def isExternalStarted(self):
        return self.externalStarted
    def setExternalStarted(self, isExternalStarted):
        self.externalStarted = isExternalStarted
    def startExternal(self, application = '', pwd = ''):
        if application == '':
            return
        if pwd != '' and os.access(pwd, os.R_OK):
            os.chdir(pwd)
        self.dragonfmManager.leave()
        self.setExternalStarted(True)
        try:
            os.system(application)
        except:
            pass
        self.setExternalStarted(False)
        self.dragonfmManager.enter()
