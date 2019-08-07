from dragonfilemanager.core.baseConfigShellCommand import baseConfigShellCommand

class command(baseConfigShellCommand):
    def __init__(self, dragonfmManager):
        baseConfigShellCommand.__init__(self, dragonfmManager, 'compress', 'compress', 'compress a list of files', True)
    def active(self):
        return self.commandManager.isCommandValidForFileOperation(minSelection = 1, writePerm = True)
    def run(self, callback = None):
        # Get the files and directories that were selected.
        selected = self.selectionManager.getSelectionOrCursorCurrentTab()
        countSelected = len(selected)
        if countSelected == 0:
            self.dragonfmManager.setMessage('No files selected for compressing')
            return

        # ask for compression type, show list of available compressions
        availableFormats = self.settingsManager.getSettingsForCategory(self.getCategory())
        question = []
        question.append(_('What format you want to compress the {} elements:').format(countSelected))
        for e in availableFormats:
            question.append(e)

        inputDialog = self.dragonfmManager.createInputDialog(description = question)
        
        try:
            defaultCompression = self.settingsManager.get('application', 'defaultCompression')
            if defaultCompression != '':
                if defaultCompression in availableFormats:
                    inputDialog.setDefaultValue(defaultCompression)
        except:
            pass

        inputDialog.setMultipleChoiceMode(True, availableFormats)
        exitStatus, fileFormat = inputDialog.show()
        if not exitStatus:
            return

        # ask for archive filename
        listManager = self.dragonfmManager.getCurrListManager()
        location = listManager.getLocation()
        archiveName = 'archive{0}{1}{2}.'
        archiveName += defaultCompression
        archiveName = self.fileManager.getInitName(location, archiveName, '_')

        inputDialog = self.dragonfmManager.createInputDialog(description = [_('Please enter an Name for the archive:')])
        inputDialog.setInitValue(archiveName)
        exitStatus, filename = inputDialog.show()
        if not exitStatus:
            return

        fileParameter = self.processManager.convertListToString(selected)
        cmd = self.settingsManager.get(self.getCategory(), fileFormat)

        super().run(cmd.format(fileParameter, filename))

        if listManager.getSelectionMode() != 0:
            listManager.setSelectionMode(0)

        if callback:
            callback()
