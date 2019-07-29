from dragonfilemanager.core.configShellCommand import configShellCommand

class command(configShellCommand):
    def __init__(self, dragonfmManager):
        configShellCommand.__init__(self, dragonfmManager, 'compress', 'quick compress 2', 'compress a list of files with quick compress 2', True)

    def run(self, callback = None):
        # Get the files and directories that were selected.
        selected = self.selectionManager.getSelectionOrCursorCurrentTab()
        countSelected = len(selected)
        if countSelected == 0:
            self.dragonfmManager.setMessage('No files selected for compressing')
            return

        availableFormats = self.settingsManager.getSettingsForCategory(self.getCategory())

        quickCompress2 = self.settingsManager.get('application', 'quickCompress2')
        if quickCompress2 != '':
            if not quickCompress2 in availableFormats:
                return
        else:
            return

        # ask for archive filename
        listManager = self.dragonfmManager.getCurrListManager()
        location = listManager.getLocation()
        archiveName = 'archive{0}{1}{2}.'
        archiveName += quickCompress2
        archiveName = self.fileManager.getInitName(location, archiveName, '_')

        inputDialog = self.dragonfmManager.createInputDialog(description = [_('Please enter an Name for the archive:')])
        inputDialog.setInitValue(archiveName)
        exitStatus, filename = inputDialog.show()
        if not exitStatus:
            return

        fileParameter = self.processManager.convertListToString(selected)
        cmd = self.settingsManager.get(self.getCategory(), quickCompress2)

        super().run(cmd.format(fileParameter, filename))
        if callback:
            callback()
