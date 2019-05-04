import sys, os, pwd, grp, curses, mimetypes, shlex, shutil
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
        self.processManager = self.dragonfmManager.getProcessManager()
        self.clipboardManager = self.dragonfmManager.getClipboardManager()
        self.magicMime = None
        try:
            self.magicMime = magic.Magic(mime=True)
        except:
            pass
        self.mime = mimetypes.MimeTypes()
    def deleteSelection(self, selection):
        if selection == None:
            return
        if selection == []:
            return
        # Loop through the files and directories and delete them.
        for fullPath in selection:
            self.deleteEntry(fullPath)
    def deleteEntry(self, fullPath):
        try:
            if os.path.isdir(fullPath):
                shutil.rmtree(fullPath)
            else:
                os.remove(fullPath)
        except Exception as e:
            pass             
    def copyEntry(self, fullPath, destination):
        try:
            if os.path.isdir(fullPath):
                shutil.copytree(fullPath, destination, symlinks=False, ignore=None)
            else:
                shutil.copy2(fullPath, destination)
        except Exception as e:
            pass         
            
    def moveEntry(self, fullPath, destination):
            try:
                shutil.move(fullPath, destination)
            except:
                pass              
    def pasteClipboard(self):
        if self.clipboardManager.isClipboardEmpty():
            return
        # Loop through the files and directories and copy them.
        folderManager = self.dragonfmManager.getCurrFolderManager()
        
        operation = self.clipboardManager.getOperation()
        clipboard = self.clipboardManager.getClipboard()
        newLocation = folderManager.getLocation()
        
        value = {}
        value['operation'] = operation
        value['clipboard'] = clipboard
        value['newLocation'] = newLocation
        if operation in ['cut']:
            self.clipboardManager.clearClipboard()
        self.processManager.startInternal(operation, description = '', 
            process = self.pasteClipboardThread, value=value.copy())
    def pasteClipboardThread(self, value):
        operation = value['operation']
        clipboard = value['clipboard']
        newLocation = value['newLocation']
        for fullPath in clipboard:
            if operation == 'copy':
                self.copyEntry(fullPath, newLocation)
            elif operation == 'cut':
                self.moveEntry(fullPath, newLocation)
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
         'link': False
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
            # mime is detected more below
        elif pathObject.is_file():
            entry['type'] = 'file'
            # mime is detected more below
        elif pathObject.is_dir():
            entry['type'] = 'directory'
            entry['mime'] = 'inode/directory'  
        if pathObject.is_symlink():
            entry['link'] = True
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
    def openFile(self, entry, pwd = ''):
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
                application = application.format(shlex.quote(entry['full']))
            except:
                pass
        except:
            return
        self.processManager.startExternal(application, pwd=pwd)

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
