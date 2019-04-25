from os.path import expanduser

class command():
    def __init__(self, dragonfmManager):
        self.dragonfmManager = dragonfmManager
        self.screen = self.dragonfmManager.getScreen()
        self.settingsManager = self.dragonfmManager.getSettingsManager()
        self.viewManager = None
    def shutdown(self):
        pass
    def getName(self):
        return _('Goto Root')
    def getDescription(self):
        return _('Goto root folder')
    def active(self):
        return True
    def getValue(self):
        return None
    def getShortcut(self):
        return None
    def run(self, callback = None):
        folderManager = self.dragonfmManager.getCurrFolderManager()
        folderManager.gotoFolder('/')
        if callback:
            callback()
