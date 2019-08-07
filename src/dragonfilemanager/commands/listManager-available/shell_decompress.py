from dragonfilemanager.core.baseConfigShellCommand import baseConfigShellCommand

class command(baseConfigShellCommand):
    def __init__(self, dragonfmManager):
        baseConfigShellCommand.__init__(self, dragonfmManager, 'decompress', 'decompress', 'decompress a archive', True)
    def active(self):
        # only allowed for mimetypes it could handle
        allowedMimeTypes = []
        # coded as own setting in settings file
        #try:
        #    allowedMimeTypes = self.settingsManager.get('folder', #'shell_decompress_mimetypes_allowed').lower().split(',')
        #except Exception as e:
        #    allowedMimeTypes = []
        
        # for this case we can get it from decompress category
        try:
            allowedMimeTypes = self.settingsManager.getSettingsForCategory('decompress')
        except Exception as e:
            pass
        return self.commandManager.isCommandValidForFileOperation(minSelection = 1, writePerm = True, mimeTypes=allowedMimeTypes)
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
