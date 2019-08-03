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
        self.page = 0
        self.columns = []
        self.setColumns(self.settingsManager.get('details', 'columns'))
    def shutdown(self):
        pass

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

    def updatePage(self):
        index = self.getIndexCurrLevel()
        size = self.getEntryAreaSize()
        page = int(index / size)
        if page != self.page:
            self.page = page

    def getEntryAreaSize(self):
        return self.height - self.dragonfmManager.getHeaderOffset()

    def getPositionForIndex(self):
        index = self.getIndexCurrLevel()
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

    def handleDetailsInput(self, shortcut):
        command = self.settingsManager.getShortcut('detail-keyboard', shortcut)
        debug = self.settingsManager.getBool('debug', 'input')
        if command == '':
            if debug:
                self.dragonfmManager.setMessage('debug Sequence: {0}'.format(shortcut))
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
        maxIndex = self.getCurrentMenuSize()
        for i in range(self.getEntryAreaSize()):
            if i == self.height:
                break
            if startingIndex + i >= maxIndex:
                break
            key = startingIndex + i
            e = self.getEntryForIndexCurrLevel(key)
            pos = 0
            for c in ['name']:
                lowerColumn = c.lower()
                formattedValue = self.fileManager.formatColumn(lowerColumn, e)
                if i + len(formattedValue) < self.width:
                    self.dragonfmManager.addText(i + self.dragonfmManager.getHeaderOffset(), pos, formattedValue )
                    pos += len(formattedValue) + 2
            i += 1
