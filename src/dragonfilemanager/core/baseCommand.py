class baseCommand():
    def __init__(self, dragonfmManager, name = '', description = ''):
        self.dragonfmManager = dragonfmManager
        self.screen = self.dragonfmManager.getScreen()
        self.settingsManager = self.dragonfmManager.getSettingsManager()
        self.commandManager = self.dragonfmManager.getCommandManager()
        self.name = name
        self.description = description
    def shutdown(self):
        pass
    def setName(self, name):
        self.name = name
    def getName(self):
        if self.name == '':
            return _('No description found')
        else:
            return _(self.name)
    def setDescription(self, description):
        self.description = description
    def getDescription(self):
        if self.description == '':
            return _('No description found')
        else:
            return _(self.description)
    def active(self):
        return True
    def visible(self):
        return True
    def getValue(self):
        return None
    def getShortcut(self):
        return None
    def run(self, callback = None):
        pass
