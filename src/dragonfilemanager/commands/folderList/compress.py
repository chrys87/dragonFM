from dragonfilemanager.core.configShellCommand import configShellCommand

class command(configShellCommand):
    def __init__(self, dragonfmManager):
        configShellCommand.__init__(self, dragonfmManager, 'compress', 'compress', ' compress a list of files', True)
    def run(self, callback = None):
        super().run('/usr/bin/touch -- works.txt')
        if callback:
            callback()
