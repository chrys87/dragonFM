from dragonfilemanager.core.baseCommand import baseCommand

class command(baseCommand):
    def __init__(self, dragonfmManager):
        baseCommand.__init__(self, dragonfmManager)
        self.dragonfmManager = dragonfmManager
        self.screen = self.dragonfmManager.getScreen()
        self.settingsManager = self.dragonfmManager.getSettingsManager()
        self.setName('Open Entry')
        self.setDescription('Opens the current entry')
    def active(self):
        return self.commandManager.isCommandValidForFileOperation(minSelection = 1)
    def run(self, callback = None):
        listManager = self.dragonfmManager.getCurrListManager()
        currentEntry = listManager.getCurrentEntry()
        if not currentEntry:
            return
        currPath = ''
        try:
            currPath = currentEntry['full']
        except:
            return
        if currPath == '':
            return
        listManager.openEntry(currPath, entry=currentEntry)
        if callback:
            callback()
