import sys, os, time, threading, curses
from os.path import expanduser
from collections import OrderedDict
from dragonfilemanager.core import favManager
from dragonfilemanager.core.menuManager import menuManager

class detailManager(menuManager):
    def __init__(self, id, dragonfmManager):
        self.dragonfmManager = dragonfmManager
        self.screen = self.dragonfmManager.getScreen()
        self.height = self.dragonfmManager.getScreenHeight()
        self.width = self.dragonfmManager.getScreenWidth()
        self.settingsManager = self.dragonfmManager.getSettingsManager()
        self.fileManager = self.dragonfmManager.getFileManager()
        self.commandManager = self.dragonfmManager.getCommandManager()
        menuManager.__init__(self, '/home/chrys/Projekte/dragonFM/src/dragonfilemanager/commands/detail-menu/')
        self.id = id
        self.details = []
        self.collectorLocation = ''
        self.collectorIdentity = ''
        self.collector = None
        self.collectorParam = {}
        self.index = 0
        self.entries = OrderedDict({'1': 'test', '2': 'test2','sub':{'1':'subtest','2': 'sub2test'}})
        self.keys = ['1','2','sub']
        self.typeAheadSearch = ''
        self.lastTypeAheadTime = time.time()
        self.page = 0
        self.columns = []
        self.setColumns(self.settingsManager.get('details', 'columns'))
        self.setCollector()
    def shutdown(self):
        pass
    def doTypeAheadSearch(self, key):
        # useful for type ahead search?
        if key == None:
            return False
        if not isinstance(key, str):
            return False
        if len(key) != 1:
            return False
        key = key.lower()
        if not key in '.-_0123456789abcdefghijklmnopqrstuvwxyz':
            return False
        if self.keys == None:
            return False
        if len(self.keys) < 2:
            return False
        # then search
        if self.typeAheadSearch != key:
            self.typeAheadSearch += key

        startIndex = self.getIndex()
        searchIndex = startIndex

        searchString = '{0}'.format(self.typeAheadSearch)

        while True:
            if len(self.typeAheadSearch) == 1:
                # jump always to next match if only one first letter nav (==1)
                searchIndex += 1
                if searchIndex >= len(self.keys):
                    searchIndex = 0
                if searchIndex == startIndex:
                    return False
            # search by name column
            entry = self.entries[self.keys[searchIndex]]
            if entry['name'].lower().startswith(searchString):
                self.setIndex(searchIndex)
                self.lastTypeAheadTime = time.time()
                return True
            elif len(self.typeAheadSearch) > 1:
                # keep current match until its not matching 
                # anymore for type ahead search (> 1)
                searchIndex += 1
                if searchIndex >= len(self.keys):
                    searchIndex = 0
                if searchIndex == startIndex:
                    return False
    def resetTypeAheadSearch(self, force = False):
        if (time.time() - self.lastTypeAheadTime > 1.5) or force:
            self.typeAheadSearch = ''
    def setColumns(self, colums):
        if isinstance(colums, str):
            colums = colums.lower().split(',')
        self.columns = colums
        if self.columns == []:
            self.columns = ['full','type','size','uname','gname','mode','mtime','ctime','atime']
    def getColumns(self):
        return self.columns
    def enter(self):
        self.dragonfmManager.update()
    def leave(self):
        pass
    def setCurrentCursor(self, index, entryName = None):
        NoOfEntries = len(self.keys)
        # dont overrunt
        if index >= NoOfEntries:
            # dont underrun
            if NoOfEntries > 0:
                index = len(self.keys) - 1
            else:
                index = 0
        self.setIndex(index)

        # try to get current element 
        if entryName != None:
            try:
                self.setIndex( self.keys.index(entryName))
            except:
                pass

    def getKeyByIndex(self, index):
        try:
            return self.keys[index]
        except Exception as e:
            pass
        return None

    def updatePage(self):
        index = self.getIndex()
        size = self.getEntryAreaSize()
        page = int(index / size)
        if page != self.page:
            self.page = page

    def getIndex(self):
        return self.index
    def setIndex(self, index):
        self.index = index
    def firstEntry(self):
        self.setIndex(0)
    def lastEntry(self):
        if len(self.entries) - 1 >= 0:
            self.setIndex(len(self.entries) - 1)
        else:
            self.setIndex(0)
    '''
    def prevEntry(self):
        if self.getIndex() > 0:
            self.setIndex( self.getIndex() -1)
        else:
            self.firstEntry()
    def nextEntry(self):
        if self.index < len(self.entries) - 1:
            self.setIndex( self.getIndex() +1)
        else:
            self.lastEntry()
    '''
    def getEntryAreaSize(self):
        return self.height - self.dragonfmManager.getHeaderOffset()

    def getCurrentEntry(self):
        try:
            return self.entries[self.getCurrentKey()]
        except:
            return None
    def getCurrentKey(self):
        try:
            return self.getKeyByIndex(self.getIndex())
        except:
            return None

    def getPositionForIndex(self):
        index = self.getIndex()
        size = self.getEntryAreaSize()
        page = self.getPage()
        # page to index
        screenIndex = index - page * size
        # header bar
        screenIndex += self.dragonfmManager.getHeaderOffset()
        return screenIndex
    def update(self):
        self.drawHeader()
        self.updatePage()
        self.drawEntryList()
        screenIndex = self.getPositionForIndex()
        self.dragonfmManager.setCursor(screenIndex, 0)
        self.dragonfmManager.refresh()
    def getID(self):
        return self.id
    def getPage(self):
        return self.page

    def defaultCollector(self, param):
        pass

    def getCollectorLocation(self):
        return self.collectorLocation

    def setCollectorLocation(self, collectorLocation):
        if self.getCollectorLocation() == '':
            self.collectorLocation = collectorLocation

    def resetCollectorLocation(self):
        self.CollectorLocation = ''
    def getCollectorIdentity(self):
        return self.collectorIdentity
    def setCollector(self, collector=None, collectorParam = {}, collectorIdentity = 'detailMenu'):
        if collector == None:
            collector = self.defaultCollector
            self.setColumns(self.settingsManager.get('details', 'columns'))
            self.resetCollectorLocation()
        else:
            self.setCollectorLocation(self.getLocation())
        self.collector = collector
        self.collectorParam = collectorParam
        self.collectorIdentity = collectorIdentity
    def getCollector(self):
        return self.collector
    def getCollectorParam(self):
        return self.collectorParam
    def handleDetailsInput(self, shortcut):
        command = self.settingsManager.getShortcut('detail-keyboard', shortcut)
        debug = self.settingsManager.getBool('debug', 'input')
        self.resetTypeAheadSearch(command != '')
        if command == '':
            if debug:
                self.dragonfmManager.setMessage('debug Sequence: {0}'.format(shortcut))
            if self.doTypeAheadSearch(shortcut):
                return True
            return False
        try:
            if not self.commandManager.isCommandActive('detail', command):
                return False
            result = self.commandManager.runCommand('detail', command)
            self.dragonfmManager.setMessage(str(self.getCurrentValue()))
            if debug:
                self.dragonfmManager.setMessage('debug Sequence: {0} Command: {1} Command Success: {2}'.format(shortcut, command, result))
            return result
        except Exception as e:
            if debug:
                self.dragonfmManager.setMessage('debug Sequence: {0} Command: {1} Error: {2}'.format(shortcut, command, e))
    def handleInput(self, shortcut):
        return self.handleDetailsInput(shortcut)

    def getDetails(self):
        return self.details
    def setDetails(self, details = []):
        self.details = details
    def drawHeader(self):
        # paint header
        self.dragonfmManager.addText(self.dragonfmManager.getHeaderOffset(), 0, _('Tab: {0} Detail').format(self.getID()))
        self.dragonfmManager.incHeaderOffset()
        details = self.getDetails()
        self.dragonfmManager.addText(self.dragonfmManager.getHeaderOffset(), 0, _('Active Elements: {0}').format(len(details)))
        if len(details) == 1:
            try:
                e = self.fileManager.getInfo(details[0])
                for column in self.getColumns():
                    if column in ['object', 'path']:
                        continue
                    formattedValue = self.fileManager.formatColumn(column, e[column])
                    line = '{1}: {0}'.format(formattedValue, column)
                    self.dragonfmManager.addText(self.dragonfmManager.getHeaderOffset(), 0, line)
                    self.dragonfmManager.incHeaderOffset()
            except:
                pass
        elif len(details) <= 5:
            for fullPath in details:
                try:
                    e = self.fileManager.getInfo(fullPath)
                except:
                    continue
                self.dragonfmManager.incHeaderOffset()
                line = 'Path: {0}'.format(e['full'])
                self.dragonfmManager.addText(self.dragonfmManager.getHeaderOffset(), 0, line)

        self.dragonfmManager.incHeaderOffset()
        self.dragonfmManager.addText(self.dragonfmManager.getHeaderOffset(), 0, _('Page: {0}').format(self.getPage() + 1))
        self.dragonfmManager.incHeaderOffset()
        pos = 0
        for c in ['name']:
            self.dragonfmManager.addText(self.dragonfmManager.getHeaderOffset(), pos, c )
            pos += len(c) + 3
        self.dragonfmManager.incHeaderOffset()

    def drawEntryList(self):
        startingIndex = self.getPage() * self.getEntryAreaSize()
        for i in range(self.getEntryAreaSize()):
            if i == self.height:
                break
            if startingIndex + i >= len(self.entries):
                break
            key = self.getKeyByIndex(startingIndex + i)
            e = self.entries[key]
            pos = 0
            for c in ['name']:
                lowerColumn = c.lower()
                
                #self.dragonfmManager.setMessage(str(e))
                #return
                formattedValue = self.fileManager.formatColumn(lowerColumn, e)
                if i + len(formattedValue) < self.width:
                    self.dragonfmManager.addText(i + self.dragonfmManager.getHeaderOffset(), pos, formattedValue )
                    pos += len(formattedValue) + 2
            i += 1
