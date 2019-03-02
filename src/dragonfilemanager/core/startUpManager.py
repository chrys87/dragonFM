import sys, os, curses

class startUpManager():
    def __init__(self, dragonfmManager):
        self.dragonfmManager = dragonfmManager
        self.screen = self.dragonfmManager.getScreen()
        self.settingsManager = self.dragonfmManager.getSettingsManager()
        self.application = ''
        self.parameters = []
    def setPostProcessStartup(self, application):
        if len(application) == 0:
            return False
        self.application = application[0]
        self.parameters = application
        return True
    def execPostProcessStartup(self):
        if self.application == '':
            return
        sys.stdout.flush()
        os.execvp(self.application, self.parameters)
        #os.system(self.application)
