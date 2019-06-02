#!/usr/bin/env python
import os
from dragonfilemanager.core import favManager

class command():
    def __init__(self, dragonfmManager):
        self.dragonfmManager = dragonfmManager
        self.favManager = favManager.favManager(self.dragonfmManager)

    def shutdown(self):
        pass
    def getName(self):
        return _('Create Link')
    def getDescription(self):
        return _('Create a link to the current entry')
    def active(self):
        return True
    def getValue(self):
        return None
    def getShortcut(self):
        return None
    def run(self, callback = None):   
        listManager = self.dragonfmManager.getCurrListManager()
        location = listManager.getLocation()
        self.favManager.addToFav(location)

        if callback:
            callback()
