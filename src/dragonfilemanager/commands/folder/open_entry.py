class command():
    def __init__(self, dragonfmManager):
        self.dragonfmManager = dragonfmManager
        self.screen = self.dragonfmManager.getScreen()
        self.settingsManager = self.dragonfmManager.getSettingsManager()
    def shutdown(self):
        pass
    def getName(self):
        return _('Open Entry')
    def getDescription(self):
        return _('Opens the current entry')
    def active(self):
        return True
    def getValue(self):
        return None
    def getShortcut(self):
        return None
    def run(self, callback = None):
        folderManager = self.dragonfmManager.getCurrFolderManager()
        currentEntry = folderManager.getCurrentEntry()
        if not currentEntry:
            return
        currPath = ''
        try:
            currPath = currentEntry['full']
        except:
            return
        if currPath == '':
            return
        folderManager.openEntry(currPath, entry=currentEntry)
        if callback:
          callback()
