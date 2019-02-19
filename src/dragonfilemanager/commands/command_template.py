class command():
    def __init__(self, dragonfmManager):
        self.dragonfmManager = dragonfmManager
        self.screen = self.dragonfmManager.getScreen()
        self.settingsManager = self.dragonfmManager.getSettingsManager()
    def shutdown(self):
        pass
    def getName(self):
        return 'No description found'
    def getDescription(self):
        return 'No description found'         
    def active(self):
        return True
    def run(self, callback):
        if callback:
          callback()
