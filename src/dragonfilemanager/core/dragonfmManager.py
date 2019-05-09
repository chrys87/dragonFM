import sys, os, threading, curses, time, inspect, termios, fcntl, locale, copy

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
        self.old_term_attr = None
        self.new_term_attr = None
        self.disabled = True
        self.screen = None
        self.height = 0
        self.width = 0
        self.encoding = 'UTF8'
        self.currentdir = os.path.dirname(os.path.realpath(os.path.abspath(inspect.getfile(inspect.currentframe()))))
        self.dragonFmPath = os.path.dirname(self.currentdir)
        self.settingsManager = settingsManager.settingsManager(self)
        self.settingsManager.parseCliArgs()
        if not self.settingsManager.loadSettings():
            raise IOError('could not load settingsfile, maybe it is not readable or does not exist.')
        self.processManager = processManager.processManager(self)
        self.clipboardManager = clipboardManager.clipboardManager(self)
        self.debugManager = debugManager.debugManager(self)
        self.fileManager = fileManager.fileManager(self)
        self.selectionManager = selectionManager.selectionManager(self)
        self.viewManager = None
        self.inputManager = None
        self.commandManager = commandManager.commandManager(self)
        self.runningLock = threading.RLock()
        self.disabledLock = threading.RLock()
        self.updateLock = threading.RLock()

        self.initEncoding()
        self.initTerminal()
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
        while self.getRunning():
            if self.getDisabled():
                continue
            self.update()
            try:
                shortcut = self.inputManager.get()
            except:
                continue
            if shortcut == None:
                continue
            if shortcut == curses.ERR:
                continue
            self.handleInput(shortcut)
        self.shutdown()
    def update(self):
        if not self.getRunning():
            return
        if self.getDisabled():
            return
        self.updateLock.acquire(True)
        self.viewManager.update()
        self.updateLock.release()
    def handleApplicationInput(self, shortcut):
        command = self.settingsManager.getShortcut('application-keyboard', shortcut)
        if command == '':
            return False
        return self.commandManager.runCommand('application', command)
    def handleInput(self, shortcut):
        if not self.handleApplicationInput(shortcut):
            return self.viewManager.handleInput(shortcut)
    def initTerminal(self):
        if self.old_term_attr == None:
            self.old_term_attr = termios.tcgetattr(sys.stdin)
        self.new_term_attr = copy.deepcopy(self.old_term_attr)
        # Disable extended input and output processing in our terminal
        self.new_term_attr[3] &= ~termios.IEXTEN
        self.new_term_attr[3] &= ~termios.OPOST
        # Enable interpretation of the flow control characters in our terminal
        self.new_term_attr[3] &= ~termios.IXON
        # Disable interpretation of the special control keys in our terminal
        self.new_term_attr[3] &= ~termios.ISIG
        # don't handle ^C / ^Z / ^\
        self.new_term_attr[6][termios.VINTR] = 0
        self.new_term_attr[6][termios.VQUIT] = 0
        self.new_term_attr[6][termios.VSUSP] = 0
        # store the old fcntl flags
        #self.oldflags = fcntl.fcntl(sys.stdin, fcntl.F_GETFL)
        # fcntl.fcntl(self.pty, fcntl.F_SETFD, fcntl.FD_CLOEXEC)
        # make the PTY non-blocking
        # fcntl.fcntl(sys.stdin, fcntl.F_SETFL, self.oldflags | os.O_NONBLOCK)
    def stop(self):
        self.setRunning(False)
    def shutdown(self):
        pass
    def refresh(self):
        self.screen.refresh()
    def clear(self):
        self.screen.clear()
    def erase(self):
        self.screen.erase()
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
        if self.new_term_attr != None:
            termios.tcsetattr(sys.stdin, termios.TCSANOW, self.new_term_attr)
        curses.raw()
        curses.nonl()
        curses.noecho()
        curses.start_color()
        #curses.cbreak()
        screen.keypad(True)
        self.setScreen(screen)
        self.setDisabled(False) 

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
        if self.old_term_attr != None:
            termios.tcsetattr(sys.stdin, termios.TCSANOW, self.old_term_attr)
    def setCursor(self, y, x):
        self.screen.move(y, x)
    def setDisabled(self, disabled):
        self.disabledLock.acquire(True)
        self.disabled = disabled
        self.disabledLock.release()
    def setRunning(self, running):
        self.runningLock.acquire(True)
        self.running = running
        self.runningLock.release()
    def initEncoding(self):
        locale.setlocale(locale.LC_ALL, '')
        self.encoding =locale.getpreferredencoding()
    # Get
    def getEncoding(self):
        return self.encoding
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
        self.disabledLock.acquire(True)
        disabled = self.disabled
        self.disabledLock.release()
        return disabled
    def getRunning(self):
        self.runningLock.acquire(True)
        running = self.running
        self.runningLock.release()
        return running
