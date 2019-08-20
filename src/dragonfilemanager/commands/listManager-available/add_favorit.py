from dragonfilemanager.core.baseCommand import baseCommand
import os
from dragonfilemanager.core import favManager

class command(baseCommand):
    def __init__(self, dragonfmManager):
        baseCommand.__init__(self, dragonfmManager)
        self.dragonfmManager = dragonfmManager
        self.favManager = favManager.favManager(self.dragonfmManager)

        self.setName('Add Favorite')
        self.setDescription('Add current Entry to Favorites')
    def active(self):
        return self.commandManager.isCommandValidForFileOperation(minSelection = 1, maxSelection = 1)
    def run(self, callback = None):   
        listManager = self.dragonfmManager.getCurrListManager()
        location = listManager.getLocation()
        self.favManager.addToFav(location)

        if callback:
            callback()
