from dragonfilemanager.core.baseCommand import baseCommand

class command(baseCommand):
    def __init__(self, dragonfmManager):
        baseCommand.__init__(self, dragonfmManager)
        self.dragonfmManager = dragonfmManager
        self.screen = self.dragonfmManager.getScreen()
        self.settingsManager = self.dragonfmManager.getSettingsManager()
        self.selectionManager = self.dragonfmManager.getSelectionManager()
        self.setName('Open Details')
        self.setDescription('Opens the Details')
    def active(self):
        return self.commandManager.isCommandValidForFileOperation(minSelection = 1)
    def run(self, callback = None):
        tabManager = self.dragonfmManager.getViewManager().getCurrentTab()
        detailManager = tabManager.getDetailManager()
        elements = self.selectionManager.getSelectionOrCursorCurrentTab()
        detailManager.setDetails(elements)
        detailManager.loadMenu()
        tabManager.changeMode(1) # details
        if callback:
            callback()
