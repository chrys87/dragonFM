import os, glob

from dragonfilemanager.utils import module_utils

class commandManager():
    def __init__(self, dragonfmManager):
        self.dragonfmManager = dragonfmManager
        self.screen = self.dragonfmManager.getScreen()
        self.settingsManager = self.dragonfmManager.getSettingsManager()
        self.selectionManager = self.dragonfmManager.getSelectionManager()
        self.fileManager = self.dragonfmManager.getFileManager()
    def loadAllCommands(self):
        self.commands = {}
        # defaults
        self.loadCommands('application')
        self.loadCommands('menu')
        self.loadCommands('view')
        self.loadCommands('tab')
        self.loadCommands('detail')
        self.loadCommands('folderList')
        # custom
        try:
            # ignore if not possible
            customPath = self.settingsManager.get('application', 'pluginFolder')
            if customPath.strip() != '':
                self.loadCommands('application', customPath)
                self.loadCommands('menu', customPath)
                self.loadCommands('view', customPath)
                self.loadCommands('tab', customPath)
                self.loadCommands('detail', customPath)
                self.loadCommands('folderList', customPath)
        except:
            pass
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
    def getCommandName(self, fullPath, command):
        try:
            return command.getName()
        except:
            return ''
    def getCommandActive(self, fullPath, command):
        try:
            return command.active()
        except:
            return False
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
        try:
            e = self.commands[section.upper()]
        except:
            self.commands[section.upper()] = {}
        commandList = glob.glob(commandFolder+'*')
        for command in commandList:
            if command == '':
                continue
            fileName, fileExtension = os.path.splitext(command)
            fileName = fileName.split('/')[-1]
            try:
                loadedCommand = self.loadFile(command)
                if loadedCommand != None:
                    self.commands[section.upper()][fileName.upper()] = loadedCommand
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
    def isCommandValidForFileOperation(self, minSelection = 0, maxSelection = None, mimeTypes = None, writePerm = False, force = False):
        if force:
            return True
        selected = self.selectionManager.getSelectionOrCursorCurrentTab()
        countSelection = len(selected)
        if countSelection < minSelection:
            return False
        if writePerm:
            listManager = self.dragonfmManager.getCurrListManager()
            location = listManager.getLocation()
            if not os.access(location, os.W_OK):
                return False
        if maxSelection != None:
            if countSelection > maxSelection:
                return False
        if mimeTypes != None:
            mimeCheckCounter = 0
            maxMimeCheckCounter = 3
            for currCursor in selected:
                mimeCheckCounter += 1
                fileInfo = self.fileManager.getInfo(currCursor)
                fileMimeType = fileInfo['mime']
                if not fileMimeType in mimeTypes:
                    return False
                if mimeCheckCounter >= maxMimeCheckCounter:
                    return False
        return True
    def runCommand(self, section, command, callback = None):
        if not self.commandExist(section, command):
            return False
        c = self.getCommand(section, command)
        try:
            if not c.active():
                return True
            c.run(callback)
            return True
        except Exception as e:
            print(e)
        return False
