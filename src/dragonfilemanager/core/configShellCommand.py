from dragonfilemanager.core.command import command

class configShellCommand(command):
    def __init__(self, dragonfmManager,  category, name = '', description = '', internal = True):
        command.__init__(self, dragonfmManager, name, description)
        self.processManager = self.dragonfmManager.getProcessManager()
        self.selectionManager = self.dragonfmManager.getSelectionManager()
        self.fileManager = self.dragonfmManager.getFileManager()
        self.category = category
        self.internal = internal
    def setCategory(self, category):
        self.category = category
    def setInternal(self, internal):
        self.internal = internal
    def getCategory(self):
        return self.category
    def getInternal(self):
        return self.internal
    def run(self, cmd, callback = None):
        if not cmd:
            return
        if cmd == '':
            return
        try:
            if self.getInternal():
                self.processManager.startInternalShell(cmd, name = self.name, description = self.description)
            else:
                self.processManager.startExternal(cmd)
        except Exception as e:
            self.dragonfmManager.setMessage('could not start: {0} Error: {1}'.format(cmd, e))
