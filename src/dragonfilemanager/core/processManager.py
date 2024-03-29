import os, threading, shlex
from subprocess import Popen, PIPE, STDOUT, DEVNULL

class processManager():
    def __init__(self, dragonfmManager):
        self.dragonfmManager = dragonfmManager
        self.screen = self.dragonfmManager.getScreen()
        self.settingsManager = self.dragonfmManager.getSettingsManager()
        self.externalStarted = False
        self.processListLock = threading.RLock()
        self.internalProcesses = {}
        # process: id, name, description, process, postProcess, preProcess, processParam
    def startInternal(self, name, description = '', process = None , processParam = None, preProcess = None, postProcess = None, pwd = '', preProcessParam = None, postProcessParam = None):
        if process == None:
            return
        id = self.getNewProcessID()
        if id == -1:
            return
        self.processListLock.acquire(True)
        self.internalProcesses[id] = threading.Thread(
            target=self.internalProcess, args=[id, name, description, process, processParam, preProcess, postProcess, pwd, preProcessParam, postProcessParam]
        )
        self.processListLock.release()
        self.internalProcesses[id].start()
    def internalProcess(self, id, name, description, process, processParam, preProcess, postProcess, pwd = '', preProcessParam = None, postProcessParam = None):
        if pwd != '' and os.access(pwd, os.R_OK):
            os.chdir(pwd)

        if preProcess != None:
            if preProcessParam != None:
                preProcess(preProcessParam)
            else:
                preProcess()
        if process != None:
            if processParam != None:
                process(processParam)
            else:
                process()
        if postProcess != None:
            if postProcessParam != None:
                postProcess(postProcessParam)
            else:
                postProcess()
        self.removeInternal(id)
    def startInternalShell(self, cmd, name = '', description = '', preProcess = None, postProcess = None, pwd = '', preProcessParam = None, postProcessParam = None):
        if name == '':
            name = cmd
        self.startInternal(name, description, self.InternalShellProcess, cmd, preProcess, postProcess, pwd, preProcessParam, postProcessParam)
    def InternalShellProcess(self, cmd):
        try:
            proc = Popen(shlex.split(cmd) , stdin=None, stdout=DEVNULL, stderr=DEVNULL, shell=False)
            proc.wait()
        except Exception as e:
            self.dragonfmManager.setMessage(e)
    def convertListToString(self, sourceList, separator = ' '):
        return separator.join('"{0}"'.format(e) for e in sourceList)
    def getNewProcessID(self):
        ids = list(self.internalProcesses.keys())
        for id in range(1000000):
            if not id in ids:
                return id
        return -1
    def removeInternal(self, id):
        try:
            self.processListLock.acquire(True)
            del self.internalProcesses[id]
            self.processListLock.release()
        except:
            pass
    def updateInternal(self, id, property, value):
        pass
    def isExternalStarted(self):
        return self.externalStarted
    def setExternalStarted(self, isExternalStarted):
        self.externalStarted = isExternalStarted
    def startExternal(self, application = '', pwd = ''):
        if application == '':
            return
        if pwd != '' and os.access(pwd, os.R_OK):
            os.chdir(pwd)
        self.dragonfmManager.leave()
        self.setExternalStarted(True)
        try:
            os.system(application)
        except:
            pass
        self.setExternalStarted(False)
        self.dragonfmManager.enter()
