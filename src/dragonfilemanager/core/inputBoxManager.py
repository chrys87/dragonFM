import os
from os.path import expanduser
import curses
import curses.ascii

def rectangle(win, uly, ulx, lry, lrx):
    """Draw a rectangle with corners at the provided upper-left
    and lower-right coordinates.
    """
    win.vline(uly+1, ulx, curses.ACS_VLINE, lry - uly - 1)
    win.hline(uly, ulx+1, curses.ACS_HLINE, lrx - ulx - 1)
    win.hline(lry, ulx+1, curses.ACS_HLINE, lrx - ulx - 1)
    win.vline(uly+1, lrx, curses.ACS_VLINE, lry - uly - 1)
    win.addch(uly, ulx, curses.ACS_ULCORNER)
    win.addch(uly, lrx, curses.ACS_URCORNER)
    win.addch(lry, lrx, curses.ACS_LRCORNER)
    win.addch(lry, ulx, curses.ACS_LLCORNER)

class inputBoxManager:
    """Editing widget using the interior of a window object.
     Supports the following Emacs-like key bindings:
    Ctrl-A      Go to left edge of window.
    Ctrl-B      Cursor left, wrapping to previous line if appropriate.
    Ctrl-D      Delete character under cursor.
    Ctrl-E      Go to right edge (stripspaces off) or end of line (stripspaces on).
    Ctrl-F      Cursor right, wrapping to next line when appropriate.
    Ctrl-G      Terminate, returning the window contents.
    Ctrl-H      Delete character backward.
    Ctrl-J      Terminate if the window is 1 line, otherwise insert newline.
    Ctrl-K      If line is blank, delete it, otherwise clear to end of line.
    Ctrl-L      Refresh screen.
    Ctrl-N      Cursor down; move down one line.
    Ctrl-O      Insert a blank line at cursor location.
    Ctrl-P      Cursor up; move up one line.
    Move operations do nothing if the cursor is at an edge where the movement
    is not possible.  The following synonyms are supported where possible:
    KEY_LEFT = Ctrl-B, KEY_RIGHT = Ctrl-F, KEY_UP = Ctrl-P, KEY_DOWN = Ctrl-N
    KEY_BACKSPACE = Ctrl-h
    """
    def __init__(self, parentWindow, insert_mode=True, description = []):
        self.init()
        self.setInsertMode(insert_mode)
        self.setParentWindow(parentWindow)
        self.setDescription(description)
    def setDescription(self, description):
        self.description = description
    def getDescription(self):
        return self.description
    def init(self):
        self.stripspaces = 1
        self.lastcmd = None
        self.parentWindow = None
        self.win = None
        self.headerOffset = 0
        self.initValue = ''
        self.description = []
        self.locationMode = False
        self.location = ''
        self.acceptFiles = False
        self.acceptFolders = False
        self.multipleChoiceMode = False
        self.validValues = []
        self.confirmationMode = False
        self.editable = True
        self.defaultValue = ''
        self.parentWindow = None
        self.exitStatus = None # None = error, True = ok, False = cancle
    def setParentWindow(self, parentWindow):
        self.parentWindow = parentWindow
    def createWindow(self):
        parentSizeY, parentSizeX = self.parentWindow.getmaxyx()
        ncols, nlines = parentSizeX, self.calculateMaxHight()
        self.win = curses.newwin(nlines, ncols, 0, 0)
        self.win.keypad(True)
        self._update_max_yx()
        self.win.erase()

    def close(self):
        if self.parentWindow:
            self.parentWindow.touchwin()
    def setInsertMode(self, insert_mode):
        self.insert_mode = insert_mode
    def _update_max_yx(self):
        maxy, maxx = self.win.getmaxyx()
        self.maxy = maxy - 1
        self.maxx = maxx - 1

    def _end_of_line(self, y):
        """Go to the location of the first blank on the given line,
        returning the index of the last non-blank character."""
        self._update_max_yx()
        last = self.maxx
        while True:
            if curses.ascii.ascii(self.win.inch(y, last)) != curses.ascii.SP:
                last = min(self.maxx, last+1)
                break
            elif last == 0:
                break
            last = last - 1
        return last

    def _insert_printable_char(self, ch):
        self._update_max_yx()
        (y, x) = self.win.getyx()
        backyx = None
        while y < self.maxy or x < self.maxx:
            if self.insert_mode:
                oldch = self.win.inch()
            # The try-catch ignores the error we trigger from some curses
            # versions by trying to write into the lowest-rightmost spot
            # in the window.
            try:
                self.win.addch(ch)
            except curses.error:
                pass
            if not self.insert_mode or not curses.ascii.isprint(oldch):
                break
            ch = oldch
            (y, x) = self.win.getyx()
            # Remember where to put the cursor back since we are in insert_mode
            if backyx is None:
                backyx = y, x

        if backyx is not None:
            self.win.move(*backyx)

    def do_command(self, ch):
        "Process a single editing command."
        self._update_max_yx()
        (y, x) = self.win.getyx()
        self.lastcmd = ch
        # debug
        #self.win.addstr(self.headerOffset, 0, str(int(ch)))
        if curses.ascii.isprint(ch):
            if not self.getEditable():
                return True
            if y < self.maxy or x < self.maxx:
                self._insert_printable_char(ch)
        elif ch == curses.ascii.SOH:                           # ^a
            self.win.move(y, 0)
        elif ch in (curses.ascii.STX,curses.KEY_LEFT, curses.ascii.BS,curses.KEY_BACKSPACE, curses.ascii.DEL):
            if x > 0:
                self.win.move(y, x-1)
            elif y == self.headerOffset:
                pass
            elif self.stripspaces:
                self.win.move(y-1, self._end_of_line(y-1))
            else:
                self.win.move(y-1, self.maxx)
            if ch in (curses.ascii.BS, curses.KEY_BACKSPACE, curses.ascii.DEL):
                if not self.getEditable():
                    return True
                self.win.delch()
        elif ch == curses.ascii.EOT:                           # ^d
            if not self.getEditable():
                return True
            self.win.delch()
        elif ch == curses.ascii.ENQ:                           # ^e
            if self.stripspaces:
                self.win.move(y, self._end_of_line(y))
            else:
                self.win.move(y, self.maxx)
        elif ch in (curses.ascii.ACK, curses.KEY_RIGHT):       # ^f
            if x < self.maxx:
                self.win.move(y, x+1)
            elif y == self.maxy:
                pass
            else:
                self.win.move(y+1, 0)
        elif ch in [curses.ascii.BEL, curses.ascii.NL, curses.ascii.CR]:
            # complete
            self.setExitStatus(True)
            return False
        #elif ch in [curses.ascii.NL]:                            # ^j
            #if self.maxy == 0:
            #    return 0
            #elif y < self.maxy:
            #    return 0
            #    self.win.move(y+1, 0)
        elif ch in [curses.ascii.ESC, 17]: # 17 = ^q
            # abbording
            self.setExitStatus(False)
            return False
        elif ch == curses.ascii.VT:                            # ^k
            if not self.getEditable():
                return True
            if x == 0 and self._end_of_line(y) == 0:
                self.win.deleteln()
            else:
                # first undo the effect of self._end_of_line
                self.win.move(y, x)
                self.win.clrtoeol()
        elif ch == curses.ascii.FF:                            # ^l
            self.win.refresh()
        elif ch in (curses.ascii.SO, curses.KEY_DOWN):         # ^n
            if y < self.maxy:
                self.win.move(y+1, x)
                if x > self._end_of_line(y+1):
                    self.win.move(y+1, self._end_of_line(y+1))
        elif ch == curses.ascii.SI:                            # ^o
            if not self.getEditable():
                return True
            self.win.insertln()
        elif ch == curses.ascii.TAB: # autocompletion
            if not self.getEditable():
                return True
            pass
        elif ch in (curses.ascii.DLE, curses.KEY_UP):          # ^p
            if y > self.headerOffset:
                self.win.move(y-1, x)
                if x > self._end_of_line(y-1):
                    self.win.move(y-1, self._end_of_line(y-1))
        return True

    def gather(self):
        "Collect and return the contents of the window."
        result = ""
        self._update_max_yx()
        for y in range(self.headerOffset, self.maxy+1):
            self.win.move(y, 0)
            stop = self._end_of_line(y)
            if stop == 0 and self.stripspaces:
                continue
            for x in range(self.maxx+1):
                if self.stripspaces and x >= stop:
                    break
                result = result + chr(curses.ascii.ascii(self.win.inch(y, x)))
            #if self.maxy > 0:
            #    result = result + "\n"
        return result
    def getValidValues(self):
        return self.validValues
    def setConfirmationMode(self, mode):
        if not mode:
            self.setMultipleChoiceMode(mode)
        else:
            answers = ['yes', 'y', '1', # yes
                       'no', 'n', '0', # no
                       'quit', 'cancel', 'q', 'c' # quit
                      ]
            self.setMultipleChoiceMode(mode, answers)
        self.confirmationMode = mode
    def getConfirmationMode(self):
        return self.confirmationMode
    def setMultipleChoiceMode(self, mode, validValues = []):
        if mode:
            self.validValues = validValues
        else:
            self.validValues = []
        self.multipleChoiceMode = mode
    def getMultipleChoiceMode(self):
        return self.multipleChoiceMode
    def setLocationMode(self, mode, location, acceptFolders = True, acceptFiles = False):
        if not mode:
            self.acceptFolders = False
            self.acceptFiles = False
            self.location = ''
        else:
            self.acceptFolders = acceptFolders
            self.acceptFiles = acceptFiles
            self.location = expanduser(location)
        self.locationMode = mode
    def getLocationMode(self):
        return self.locationMode
    def getLocation(self):
        return self.location
    def setEditable(self, editable):
        self.editable = editable
    def getEditable(self):
        return self.editable
    def setDefaultValue(self, defaultValue):
        self.defaultValue = defaultValue
    def getDefaultValue(self):
        return self.defaultValue
    def isValidValues(self):
        exitStatus = self.getExitStatus()
        # cancle is also always valid
        if exitStatus == False:
            return True
        currValue = self.getCurrValue()
        # no input yet/ error
        if currValue == None:
            return False
        isValid = True

        # check for file or path
        if self.getLocationMode():
            if currValue == '':
                return False
            currValue = expanduser(currValue)
            try:
                os.chdir(self.getLocation())
                currValue = os.path.abspath(currValue)
            except:
                pass
            if currValue.endswith('/') and currValue != '/':
                currValue = currValue[:-1]
            self.setCurrValue(currValue)
            validLocation = False
            if self.acceptFiles:
                if os.path.isfile(currValue):
                    validLocation = True
            if self.acceptFolders:
                if os.path.isdir(currValue):
                    validLocation = True
            isValid = validLocation
            # not a valid path/ File
            if not isValid:
                return isValid 
        # check for multiple choice
        if self.getMultipleChoiceMode():
            isValid = currValue in self.getValidValues()
            # is not a valid choice
            if not isValid:
                return isValid 
        return isValid
    def setInitValue(self, initValue):
        self.initValue = initValue
    def getInitValue(self):
        return self.initValue
    def getCurrValue(self):
        return self.currValue
    def setCurrValue(self, currValue):
        if self.getDefaultValue() != '':
            if currValue == '':
                currValue = self.getDefaultValue()
        self.currValue = currValue
    def setExitStatus(self, exitStatus):
        self.exitStatus = exitStatus
    def getExitStatus(self):
        return self.exitStatus
    def processConfirmationMode(self):
        if not self.getConfirmationMode():
            return
        # normalize yes, no, cancle for confirmation mode
        exitStatus = self.getExitStatus()
        if exitStatus == False:
            self.setCurrValue('q')
            return
        value = self.getCurrValue()
        # normalize answer for confirmation mode
        # quit
        if value in ['quit','cancel','q', 'c']:
            self.setCurrValue('q')
            self.setExitStatus(False)
        # yes
        elif value in ['yes', 'y', '1']:
            self.setCurrValue('y')
            self.setExitStatus(True)
        # no
        elif value in ['no', 'n', '0']:
            self.setCurrValue('n')
            self.setExitStatus(True)
    def printHeader(self):
        description = self.getDescription()
        for d in description:
            self.win.addstr(self.headerOffset, 0, d)
            self.headerOffset += 1
        defaultValue = self.getDefaultValue()
        if defaultValue != '':
            self.win.addstr(self.headerOffset, 0, 'Default Value: ({})'.format(defaultValue))
            self.headerOffset += 1
    def calculateMaxHight(self):
        # input box
        height = 1
        # description
        height += len(self.getDescription())
        # init value
        if self.getDefaultValue() != '':
            height += 1
        return height
    def show(self, validate=None):
        "Edit in the widget window and collect the results."
        self.createWindow()
        self.setCurrValue(None)
        self.printHeader()
        while not self.isValidValues():
            if self.getInitValue() != '' :
                self.win.addstr(self.headerOffset, 0, self.getInitValue())
            else:
                self.win.move(self.headerOffset, 0)
            self.win.clrtoeol()
            while True:
                ch = self.win.getch()
                if validate:
                    ch = validate(ch)
                if not ch:
                    continue
                if not self.do_command(ch):
                    break
                self.win.refresh()
            self.setCurrValue(self.gather())
            self.processConfirmationMode()
        self.close()
        del self.win
        return self.getExitStatus(), self.getCurrValue()

if __name__ == '__main__':
    def test_editbox(stdscr):
        uly, ulx = 2, 1
        stdscr.addstr(0, 0, "Parent Window")
        stdscr.refresh()
        stdscr.getch()
        inputBox = inputBoxManager(stdscr, description=['Do You realy want?','q = quit','y = yes','n = nope'])
        inputBox.setDefaultValue('test')
        #inputBox.setMultipleChoiceMode(True,['q', 'y', 'n'])
        inputBox.setLocationMode(True, '/tmp/playzone',True,True)
        inputBox.setConfirmationMode(True)
        #inputBox.setEditable(False)
        #inputBox.setInitValue('/tmp/playzone')
        status, text = inputBox.show()
        stdscr.erase()
        stdscr.addstr(0, ulx, "Parent Window")
        stdscr.addstr(1, ulx, "Dialog was closed                      ")
        stdscr.addstr(2, ulx, 'Staus: {}; Value: {}'.format(status,text))
        stdscr.getch()

    curses.wrapper(test_editbox)
