import sys,os
import curses

class folderManager():
    def __init__(self):
        self.screen = None
    def draw(self, activeScreen):
        self.activeScreen = activeScreen
    def drawWrapper(self):
        curses.wrapper(self.draw)
    def handleInput(self):
        pass
    def getScreen(self):
        return self.screen
