import sys, os, curses

class startUpManager():
    def __init__(self, dragonfmManager):
        self.dragonfmManager = dragonfmManager
        self.screen = self.dragonfmManager.getScreen()
        self.settingsManager = self.dragonfmManager.getSettingsManager()

    def start(self, application = ''):
        if application == '':
            return
        self.dragonfmManager.leave()
        try:
            os.system(application)
        except:
            pass
        self.dragonfmManager.enter()
