import os, glob

from dragonfilemanager.utils import module_utils

class commandManager():
    def __init__(self, dragonfmManager):
        self.dragonfmManager = dragonfmManager
        self.screen = self.dragonfmManager.getScreen()
        self.settingsManager = self.dragonfmManager.getSettingsManager()
        self.commands = {}
        self.loadCommands('application')
        self.loadCommands('menu')
        self.loadCommands('view')
        self.loadCommands('tab')
        self.loadCommands('detail')
        self.loadCommands('folderList')
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
            print(e)
            pass
        return None

    def loadCommands(self, section ,commandPath=''):
        if commandPath =='':
            commandPath = self.dragonfmManager.getDragonFmPath() + '/commands/'
        if not commandPath.endswith('/'):
            commandPath += '/'
        commandFolder = commandPath + section +"/"
        if not os.path.exists(commandFolder):
            return   
        if not os.path.isdir(commandFolder):
            return
        if not os.access(commandFolder, os.R_OK):
            return
        self.commands[section.upper()] = {}
        commandList = glob.glob(commandFolder+'*')
        for command in commandList:
            try:
                if command == '':
                    continue
                if not os.path.exists(command):
                    continue
                if os.path.isdir(command):
                    continue
                if not os.access(command, os.R_OK):
                    continue
                fileName, fileExtension = os.path.splitext(command)
                fileName = fileName.split('/')[-1]
                if fileName.startswith('__'):
                    continue
                if fileExtension.lower() != '.py':
                    continue
                command_mod = module_utils.importModule(fileName, command)
                self.commands[section.upper()][fileName.upper()] = command_mod.command(self.dragonfmManager)
            except Exception as e:
                print('command {0}: {1}'.format(fileName, e))
                continue

    def commandExist(self, section, command):
        try:
            c = self.getCommand(section, command)
            if not c:
                return False
        except KeyError:
            return False
        return True
    def getCommand(self, section, command):
        try:
            c = self.commands[section.upper()][command.upper()]
            return c
        except Exception as e:
            print(e)
            return None
        return None
    def isCommandActive(self, section, command):
        if not self.commandExist(section, command):
            return False
        c = self.getCommand(section, command)
        try:
            return c.active()
        except Exception as e:
            print(e)
        return False
    def runCommand(self, section, command, callback = None):
        #self.dragonfmManager.leave()

        if not self.commandExist(section, command):
            return False
        c = self.getCommand(section, command)
        try:
            c.run(callback)
            return True
        except Exception as e:
            print(e)
        return False
