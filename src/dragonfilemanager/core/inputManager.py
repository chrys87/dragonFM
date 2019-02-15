import sys,os
import curses

class inputManager():
    def __init__(self):
        self.screen = None
    def get(self):
        if not self.screen:
            return None
    def setScreen(self, screen)
        if screen ==  self.screen:
            return
        self.screen = screen
