import time

class AutoComplete:
    def __init__(self):
        self.choices = []
        self.base = ''
        self.lastInputTime = 0
        self.lastCompletionTime = 0
        self.resetAutoCompleteList()
        self.index = None
    def setBase(self, base):
        self.base = base
        self.lastInputTime = time.time()
        self.index = None
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
    def complete(self):
        self.lastCompletionTime = time.time()
        # base = '/ho'
        # Value = '/home'
        # completedValue = 'me'
        return True, 'Value', 'completedValue'


'''
c = AutoComplete()
c.addChoice('/home')
c.setBase('/ho')
ok, value, compValue = c.complete()
'''
