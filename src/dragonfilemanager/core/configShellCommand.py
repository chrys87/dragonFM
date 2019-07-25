from dragonfilemanager.core.command import command

class configShellCommand(command):
    def __init__(self, dragonfmManager,  category, name = '', description = '', internal = True):
        command.__init__(self, dragonfmManager, name, description)
        self.processManager = self.dragonfmManager.getProcessManager()
        self.selectionManager = self.dragonfmManager.getSelectionManager()
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
        print(cmd)
        if not cmd:
            return
        if cmd == '':
            return
        try:
            if self.getInternal():
                self.processManager.startInternal(cmd)
            else:
                self.processManager.startExternal(cmd)
        except Exception as e:
            self.dragonfmManager.setMessage('could not start: {0} Error: {1}'.format(cmd, e))


'''
    def getCmd(self, setting):
        cmd = None
        try:
            cmd = self.settingsManager.get(self.getCategory(), setting)
        except:
            return None
        return cmd
    def replaceParameters(self, rawCmd):
        cmd = rawCmd
        try:
            selected = self.selectionManager.getSelectionOrCursorCurrentTab()
            countSelected = len(selected)
            if countSelected == 0:
                self.dragonfmManager.setMessage('No files selected')
                return
            fileParameter = ' '.join('"{0}"'.format(e) for e in selected)
            cmd = cmd.format(fileParameter)
        except:
            return None
        return cmd
'''
