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
    def run(self, cmd, callback = None, preProcess = None, postProcess = None, pwd = '', preProcessParam = None, postProcessParam = None):
        if not cmd:
            return
        if cmd == '':
            return
        listManager = self.dragonfmManager.getCurrListManager()
        location = listManager.getLocation()
        try:
            if self.getInternal():
                self.processManager.startInternalShell(cmd, self.name,  self.description, preProcess, postProcess, location, preProcessParam, postProcessParam)
            else:
                self.processManager.startExternal(cmd, pwd = location)
        except Exception as e:
            self.dragonfmManager.setMessage('could not start: {0} Error: {1}'.format(cmd, e))
