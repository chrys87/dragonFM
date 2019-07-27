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

        fileParameter = self.processManager.convertListToString(selected)
        super().run('gzip -c {1} > {0}'.format('target.zip', fileParameter))
        if callback:
            callback()
