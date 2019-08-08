from dragonfilemanager.core.baseCommand import baseCommand
import os

class command(baseCommand):
    def __init__(self, dragonfmManager):
        baseCommand.__init__(dragonfmManager)
        self.dragonfmManager = dragonfmManager
        self.settingsManager = self.dragonfmManager.getSettingsManager()
        self.selectionManager = self.dragonfmManager.getSelectionManager()
        self.fileManager = self.dragonfmManager.getFileManager()
        self.setName('Rename')
        self.setDescription('Rename a file or folder')
    def active(self):
        return self.commandManager.isCommandValidForFileOperation(minSelection = 1, writePerm = True)
    def run(self, callback = None):   
        listManager = self.dragonfmManager.getCurrListManager()
        location = listManager.getLocation()
        currentCursor = self.selectionManager.getCursorCurrentTab()
        if currentCursor == None:
            return
        if not os.path.exists(currentCursor):
            return
        currEntryName = os.path.basename(currentCursor)
        inputDialog = self.dragonfmManager.createInputDialog(description = ['Please enter a new name:'], initValue = currEntryName)
        exitStatus, newEntryName = inputDialog.show()
        if not exitStatus:
            return
        if currEntryName == newEntryName:
            return
        if not location.endswith('/'):
            location += '/'
        fullPath = '{0}{1}'.format(location, newEntryName)
        self.fileManager.moveEntry(currentCursor, fullPath)
        if callback:
            callback()
