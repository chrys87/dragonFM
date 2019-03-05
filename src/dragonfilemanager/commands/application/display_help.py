
import shlex

class command():
    def __init__(self, dragonfmManager):
        self.dragonfmManager = dragonfmManager
        self.screen = self.dragonfmManager.getScreen()
        self.startUpManager = self.dragonfmManager.getStartUpManager()
        self.viewManager = None
    def shutdown(self):
        pass
    def getName(self):
        return _('Display Help')
    def getDescription(self):
        return _('Documentation for DragonFM')
    def active(self):
        return True
    def getValue(self):
        return None
    def getShortcut(self):
        return "f1"
    def run(self, callback = None):
        if self.viewManager == None:
            self.viewManager = self.dragonfmManager.getViewManager()
        terminalcmd = self.settingsManager.get('application', 'commandline')
        if terminalcmd == '':
            return
        self.startUpManager.start('man dragonfm')
        if callback:
            callback()
