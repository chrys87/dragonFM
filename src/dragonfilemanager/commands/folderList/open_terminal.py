
import shlex

class command():
    def __init__(self, dragonfmManager):
        self.dragonfmManager = dragonfmManager
        self.screen = self.dragonfmManager.getScreen()
        self.settingsManager = self.dragonfmManager.getSettingsManager()
        self.processManager = self.dragonfmManager.getProcessManager()
    def shutdown(self):
        pass
    def getName(self):
        return _('Open Terminal')
    def getDescription(self):
        return _('Open current location in terminal')
    def active(self):
        return True
    def visible(self):
        return True
    def getValue(self):
        return None
    def getShortcut(self):
        return None
    def run(self, callback = None):
        terminalcmd = self.settingsManager.get('application', 'commandline')
        if terminalcmd == '':
            return
        listManager = self.dragonfmManager.getCurrListManager()
        location = listManager.getLocation()
        self.processManager.startExternal(terminalcmd, location)
        if callback:
            callback()
