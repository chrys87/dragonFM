#!/bin/python
import sys,os

class viewManager():
    def __init__(self):
        self.tabs = {}
        self.tabList = []
        self.currentID = -1
        self.mode = 0 # 0: folder, 1: context menu
        self.addTab()
        
    def getNewID(self):
        for i in range(1000):
            if not i in self.tabList:
                return i
        return None
    def addTab(self, changeToNew = True, newID = None):
        if self.mode != 0:
            return False
        id = None
        if newID == None:
            id = self.getNewID()
        else:
            id = newID
        if id == None:
            return False
        self.tabs[id] = 'tab ' + str(id)
        if self.tabList == []:
            self.tabList = [id]
        else:
            self.tabList = self.tabList[:self.getCurrentIndex() + 1] + [id] + self.tabList[self.getCurrentIndex() + 1:]
        if changeToNew:
            self.changeTab(id)
        return True
    def closeCurrentTab(self):
        self.closeTab(self.currentID)
    def closeTab(self, id):
        if self.mode != 0:
            return
        #if len(self.tabList) > 1:
        tabIndex = -1
        try:
            oldIndex = self.getIndexForID(id)
            newIndex = oldIndex
            if newIndex >= len(self.tabList) - 1:
                newIndex = len(self.tabList) - 2
            #newID = self.tabList[0]
            self.tabList.remove(id)
            newID = self.tabList[newIndex]
            self.changeTab(newID)
            del self.tabs[id]
        except Exception as e:
            print(e)
            pass
        #else:
        #    self.dragonfmManager.stop()
    def getCurrentIndex(self):
        return self.getIndexForID(self.currentID)
    def getIndexForID(self, id):
        try:
            return self.tabList.index(id)
        except:
            return None
    def getIDForIndex(self, index):
        try:
            return self.tabList[index]
        except:
            return None
    def changeMode(self, mode):
        if self.mode == mode:
            return
        if self.mode == 0:
            print('leave index', self.getCurrentIndex())
        elif self.mode == 1:
            print('self.mainMenuManager.leave()')

        if mode == 0:
            print('enter index', self.getCurrentIndex())
        elif mode == 1:
            print('self.mainMenuManager.enter()')
        self.mode = mode
    def prevTab(self):
        currIndex = self.getCurrentIndex()
        currIndex -= 1
        if currIndex < 0:
            currIndex = len(self.tabList) - 1
        self.changeTab(self.tabList[currIndex])
    def nextTab(self):
        currIndex = self.getCurrentIndex()
        currIndex += 1
        if currIndex >= len(self.tabList):
            currIndex = 0
        self.changeTab(self.tabList[currIndex])
    def changeTabIndex(self, index):
        id = self.getIDForIndex(index)
        if id == None:
            return
        self.changeTab(id)
    def changeTab(self, id):
        if self.mode != 0:
            return
        if not id in self.tabList:
            return
        # old
        if self.currentID != -1:
            if self.currentID == id:
                return
            print('leave currentID' + str(self.currentID))
        # new
        self.currentID = id
        print('changed to' + str(self.currentID ))
        print('enter currentID' + str(self.currentID))
    def getCurrentTab(self):
        return self.getTab(self.currentID)
    def getTab(self, id):
        try:
            return self.tabs[id]
        except:
            return None
    def update(self):
        if self.mode == 0:
            self.getCurrentTab().update()
        elif self.mode == 1:
            print('self.mainMenuManager.update()')
        #self.screen.addstr(8, 0, 'index:{}, tablist: {}'.format(self.getCurrentIndex(),self.tabList))
        #self.screen.addstr(9, 0, str(self.tabs.keys()))

vm = viewManager()
vm.addTab()
vm.addTab()
vm.addTab()
vm.addTab()
vm.addTab()
vm.nextTab()
vm.closeCurrentTab()
print(vm.tabList, vm.getCurrentIndex(), vm.currentID)
