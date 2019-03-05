import sys, os, curses

class startUpManager():
    def __init__(self, dragonfmManager):
        self.dragonfmManager = dragonfmManager
        self.screen = self.dragonfmManager.getScreen()
        self.settingsManager = self.dragonfmManager.getSettingsManager()

    def start(self, application = '', pwd = ''):
        if application == '':
            return
        if pwd != '' and os.access(pwd, os.R_OK):
            os.chdir(pwd)
        self.dragonfmManager.leave()
        try:
            os.system(application)
        except:
            pass
        self.dragonfmManager.enter()
