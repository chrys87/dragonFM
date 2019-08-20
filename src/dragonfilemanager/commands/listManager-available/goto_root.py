from dragonfilemanager.core.baseCommand import baseCommand
from os.path import expanduser

class command(baseCommand):
    def __init__(self, dragonfmManager):
        baseCommand.__init__(self, dragonfmManager)
        self.dragonfmManager = dragonfmManager
        self.screen = self.dragonfmManager.getScreen()
        self.settingsManager = self.dragonfmManager.getSettingsManager()
        self.viewManager = None
        self.setName('Goto Root')
        self.setDescription('Goto root folder')
    def run(self, callback = None):
        listManager = self.dragonfmManager.getCurrListManager()
        listManager.gotoFolder('/')
        if callback:
            callback()
