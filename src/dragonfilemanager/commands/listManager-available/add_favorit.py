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
        return _('Add Favorite')
    def getDescription(self):
        return _('Add current Entry to Favorites')
    def active(self):
        return True
    def visible(self):
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
