from dragonfilemanager.core.baseCommand import baseCommand

class command(baseCommand):
    def __init__(self, dragonfmManager):
        baseCommand.__init__(self, dragonfmManager)
        self.dragonfmManager = dragonfmManager
        self.screen = self.dragonfmManager.getScreen()
        self.settingsManager = self.dragonfmManager.getSettingsManager()
        self.setName('Reset')
        self.setDescription('Reset All')
    def run(self, callback = None):
        listManager = self.dragonfmManager.getCurrListManager()
        listManager.setSelectionMode(0)
        listManager.resetTypeAheadSearch(True)
        listManager.unselectAllEntries()
        if listManager.getCollectorLocation() != '':
            listManager.setLocation(listManager.getCollectorLocation())
        self.dragonfmManager.erase()
        listManager.setCollector()
        listManager.setRequestReload()
        if callback:
            callback()
