from dragonfilemanager.core.baseConfigShellCommand import baseConfigShellCommand

class command(baseConfigShellCommand):
    def __init__(self, dragonfmManager):
        baseConfigShellCommand.__init__(self, dragonfmManager, 'decompress', 'decompress', 'decompress a archive', True)
    def active(self):
        return self.commandManager.isCommandValidForFileOperation(minSelection = 1, writePerm = True)
    def run(self, callback = None):
        # Get the current cursor 
        currCursor = self.selectionManager.getCursorCurrentTab()
        if currCursor == '':
            self.dragonfmManager.setMessage('No file for deccompression')
            return

        listManager = self.dragonfmManager.getCurrListManager()
        location = listManager.getLocation()
        fileInfo = self.fileManager.getInfo(currCursor)
        fileMimeType = fileInfo['mime']
        fileName = fileInfo['nameOnly']

        folderName = fileName + '{0}{1}{2}'
        folderName = self.fileManager.getInitName(location, folderName, '_')

        folderName = location + '/' + folderName
        self.fileManager.createFolder(folderName)

        cmd = self.settingsManager.get(self.getCategory(), fileMimeType)

        super().run(cmd.format(currCursor, folderName))
        if callback:
            callback()
