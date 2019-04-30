import sys, os, threading, curses, time, inspect, signal

from dragonfilemanager.core import i18n
from dragonfilemanager.core import settingsManager
from dragonfilemanager.core import debugManager
from dragonfilemanager.core import viewManager
from dragonfilemanager.core import inputManager
from dragonfilemanager.core import fileManager
from dragonfilemanager.core import commandManager
from dragonfilemanager.core import clipboardManager
from dragonfilemanager.core import processManager
from dragonfilemanager.core import selectionManager

class dragonfmManager():
    def __init__(self):
        self.running = True
        self.disabled = True
        self.screen = None
        self.height = 0
        self.width = 0
        self.currentdir = os.path.dirname(os.path.realpath(os.path.abspath(inspect.getfile(inspect.currentframe()))))
        self.dragonFmPath = os.path.dirname(self.currentdir)
        self.settingsManager = settingsManager.settingsManager(self)
        self.settingsManager.parseCliArgs()
        self.settingsManager.loadSettings()
        self.processManager = processManager.processManager(self)
        self.clipboardManager = clipboardManager.clipboardManager(self)
        self.debugManager = debugManager.debugManager(self)
        self.fileManager = fileManager.fileManager(self)
        self.selectionManager = selectionManager.selectionManager(self)       
        self.viewManager = None
        self.inputManager = None
        self.commandManager = commandManager.commandManager(self)

        self.setProcessName()

    def start(self):
        self.enter()
        try:
            self.proceed()
        except Exception as e:
            print(e)
        self.leave()
    # main process
    def proceed(self):
        self.inputManager = inputManager.inputManager(self)
        self.viewManager = viewManager.viewManager(self)
        self.update()
        while self.running:
            shortcut = str(self.inputManager.get())
            if shortcut:
                self.handleInput(shortcut)
            self.update()
        self.shutdown()
    def update(self):
        if not self.running:
            return
        self.viewManager.update()
    def handleApplicationInput(self, shortcut):
        command = self.settingsManager.getShortcut('application-keyboard', shortcut)
        if command == '':
            return False
        return self.commandManager.runCommand('application', command)
    def handleInput(self, shortcut):
        if not self.handleApplicationInput(shortcut):
            return self.viewManager.handleInput(shortcut)

    def stop(self):
        self.running = False
    def shutdown(self):
        pass
    def refresh(self):
        self.screen.refresh()
    def clear(self):
        self.screen.clear()
    # Set
    def setScreen(self, screen):
        if not screen:
            return
        self.screen = screen
        self.height, self.width = self.screen.getmaxyx()

    def setProcessName(self, name = 'dragonFM'):
        """Attempts to set the process name to 'dragonFM'."""
        # Disabling the import error of setproctitle.
        # pylint: disable-msg=F0401
        try:
            from setproctitle import setproctitle
        except ImportError:
            pass
        else:
            setproctitle(name)
            return True

        try:
            from ctypes import cdll, byref, create_string_buffer
            libc = cdll.LoadLibrary('libc.so.6')
            stringBuffer = create_string_buffer(len(name) + 1)
            stringBuffer.value = bytes(name, 'UTF-8')
            libc.prctl(15, byref(stringBuffer), 0, 0, 0)
            return True
        except:
            pass
        return False
    def enter(self):
        screen = curses.initscr()
        curses.nonl()
        curses.start_color()
        curses.noecho()
        #curses.cbreak()
        curses.raw()        
        screen.keypad(False)        
        self.original_sigint_handler = signal.signal(signal.SIGINT, signal.SIG_IGN)
        self.setScreen(screen)
        self.setDisabled(False)        
    def captureSignal(self, siginit, frame):
        pass
    def leave(self):
        self.setDisabled(True)
        curses.nl()
        curses.noraw()
        curses.echo()
        #curses.nocbreak()
        self.screen.keypad(False)
        self.clear()
        curses.endwin()
        sys.stdout.flush()
        signal.signal(signal.SIGINT, self.original_sigint_handler)

    def setCursor(self, y, x):
        self.screen.move(y, x)
    def setDisabled(self, disabled):
        self.disabled = disabled
    def setIsRunning(self, running):
        self.running = running
    # Get
    def getScreenWidth(self):
        return self.width
    def getScreenHeight(self):
        return self.height
    def getClipboardManager(self):
        return self.clipboardManager
    def getCurrFolderManager(self):
        return self.viewManager.getCurrentTab().getFolderManager()    
    def getSelectionManager(self):
        return self.selectionManager
    def getProcessManager(self):
        return self.processManager
    def getSettingsManager(self):
        return self.settingsManager
    def getFileManager(self):
        return self.fileManager
    def getViewManager(self):
        return self.viewManager   
    def getInputManager(self):
        return self.inputManager
    def getCommandManager(self):
        return self.commandManager
    def getDebugManager(self):
        return self.debugManager
    def getScreen(self):
        return self.screen
    def getDragonFmPath(self):
        return self.dragonFmPath
    def getDisabled(self):
        return self.disabled
    def getIsRunning(self):
        return self.running
