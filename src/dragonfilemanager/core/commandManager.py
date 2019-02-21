import os

from dragonfilemanager.utils import module_utils

class commandManager():
    def __init__(self, dragonfmManager):
        self.dragonfmManager = dragonfmManager
        self.screen = self.dragonfmManager.getScreen()
        self.settingsManager = self.dragonfmManager.getSettingsManager()

    def loadFile(self, filepath = ''):
        if filepath == '':
            return None
        if not os.path.exists(filepath):
            return None
        if os.path.isdir(filepath):
            return None
        if not os.access(filepath, os.R_OK):
            return None
        try:
            fileName, fileExtension = os.path.splitext(filepath)
            fileName = fileName.split('/')[-1]
            if fileName.startswith('__'):
                return None
            if fileExtension.lower() == '.py':
                command_mod = module_utils.importModule(fileName, filepath)
                command = command_mod.command(self.dragonfmManager)
                return command
        except Exception as e:
            pass
        return None
