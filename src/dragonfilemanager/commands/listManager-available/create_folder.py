from dragonfilemanager.core.baseCommand import baseCommand

class command(baseCommand
    def __init__(self, dragonfmManager):
        baseCommand.__init__(self, dragonfmManager)
        self.dragonfmManager = dragonfmManager
        self.settingsManager = self.dragonfmManager.getSettingsManager()
        self.fileManager = self.dragonfmManager.getFileManager()
        self.setName('Create Folder')
        self.setDescription('Create a new folder')
    def active(self):
        return self.commandManager.isCommandValidForFileOperation()
    def run(self, callback = None):   
        listManager = self.dragonfmManager.getCurrListManager()
        location = listManager.getLocation()
        folderName = self.fileManager.getInitName(location, 'new_folder{0}{1}{2}', '_')

        inputDialog = self.dragonfmManager.createInputDialog(description = ['Foldername:'])
        inputDialog.setDefaultValue(folderName)

        exitStatus, folderName = inputDialog.show()
        if not exitStatus:
            return

        if not location.endswith('/'):
            location += '/'
        fullPath = '{0}{1}'.format(location, folderName)
        self.fileManager.spawnCreateFolderThread(fullPath)
        if callback:
            callback()
