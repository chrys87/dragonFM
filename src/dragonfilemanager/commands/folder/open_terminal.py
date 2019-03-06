
import shlex

class command():
    def __init__(self, dragonfmManager):
        self.dragonfmManager = dragonfmManager
        self.screen = self.dragonfmManager.getScreen()
        self.settingsManager = self.dragonfmManager.getSettingsManager()
        self.processManager = self.dragonfmManager.getProcessManager()
        self.viewManager = None
    def shutdown(self):
        pass
    def getName(self):
        return _('Open Terminal')
    def getDescription(self):
        return _('Open current location in terminal')
    def active(self):
        return True
    def getValue(self):
        return None
    def getShortcut(self):
        return None
    def run(self, callback = None):
        if self.viewManager == None:
            self.viewManager = self.dragonfmManager.getViewManager()
        terminalcmd = self.settingsManager.get('application', 'commandline')
        if terminalcmd == '':
            return
        location = self.viewManager.getCurrentTab().getFolderManager().getLocation()
        terminalcmd = terminalcmd.format(shlex.quote(location))
        self.processManager.startExternal(terminalcmd)
        if callback:
            callback()
