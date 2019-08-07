from dragonfilemanager.core.baseCommand import baseCommand

class command(baseCommand):
    def __init__(self, dragonfmManager):
        baseCommand.__init__(self, dragonfmManager)
        self.dragonfmManager = dragonfmManager
        self.settingsManager = self.dragonfmManager.getSettingsManager()
        self.fileManager = self.dragonfmManager.getFileManager()
        self.setName('Paste')
        self.setDescription('Paste the clipboard to current location')
    def active(self):
        return self.commandManager.isCommandValidForFileOperation(writePerm = True)
    def run(self, callback = None):   
        self.fileManager.spawnPasteClipboardThread()
        if callback:
            callback()
