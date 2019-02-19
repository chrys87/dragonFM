from configparser import ConfigParser
import os
from dragonfilemanager.core import defaultSettings

class settingsManager():
    def __init__(self, dragonfmManager):
        self.dragonfmManager = dragonfmManager
        self.settings = None
        self.args = None
        self.parser = None
        self.loadedSettingFile = ''
        self.reset()
    def getSettingsPath(self):
        path = '~/.config/dragonFM/settings.conf'
        if os.access(path, R_OK):
            return path
        path = '/etc/dragonFM/settings.conf'
        if os.access(path, R_OK):
            return path
        path = '/../../config/settings.conf'
        if os.access(path, R_OK):
            return path
        return ''
    def load(self, path):
        if not os.access(path,os.R_OK):
            return False
        try
            self.configParser = ConfigParser()
            self.configParser.read(path)
            self.loadedSettingFile = path
            return True
        except:
            pass
        return False
    def save(self, path):
        if not os.access(path, os.W_OK):
            return False
        try:
            configFile = open(path, 'w')
            self.parser.write(configFile)
            configFile.close()
            return True
        except:
            pass
        return False
        
    def parseCliArgs(self):
        args = None
        self.parser = argparse.ArgumentParser(description="dragonFM Help")
        parser.add_argument('-s', '--setting', metavar='SETTING-FILE', default='~/.config/dragonFM/settings.conf', help='Use a specified settingsfile')
        try:
            args = parser.parse_args()
        except Exception as e:
            parser.print_help()
            return False
        self.args = args
        return True

    def reset(self):
        self.settings = defaultSettings.settings

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
            value = self.settings.get(section, setting)
        except:
            value = str(self.settings[section][setting])
        return value

    def getInt(self, section, setting):
        value = 0
        try:
            value = self.settings.getint(section, setting)
        except:
            value = self.settings[section][setting]
        return value

    def getFloat(self, section, setting):
        value = 0.0
        try:
            value = self.settings.getfloat(section, setting)
        except:
            value = self.settings[section][setting]
        return value

    def getBool(self, section, setting):
        value = False
        try:
            value = self.settings.getboolean(section, setting)
        except:
            value = self.settings[section][setting]
        return value
