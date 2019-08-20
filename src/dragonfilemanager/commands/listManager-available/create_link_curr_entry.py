from dragonfilemanager.core.baseCommand import baseCommand
import os

class command(baseCommand):
    def __init__(self, dragonfmManager):
        baseCommand.__init__(self, dragonfmManager)
        self.dragonfmManager = dragonfmManager
        self.settingsManager = self.dragonfmManager.getSettingsManager()
        self.selectionManager = self.dragonfmManager.getSelectionManager()
        self.fileManager = self.dragonfmManager.getFileManager()
        self.setName('Create Link')
        self.setDescription('Create a link to the current entry')
    def active(self):
        return self.commandManager.isCommandValidForFileOperation(minSelection = 1, maxSelection = 1, writePerm = True)
    def run(self, callback = None):   
        listManager = self.dragonfmManager.getCurrListManager()
        
        # Get the files and directories that were selected.
        currentCursor = self.selectionManager.getCursorCurrentTab()
        if currentCursor == None:
            return
        if not os.path.exists(currentCursor):
            return
        filename_w_ext = os.path.basename(currentCursor)
        fileName, fileExtension = os.path.splitext(filename_w_ext)
        
        location = listManager.getLocation()
        nameTemplate = fileName + '_link{0}{1}{2}'

        if fileExtension != None:
            if fileExtension != '':
                nameTemplate += fileExtension

        linkName = self.fileManager.getInitName(location, nameTemplate, '_')

        inputDialog = self.dragonfmManager.createInputDialog(description = ['Linkname:'])
        inputDialog.setDefaultValue(linkName)
        exitStatus, linkName = inputDialog.show()
        if not exitStatus:
            return

        if not location.endswith('/'):
            location += '/'
        fullPath = '{0}{1}'.format(location, linkName)

        self.fileManager.spawnCreateLinkCursorThread(currentCursor, fullPath)
        if callback:
            callback()
