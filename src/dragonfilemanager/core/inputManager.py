import sys,os
import curses

class inputManager():
    def __init__(self, screen):
        self.screen = screen
    def get(self):
        if not self.screen:
            return None
        return self.screen.getkey()
    def setScreen(self, screen):
        self.screen = screen
