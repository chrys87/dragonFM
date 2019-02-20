import sys, os, curses

class fileManager():
    def __init__(self, dragonfmManager):
        self.dragonfmManager = dragonfmManager
        self.screen = self.dragonfmManager.getScreen()
        self.settingsManager = self.dragonfmManager.getSettingsManager()
    def getInfo(self, fullPath):
        if fullPath == '':
            return None
        if not os.path.exists(fullPath):
            return None
        # basic
        name = os.path.basename(fullPath)
        path = os.path.dirname(fullPath)
        entry = {'name': name,
         'full': fullPath,
         'path': path,
         'marked': False,
         'type': None,
         'mode', None,
         'ino', None,
         'dev', None,
         'nlink', None,
         'uid', None,
         'uname': None,
         'gid', None,
         'gname': None,
         'size', None,
         'atime', None,
         'mtime', None,
         'ctime', None,
        }
        # type
        if os.path.isfile(fullPath):
            entry['type'] = 'file'
        elif os.path.isdir(fullPath):
            entry['type'] = 'directory'
        elif os.path.islink(fullPath):
            entry['type'] = 'link'
        elif os.path.ismount(fullPath):
            entry['type'] = 'mountpoint'
        # details
        info = None
        try:
            info = os.stat(fullPath)
            entry['mode'] = info.st_mode
            entry['ino'] = 2 ** 32 + info.st_ino + 1  # Ensure st_ino > 2 ** 32
            entry['dev'] = info.st_dev
            entry['nlink'] = info.st_nlink
            entry['uid'] = info.st_uid
            entry['uname'] = username
            entry['gid'] = info.st_gid
            entry['gname'] = groupname
            entry['size'] = info.st_size
            entry['atime'] = info.st_atime
            entry['mtime'] = info.st_mtime
            entry['ctime'] = info.st_ctime
        except:
            pass
        return entry.copy()
    def openFile(self, fullPath):
        try:
            os.execlp('nano', 'nano', fullPath)
        except:
            return False
        return True
