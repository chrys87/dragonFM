from os.path import expanduser

class command():
    def __init__(self, dragonfmManager):
        self.dragonfmManager = dragonfmManager
        self.screen = self.dragonfmManager.getScreen()
        self.settingsManager = self.dragonfmManager.getSettingsManager()
    def shutdown(self):
        pass
    def getName(self):
        return _('Goto Location')
    def getDescription(self):
        return _('Open an dialog and goto location')
    def active(self):
        return True
    def visible(self):
        return True
    def getValue(self):
        return None
    def getShortcut(self):
        return None
    def run(self, callback = None):
        listManager = self.dragonfmManager.getCurrListManager()
        location = listManager.getLocation()
        inputDialog = self.dragonfmManager.createInputDialog(description = ['Location:'], initValue = location)
        inputDialog.setLocationMode(True, location, True, False)
        exitStatus, location = inputDialog.show()
        if not exitStatus:
            return
        listManager.gotoFolder(location)
        if callback:
            callback()
