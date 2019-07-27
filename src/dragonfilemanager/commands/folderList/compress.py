from dragonfilemanager.core.configShellCommand import configShellCommand

class command(configShellCommand):
    def __init__(self, dragonfmManager):
        configShellCommand.__init__(self, dragonfmManager, 'compress', 'compress', ' compress a list of files', True)
    def run(self, callback = None):
        # Get the files and directories that were selected.
        selected = self.selectionManager.getSelectionOrCursorCurrentTab()
        countSelected = len(selected)
        if countSelected == 0:
            self.dragonfmManager.setMessage('No files selected for compressing')
            return

        inputDialog = self.dragonfmManager.createInputDialog(description = [_('What format you want to compress the {} elements:').format(len(selected))])
        inputDialog.setDefaultValue(self.settingsManager.get('compress', 'default'))
        inputBox.setMultipleChoiceMode(True,['zip', 'tar', 'rar'])
        exitStatus, answer = inputDialog.show()
        
        if not exitStatus:
            return

        fileParameter = self.processManager.convertListToString(selected)

        super().run('zip {1} {0}'.format(fileParameter, '/tmp/playzone/target.zip'))
        if callback:
            callback()

'''
inputBox = inputBoxManager(stdscr, description=['Do You realy want?','q = quit','y = yes','n = nope'])
inputBox.setDefaultValue('test')
inputBox.setMultipleChoiceMode(True,['q', 'y', 'n'])
inputBox.setLocationMode(True, '/tmp/playzone',True,True)
inputBox.setConfirmationMode(True)
inputBox.setEditable(False)
inputBox.setInitValue('/tmp/playzone')
'''
