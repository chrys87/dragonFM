import sys, os, pwd, grp, curses, mimetypes
from pathlib import Path

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
        self.startUpManager = self.dragonfmManager.getStartUpManager()
        self.magicMime = None
        try:
            self.magicMime = magic.Magic(mime=True)
        except:
            pass
        self.mime = mimetypes.MimeTypes()
    def getInfo(self, fullPath):
        if fullPath == '':
            return None
        if not os.path.exists(fullPath):
            return None
        pathObject = None
        try:
            pathObject = Path(fullPath)
        except:
            return None
        # basic
        name = os.path.basename(fullPath)
        path = os.path.dirname(fullPath)
        entry = {'name': name,
         'object': pathObject,
         'full': fullPath,
         'path': path,
         'marked': False,
         'type': None,
         'mode': None,
         'ino': None,
         'dev': None,
         'nlink': None,
         'uid': None,
         'uname': None,
         'gid': None,
         'gname': None,
         'size': None,
         'atime': None,
         'mtime': None,
         'ctime': None,
         'mime': None,
        }
        # type


        if pathObject.is_mount():
            entry['type'] = 'mountpoint'
            entry['mime'] = 'inode/mount-point'
        elif pathObject.is_fifo():
            entry['type'] = 'fifo'
            entry['mime'] = 'inode/fifo'
        elif pathObject.is_socket():
            entry['type'] = 'socket'
            entry['mime'] = 'inode/socket'
        elif pathObject.is_block_device():
            entry['type'] = 'block'
            entry['mime'] = 'inode/blockdevice'
        elif pathObject.is_char_device():
            entry['type'] = 'char'
            entry['mime'] = 'inode/chardevice'
        elif pathObject.is_symlink():
            entry['type'] = 'link'
            # mime is detected more below
        elif pathObject.is_file():
            entry['type'] = 'file'
            # mime is detected more below
        elif pathObject.is_dir():
            entry['type'] = 'directory'
            entry['mime'] = 'inode/directory'            
        # mimetype
        if entry['mime'] == None:
            if pathObject.is_file() or pathObject.is_symlink():
                if self.magicMime:
                    try: 
                        mime = None
                        mime = self.magicMime.from_file(fullPath)
                        if mime != None:
                            if mime != '':
                                entry['mime'] = mime
                    except:
                        pass
                if entry['mime'] == None:
                    try:
                        mime = None
                        mime = self.mime.guess_type(fullPath)[0]  
                        if mime != None:
                            if mime != '':
                                entry['mime'] = mime
                    except:
                        pass
                if entry['mime'] == None:
                    if pathObject.is_symlink():
                        entry['mime'] = 'inode/symlink'                
                    else:
                        entry['mime'] = 'application/octet-stream'
                # be a badass?
                #mime = subprocess.Popen("/usr/bin/file --mime PATH", shell=True, \
                #    stdout=subprocess.PIPE).communicate()[0]                        

        # details
        info = None
        try:
            info = pathObject.stat()
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
    def openFile(self, entry):
        if not entry:
            return
        try:
            application = self.settingsManager.get('mime', entry['mime'])
            if application == '':
                slashpos = entry['mime'].find('/')
                if slashpos != -1:
                    category = entry['mime'][:slashpos] + '/*'
                    application = self.settingsManager.get('mime', category)
            try:
                application = application.format(entry['full'])
            except:
                pass
            application = application.split(',')
        except:
            return
        self.startUpManager.setPostProcessStartup(application)
        self.dragonfmManager.stop()

    def getMimeType(self, pathObject):
        mime = None
        path = str(pathObject)
        if self.magicMime != None:
            try: 
                mime = self.magicMime.from_file(path)
                if mime != None:
                    if mime != '':
                        return mime
            except:
                pass
        try:
            mime = self.mime.guess_type(path)[0]  
            if mime != None:
                if mime != '':
                    return mime
        except:
            pass
        # be a badass?
        #mime = subprocess.Popen("/usr/bin/file --mime PATH", shell=True, \
        #    stdout=subprocess.PIPE).communicate()[0]                    
        if pathObject.is_symlink():
            mime = 'inode/symlink'
        else:
            mime = 'application/octet-stream'
        return mime
