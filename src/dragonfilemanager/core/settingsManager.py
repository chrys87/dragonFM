from configparser import RawConfigParser
import os, argparse
from os.path import expanduser


class settingsManager():
    def __init__(self, dragonfmManager):
        self.dragonfmManager = dragonfmManager
        self.settings = None
        self.reset()
        self.configParser = None
        self.args = None
        self.argParser = None
        self.settingFile = ''
    def getSettingsPath(self):
        path = self.args.setting
        if os.access(path, os.R_OK):
            return path
        path = expanduser('~/.config/dragonfm/settings/settings.conf')
        if os.access(path, os.R_OK):
            return path
        path = '/etc/dragonfm/settings/settings.conf'
        if os.access(path, os.R_OK):
            return path
        path = self.dragonfmManager.getDragonFmPath() + '/../../config/settings/settings.conf'
        if os.access(path, os.R_OK):
            return path
        return ''
    def loadSettings(self):
        settingsFile = self.getSettingsPath()
        if settingsFile != '':
            return self.load(settingsFile)
        return False
    def load(self, path):
        if not os.access(path, os.R_OK):
            return False
        try:
            self.configParser = RawConfigParser()
            self.configParser.read(path)
            self.loadedSettingFile = path
            return True
        except Exception as e:
            print(e)
        return False
    def save(self, path):
        if not os.access(path, os.W_OK):
            return False
        try:
            configFile = open(path, 'w')
            self.configParser.write(configFile)
            configFile.close()
            return True
        except:
            pass
        return False
    def getCategorys(self):
        return self.configParser.sections()
    def getSettingsForCategory(self, category):
        return self.configParser.options(category)
    def parseCliArgs(self):
        args = None
        self.argParser = argparse.ArgumentParser(description="dragonFM Help")
        self.argParser.add_argument('-s', '--setting', metavar='SETTING-FILE', default='~/.config/dragonFM/settings.conf', help='Use a specified settingsfile')
        try:
            args = self.argParser.parse_args()
        except Exception as e:
            self.argParser.print_help()
            return False
        self.args = args
        return True

    def reset(self):
        self.settings = self.getDefaultSettings()

    def set(self, section, setting, value):
        testValue = None
        try:
            testValue = self.configParser.get(section, setting)
        except Exception as e:
            print(section, setting, 'not found')
            return
        try:
            if isinstance(testValue, str):
                v = str(value)
            elif isinstance(testValue, bool):
                if not value in ['True','False']:
                    raise ValueError('could not convert string to bool: '+ value)
            elif isinstance(testValue, int):
                v = int(value)
            elif isinstance(testValue, float):
                v = float(value)
            try:
                testSection = self.settings[section]
            except KeyError:
                self.settings[section] = {}
            self.settings[section][setting] = str(value)
        except Exception as e:
            print('settingsManager:set:Datatype missmatch: '+ section + '#' + setting + '=' +  value + ' Error:' +  str(e))
            return
    def get(self, section, setting):
        value = ''
        try:
            value = str(self.settings[section][setting])
        except KeyError:
            value = self.configParser.get(section, setting)
        return value
    def getShortcut(self, section, setting):
        value = ''
        try:
            value = str(self.settings[section][setting])
        except KeyError:
            try:
                value = self.configParser.get(section, setting)
            except:
                pass
        return value

    def getInt(self, section, setting):
        value = 0
        try:
            value = int(self.settings[section][setting])
        except:
            value = self.configParser.getint(section, setting)
        return value

    def getFloat(self, section, setting):
        value = 0.0
        try:
            value = float(self.settings[section][setting])
        except:
            value = self.configParser.getfloat(section, setting)
        return value

    def getBool(self, section, setting):
        value = False
        try:
            value = self.settings[section][setting] == 'True'
        except KeyError:
            value = self.configParser.getboolean(section, setting)
        return value
    def getDefaultSettings(self):
        return {
        }.copy()
