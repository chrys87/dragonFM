from dragonfilemanager.core.baseCommand import baseCommand

class command(baseCommand):
    def __init__(self, dragonfmManager):
        baseCommand.__init__(self, dragonfmManager)
        self.dragonfmManager = dragonfmManager
        self.dragonfmManager = dragonfmManager
        self.screen = self.dragonfmManager.getScreen()
        self.settingsManager = self.dragonfmManager.getSettingsManager()
        self.setName('Previous Entry use mode')
        self.setDescription('Move Cursor to previous entry using current mode')
    def run(self, callback = None):
        listManager = self.dragonfmManager.getCurrListManager()
        listManager.prevEntry()
        # unselection mode
        if listManager.getSelectionMode() == 0:
            listManager.unselectAllEntries()
        # selection mode
        elif listManager.getSelectionMode() == 1:
            listManager.selectCurrentEntry()
        # ignore mode
        elif listManager.getSelectionMode() == 2:
            pass
        if callback:
            callback()
