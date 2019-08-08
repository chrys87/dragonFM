from dragonfilemanager.core.baseCommand import baseCommand

class command(baseCommand):
    def __init__(self, dragonfmManager):
        baseCommand.__init__(self, dragonfmManager)
        self.dragonfmManager = dragonfmManager
        self.settingsManager = self.dragonfmManager.getSettingsManager()
        self.fileManager = self.dragonfmManager.getFileManager()
        self.setName('Create File')
        self.setDescription('Create a new file')
    def active(self):
        return self.commandManager.isCommandValidForFileOperation()
    def run(self, callback = None):   
        listManager = self.dragonfmManager.getCurrListManager()
        location = listManager.getLocation()
        fileName = self.fileManager.getInitName(location, 'new_file{0}{1}{2}.txt', '_')

        inputDialog = self.dragonfmManager.createInputDialog(description = ['Filename:'])
        inputDialog.setDefaultValue(fileName)
        exitStatus, fileName = inputDialog.show()
        if not exitStatus:
            return

        if not location.endswith('/'):
            location += '/'
        fullPath = '{0}{1}'.format(location, fileName)
        self.fileManager.spawnCreateFileThread(fullPath)
        if callback:
            callback()
