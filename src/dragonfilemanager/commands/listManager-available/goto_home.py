from dragonfilemanager.core.baseCommand import baseCommand
from os.path import expanduser

class command(baseCommand):
    def __init__(self, dragonfmManager):
        baseCommand.__init__(self, dragonfmManager)
        self.dragonfmManager = dragonfmManager
        self.screen = self.dragonfmManager.getScreen()
        self.settingsManager = self.dragonfmManager.getSettingsManager()
        self.setName('Goto Home')
        self.setDescription('Goto Home folder')
    def run(self, callback = None):
        listManager = self.dragonfmManager.getCurrListManager()
        listManager.gotoFolder(expanduser("~"))
        if callback:
            callback()
