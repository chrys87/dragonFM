import sys,os
import curses

class contextMenuManager():
    def __init__(self, screen):
        self.screen = None
        self.height = 0
        self.width = 0
        self.setScreen(screen)
    def enter(self):
        self.clear()
        self.screen.refresh()
    def leave(self):
        pass
    def draw(self):
        self.screen.addstr(0, 0, 'Menu')
    def handleInput(self, key):
        return False
    def refresh(self):
        self.screen.refresh()
    def clear(self):
        self.screen.clear()
    def setScreen(self, screen):
        if not screen:
            return
        self.screen = screen
        self.height, self.width = self.screen.getmaxyx()

