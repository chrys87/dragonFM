from configparser import ConfigParser
import os
from dragonfilemanager.core import defaultSettings

class settingsManager():
    def __init__(self):
        self.settings = None
        self.reset()
    def getDefaultSettingsPath():
        return '/tmp'
    def load(self, path):
        pass
    def save(self, path):
        pass

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
