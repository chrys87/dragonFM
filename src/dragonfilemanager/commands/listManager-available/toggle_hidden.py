from dragonfilemanager.core.baseCommand import baseCommand

class command(baseCommand):
    def __init__(self, dragonfmManager):
        baseCommand.__init__(self, dragonfmManager)
        self.dragonfmManager = dragonfmManager
        self.screen = self.dragonfmManager.getScreen()
        self.settingsManager = self.dragonfmManager.getSettingsManager()
        self.setName('toggle hiden')
        self.setDescription('toggle show / hide hidden files and folders')
    def run(self, callback = None):
        listManager = self.dragonfmManager.getCurrListManager()
        showHidden = self.settingsManager.getBool('folder', 'showHidden')
        if showHidden:
            self.settingsManager.set('folder', 'showHidden', 'False')
        else:
            self.settingsManager.set('folder', 'showHidden', 'True')
        listManager.reloadFolder()
        showHidden = not showHidden
        if showHidden:
            self.dragonfmManager.setMessage('{} hidden elements'.format('show'))
        else:
            self.dragonfmManager.setMessage('{} hidden elements'.format('hide'))
        if callback:
            callback()
