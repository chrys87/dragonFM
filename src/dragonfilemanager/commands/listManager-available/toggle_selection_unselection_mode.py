from dragonfilemanager.core.baseCommand import baseCommand

class command(baseCommand):
    def __init__(self, dragonfmManager):
        baseCommand.__init__(self, dragonfmManager)
        self.dragonfmManager = dragonfmManager
        self.screen = self.dragonfmManager.getScreen()
        self.settingsManager = self.dragonfmManager.getSettingsManager()
        self.setName('toggle selection / unselection')
        self.setDescription('toggle selection / unselection on navigation')
    def active(self):
        return self.commandManager.isCommandValidForFileOperation()
    def run(self, callback = None):
        listManager = self.dragonfmManager.getCurrListManager()
        if listManager.getSelectionMode() == 0:
            listManager.setSelectionMode(1)
            listManager.selectCurrentEntry()
        else:
            listManager.setSelectionMode(0)
            listManager.unselectAllEntries()
        if callback:
            callback()
