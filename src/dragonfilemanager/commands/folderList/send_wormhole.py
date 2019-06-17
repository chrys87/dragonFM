#!/usr/bin/env python
import time, fcntl, os, subprocess, zipfile
from sh import wormhole

class command():
    def __init__(self, dragonfmManager):
        self.dragonfmManager = dragonfmManager
        self.screen = self.dragonfmManager.getScreen()
        self.settingsManager = self.dragonfmManager.getSettingsManager()
        self.selectionManager = self.dragonfmManager.getSelectionManager()
        self.clipboardManager = self.dragonfmManager.getClipboardManager()
    def shutdown(self):
        pass
    def getName(self):
        return _('Wormhole')
    def getDescription(self):
        return _('Wormhole current entry or selection')
    def active(self):
        return True
    def getValue(self):
        return None
    def getShortcut(self):
        return None
    def run(self, callback = None):
        listManager = self.dragonfmManager.getCurrListManager()

        # Get the files and directories that were selected.
        selected = self.selectionManager.getSelectionOrCursorCurrentTab()
        filename = ''
        if len(selected) == 0:
            return
        elif len(selected) == 1:
            filename = selected[0]
        else:
            filename = '{0}.zip'.format('/tmp/wh')
            self.zipFileList(selected, filename)
        # wromhole writes to stderr ?!
        proc = subprocess.Popen(['wormhole', 'send', filename], stdout=subprocess.PIPE, stderr=subprocess.PIPE)

        stdoutdata = None
        while stdoutdata == None:
            time.sleep(0.2)
            stdoutdata = self.nonBlockRead(proc.stderr)

        lines = stdoutdata.decode('utf8').split('\n')
        lines = list(filter(None, lines))
        # create content
        for i in range(len(lines)):
            lines[i] = lines[i].rstrip()
        lines = ['Wormhole:'] + lines

        inputDialog = self.dragonfmManager.createInputDialog(description = lines)
        inputDialog.setEditable(False)
        exitStatus, linkName = inputDialog.show()
        if callback:
            callback()

    def nonBlockRead(self, output):
        ''' even in a thread, a normal read with block until the buffer is full '''
        fd = output.fileno()
        fl = fcntl.fcntl(fd, fcntl.F_GETFL)
        fcntl.fcntl(fd, fcntl.F_SETFL, fl | os.O_NONBLOCK)
        try:
            return output.read()
        except:
            return None

    def zipFileList(self, pathlist, filename):
        zipf = zipfile.ZipFile(filename, 'w', zipfile.ZIP_DEFLATED)
        for path in pathlist:
            if os.path.isfile(path):
                zipf.write(os.path.abspath(path), arcname=path)
            else:
                for folder in os.listdir(path):
                    for root, dirs, files in os.walk(os.path.join(path, folder)):
                        for filename in files:
                            zipf.write(os.path.abspath(os.path.join(root, filename)), arcname=filename)
        zipf.close()
