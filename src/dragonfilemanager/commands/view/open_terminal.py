
import os, shlex
class command():
    def __init__(self, dragonfmManager):
        self.dragonfmManager = dragonfmManager
        self.screen = self.dragonfmManager.getScreen()
        self.settingsManager = self.dragonfmManager.getSettingsManager()
        self.startUpManager = self.dragonfmManager.getStartUpManager()
        self.viewManager = None
    def shutdown(self):
        pass
    def getName(self):
        return _('Open Terminal')
    def getDescription(self):
        return _('Open current Tab in terminal')
    def active(self):
        return True
    def getValue(self):
        return None
    def getShortcut(self):
        return None
    def run(self, callback = None):
        if self.viewManager == None:
            self.viewManager = self.dragonfmManager.getViewManager()
        location = self.viewManager.getCurrentTab().getLocation()
        terminalcmd = self.settingsManager.get('application', 'commandline')
        terminalcmd = terminalcmd.format(shlex.quote(location))
        self.startUpManager.start(terminalcmd)
        if callback:
            callback()
