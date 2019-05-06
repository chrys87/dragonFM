from configparser import RawConfigParser
import os, argparse

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
        path = '~/.config/dragonfm/settings.conf'
        if os.access(path, os.R_OK):
            return path
        path = '/etc/dragonfm/settings.conf'
        if os.access(path, os.R_OK):
            return path
        path = self.dragonfmManager.getDragonFmPath() + '/../../conf/settings/settings.conf'
        if os.access(path, os.R_OK):
            return path
        return ''
    def loadSettings(self):
        settingsFile = self.getSettingsPath()
        if settingsFile != '':
            self.load(settingsFile)
    def load(self, path):
        if not os.access(path, os.R_OK):
            return False
        try:
            self.configParser = RawConfigParser()
            self.configParser.read(path)
            self.loadedSettingFile = path
            return True
        except Exception as e:
            pass
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
        try:
            t = self.settings[section][setting]
        except:
            print(section, setting, 'not found')
            return
        try:
            if isinstance(self.settings[section][setting], str):
                v = str(value)
            elif isinstance(self.settings[section][setting], bool):
                if not value in ['True','False']:
                    raise ValueError('could not convert string to bool: '+ value)
            elif isinstance(self.settings[section][setting], int):
                v = int(value)
            elif isinstance(self.settings[section][setting], float):
                v = float(value)
            self.settingArgDict[section][setting] = str(value)
        except Exception as e:
            print('settingsManager:set:Datatype missmatch: '+ section + '#' + setting + '=' +  value + ' Error:' +  str(e))
            return
    def get(self, section, setting):
        value = ''
        try:
            value = self.configParser.get(section, setting)
        except Exception as e:
            try:
                value = str(self.settings[section][setting])
            except Exception as e:
                return ''
        return value
    def getShortcut(self, section, setting):
        value = ''
        try:
            value = self.configParser.get(section, setting)
        except:
            try:
                value = str(self.settings[section][setting])    
            except:
                pass
        return value

    def getInt(self, section, setting):
        value = 0
        try:
            value = self.configParser.getint(section, setting)
        except:
            value = self.settings[section][setting]
        return value

    def getFloat(self, section, setting):
        value = 0.0
        try:
            value = self.configParser.getfloat(section, setting)
        except:
            value = self.settings[section][setting]
        return value

    def getBool(self, section, setting):
        value = False
        try:
            value = self.configParser.getboolean(section, setting)
        except:
            value = self.settings[section][setting]
        return value
    def getDefaultSettings(self):
        return {
        }.copy()
                           
