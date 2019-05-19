import os, sys 
from os.path import expanduser

class favManager(object):
    def __init__(self, dragonfmManager):
        self.dragonfmManager = dragonfmManager
        self.settingsManager = self.dragonfmManager.getSettingsManager()
        self.fileManager = self.dragonfmManager.getFileManager()
    def isFavoritFolder(self, location):
        return location == expanduser(self.settingsManager.get('favorits', 'path'))

    def addToFav(self, location):

        if not os.path.exists(location):
            return

        favoritName = os.path.basename(location)

        inputDialog = self.dragonfmManager.createInputDialog(description = ['Favoritname:'], initValue = favoritName)
        exitStatus, favoritName = inputDialog.show()
        if not exitStatus:
            return
        favDir = expanduser(self.settingsManager.get('favorits', 'path'))
        if not os.path.exists(favDir):
            os.makedirs(favDir)

        if not favDir.endswith('/'):
            favDir += '/'
        if not location.endswith('/'):
            location += '/'

        destPath = '{0}{1}'.format(favDir, favoritName)

        self.fileManager.spawnCreateLinkCursorThread(location, destPath)
