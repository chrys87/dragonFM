import time
import os
from os.path import expanduser

class AutoComplete:
    def __init__(self):
        self.choices = []
        self.base = ''
        self.actualLineValue = ''
        self.lastInputTime = 0
        self.lastCompletionTime = 0
        self.resetChoices()
        self.index = 0
    def setBase(self, base):
        self.base = base
        self.actualLineValue = ''
        self.lastInputTime = time.time()
        self.index = 0
    def getBase(self):
        return self.base
    def resetChoices(self):
        self.choices = []
    def getChoices(self):
        return self.choices
    def addChoice(self, l):
        if isinstance(l, list):
            self.choices.extend(l)
        if isinstance(l, tuple):
            self.choices.extend(l)
        else:
            self.choices.append(l)
    def addFolderChoices(self, location):
        subfolders = []
        if not '/' in self.base:
            subfolders = [f.name for f in os.scandir(location) if f.is_dir() and self.base in f.name[0:len(self.base)]]
        else:
            slashIndex = self.base.rfind('/')
            subfolders = [f.name for f in os.scandir(location + self.base[0:slashIndex]) if f.is_dir() and self.base[slashIndex + 1:] in f.name[0:len(self.base[slashIndex + 1:])]]
        self.addChoice(subfolders)
    def complete(self):
        self.lastCompletionTime = time.time()
        # base = '/ho'
        # Value = '/home'
        # completedValue = 'me'
        
        if self.index >= len(self.choices):
            self.index = 0
        if self.choices != []:
            actualLineValue = self.base[0:self.base.rfind('/') + 1] + self.choices[self.index]
            self.index += 1
            return True, actualLineValue, actualLineValue[len(self.base):]
        
        return False, self.base, ''



c = AutoComplete()
c.addFolderChoices('./tmp/playzone')
c.setBase('/')
ok, value, compValue = c.complete()
print(value)
ok, value, compValue = c.complete()
print(value)
ok, value, compValue = c.complete()
print(value)
print('-----------------------------')
c.setBase(value + '/')
ok, value, compValue = c.complete()
print(value)
ok, value, compValue = c.complete()
print(value)
ok, value, compValue = c.complete()
print(value)
c.resetChoices()
c.setBase('')
c.addChoice('help')
c.addChoice('?help')
c.addChoice('?version')
c.addChoice('?author')
print('-----------------------------')
ok, value, compValue = c.complete()
print(value)
ok, value, compValue = c.complete()
print(value)
ok, value, compValue = c.complete()
print(value)
ok, value, compValue = c.complete()
print(value)
