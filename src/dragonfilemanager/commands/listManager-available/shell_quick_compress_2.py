from dragonfilemanager.core.baseConfigShellCommand import baseConfigShellCommand

class command(baseConfigShellCommand):
    def __init__(self, dragonfmManager):
        baseConfigShellCommand.__init__(self, dragonfmManager, 'compress', 'quick compress 1', 'compress a list of files with quick compress 1', True)

    def run(self, callback = None):
        # Get the files and directories that were selected.
        selected = self.selectionManager.getSelectionOrCursorCurrentTab()
        countSelected = len(selected)
        if countSelected == 0:
            self.dragonfmManager.setMessage('No files selected for compressing')
            return

        availableFormats = self.settingsManager.getSettingsForCategory(self.getCategory())

        quickCompress1 = self.settingsManager.get('application', 'quickCompress1')
        if quickCompress1 != '':
            if not quickCompress1 in availableFormats:
                return
        else:
            return

        # ask for archive filename
        listManager = self.dragonfmManager.getCurrListManager()
        location = listManager.getLocation()
        archiveName = 'archive{0}{1}{2}.'
        archiveName += quickCompress1
        archiveName = self.fileManager.getInitName(location, archiveName, '_')

        inputDialog = self.dragonfmManager.createInputDialog(description = [_('Please enter an Name for the archive:')])
        inputDialog.setInitValue(archiveName)
        exitStatus, filename = inputDialog.show()
        if not exitStatus:
            return

        fileParameter = self.processManager.convertListToString(selected)
        cmd = self.settingsManager.get(self.getCategory(), quickCompress1)

        super().run(cmd.format(fileParameter, filename))

        if listManager.getSelectionMode() != 0:
            listManager.setSelectionMode(0)

        if callback:
            callback()
