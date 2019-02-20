import sys, os, pwd, grp, curses, mimetypes 
magicAvailable = False
try:
    import magic
    magicAvailable = True
except:
    pass
    

class fileManager():
    def __init__(self, dragonfmManager):
        self.dragonfmManager = dragonfmManager
        self.screen = self.dragonfmManager.getScreen()
        self.settingsManager = self.dragonfmManager.getSettingsManager()
        self.magicMime = magic.Magic(mime=True)
        self.mime = mimetypes.MimeTypes()
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
         'mime': None,
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
        # mimetype
        try: 
            entry['mime'] = self.magicMime.from_file(fullPath)
        except:
            try:
                entry['mime'] = self.mime.guess_type(fullPath)[0]
            except:
                entry['mime'] = 'application/octet-stream'
        
        # details
        info = None
        try:
            info = os.stat(fullPath)
            entry['mode'] = info.st_mode
            entry['ino'] = 2 ** 32 + info.st_ino + 1  # Ensure st_ino > 2 ** 32
            entry['dev'] = info.st_dev
            entry['nlink'] = info.st_nlink
            entry['uid'] = info.st_uid
            try:
                entry['uname'] = pwd.getpwuid( info.st_uid ).pw_name
            except:
                pass
            entry['gid'] = info.st_gid
            try:
                entry['gname'] = grp.getgrgid( info.st_gid ).gr_name
            except:
                pass
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
