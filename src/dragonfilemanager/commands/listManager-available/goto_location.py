from dragonfilemanager.core.baseCommand import baseCommand
from os.path import expanduser

class command(baseCommand):
    def __init__(self, dragonfmManager):
        baseCommand.__init__(self, dragonfmManager)
        self.dragonfmManager = dragonfmManager
        self.screen = self.dragonfmManager.getScreen()
        self.settingsManager = self.dragonfmManager.getSettingsManager()
        self.setName('Goto Location')
        self.setDescription('Open an dialog and goto location')
    def active(self):
        return self.commandManager.isCommandValidForFileOperation()
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
