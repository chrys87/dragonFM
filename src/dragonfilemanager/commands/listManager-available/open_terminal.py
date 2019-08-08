from dragonfilemanager.core.baseCommand import baseCommand
import shlex

class command()baseCommand:
    def __init__(self, dragonfmManager):
        baseCommand.__init__(self, dragonfmManager)
        self.dragonfmManager = dragonfmManager
        self.screen = self.dragonfmManager.getScreen()
        self.settingsManager = self.dragonfmManager.getSettingsManager()
        self.processManager = self.dragonfmManager.getProcessManager()
        self.setName('Open Terminal')
        self.setDescription('Open current location in terminal')
    def active(self):
        return self.commandManager.isCommandValidForFileOperation()
    def run(self, callback = None):
        terminalcmd = self.settingsManager.get('application', 'commandline')
        if terminalcmd == '':
            return
        listManager = self.dragonfmManager.getCurrListManager()
        location = listManager.getLocation()
        self.processManager.startExternal(terminalcmd, location)
        if callback:
            callback()
