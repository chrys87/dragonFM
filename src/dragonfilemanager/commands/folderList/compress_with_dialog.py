from dragonfilemanager.core.configShellCommand import configShellCommand

class command(configShellCommand):
    def __init__(self, dragonfmManager):
        configShellCommand.__init__(self, dragonfmManager, 'compress', 'compress', ' compress a list of files', True)
        self.fileManager = self.dragonfmManager.getFileManager()

    def run(self, callback = None):
        # Get the files and directories that were selected.
        selected = self.selectionManager.getSelectionOrCursorCurrentTab()
        countSelected = len(selected)
        if countSelected == 0:
            self.dragonfmManager.setMessage('No files selected for compressing')
            return

        availableFormats = self.settingsManager.getSettingsForCategory(self.getCategory())

        question = []
        question.append(_('What format you want to compress the {} elements:').format(countSelected))
        for e in availableFormats:
            question.append(e)

        defaultCompression = self.settingsManager.get('application', 'defaultCompression')

        inputDialog = self.dragonfmManager.createInputDialog(description = question)
        inputDialog.setDefaultValue(defaultCompression)
        inputDialog.setMultipleChoiceMode(True, availableFormats)
        exitStatus, fileFormat = inputDialog.show()
        
        if not exitStatus:
            return
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
        if callback:
            callback()
