import sys, os, pwd, grp, curses, mimetypes, shlex, shutil, datetime, stat
from pathlib import Path
from distutils.dir_util import copy_tree

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
    def spawnDeleteSelectionThread(self, selection):
        if selection == None:
            return
        if selection == []:
            return
        valueParam = {}
        valueParam['selection'] = selection
        self.processManager.startInternal('remove', description = '',
            process = self.deleteSelectionThread, processParam=valueParam.copy())
    def deleteSelectionThread(self, valueParam):
        selection = valueParam['selection']
        self.deleteSelection(selection)
    def deleteSelection(self, selection):
        for fullPath in selection:
            self.deleteEntry(fullPath)
    def deleteEntry(self, fullPath):
        try:
            destPath = Path(fullPath)
            if destPath.is_symlink():
                os.unlink(str(destPath))
            elif destPath.is_dir():
                shutil.rmtree(str(destPath))
            else:
                os.remove(str(destPath))
        except Exception as e:
            pass
    def copyEntry(self, fullPath, destination):
        try:
            sourcePath = Path(fullPath)
            destPath = Path(destination)
            if sourcePath.is_dir():
                shutil.copytree(str(sourcePath), 
                    "{0}/{1}".format(destPath, sourcePath.name),
                    symlinks=False, ignore=None)
            else:
                shutil.copy2(str(sourcePath), str(destPath))
        except Exception as e:
            pass         
    
    def createLink(self, currentCursor, fullPath):
        try:
            if not os.path.exists(fullPath):
                os.symlink(currentCursor, fullPath)
        except OSError:
            pass

    def createLinkThread(self, valueParam):
        currentCursor = valueParam['currentCursor']
        fullPath = valueParam['fullPath']
        self.createLink(currentCursor, fullPath)

    def spawnCreateLinkCursorThread(self, currentCursor, fullPath):
        if currentCursor == None:
            return
        if currentCursor == '':
            return
        if fullPath == None:
            return
        if fullPath == '':
            return
        valueParam = {}
        valueParam['currentCursor'] = currentCursor
        valueParam['fullPath'] = fullPath
        
        self.processManager.startInternal('create link', description = '', 
            process = self.createLinkThread, processParam=valueParam.copy())

    def createFolder(self, fullPath):
        try:
            if not os.path.exists(fullPath):
                os.makedirs(fullPath)
        except OSError:
            pass
    def createFolderThread(self, valueParam):
        fullPath = valueParam['fullPath']
        self.createFolder(fullPath)
    def spawnCreateFolderThread(self, fullPath):
        if fullPath == None:
            return
        if fullPath == '':
            return
        valueParam = {}
        valueParam['fullPath'] = fullPath
        self.processManager.startInternal('create folder', description = '', 
            process = self.createFolderThread, processParam=valueParam.copy())
    def createFile(self, fullPath):
        try:
            if not os.path.exists(fullPath):
                os.mknod(fullPath)
        except OSError:
            pass
    def createFileThread(self, valueParam):
        fullPath = valueParam['fullPath']
        self.createFile(fullPath)
    def spawnCreateFileThread(self, fullPath):
        if fullPath == None:
            return
        if fullPath == '':
            return
        valueParam = {}
        valueParam['fullPath'] = fullPath
        self.processManager.startInternal('create file', description = '', 
            process = self.createFileThread, processParam=valueParam.copy())

    def moveEntry(self, fullPath, destination):
            try:
                sourcePath = Path(fullPath)
                destPath = Path(destination)
                shutil.move(str(sourcePath), str(destPath))
            except:
                pass
    def pasteClipboardThread(self, valueParam):
        operation = valueParam['operation']
        clipboard = valueParam['clipboard']
        newLocation = valueParam['newLocation']
        self.pasteClipboard(operation, clipboard, newLocation)
    def spawnPasteClipboardThread(self):
        if self.clipboardManager.isClipboardEmpty():
            return
        # Loop through the files and directories and copy them.
        listManager = self.dragonfmManager.getCurrListManager()

        operation = self.clipboardManager.getOperation()
        clipboard = self.clipboardManager.getClipboard()
        newLocation = listManager.getLocation()

        valueParam = {}
        valueParam['operation'] = operation
        valueParam['clipboard'] = clipboard
        valueParam['newLocation'] = newLocation

        self.processManager.startInternal(operation, description = '', 
            process = self.pasteClipboardThread, processParam=valueParam.copy())
    def pasteClipboard(self, operation, clipboard, newLocation):
        if operation in ['cut']:
            self.clipboardManager.clearClipboard()
        for fullPath in clipboard:
            if operation == 'copy':
                self.copyEntry(fullPath, newLocation)
            elif operation == 'cut':
                self.moveEntry(fullPath, newLocation)

    def getInitName(self, location, name, prefix = '', suffix = ''):
        newName = name.format('', '', '')
        i = 0
        while os.path.exists('{0}/{1}'.format(location, newName)):
            i += 1
            newName = name.format(prefix, i, suffix)
        return newName

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
         'nameOnly': os.path.splitext(name)[0],
         'ext': ''.join(os.path.splitext(name)[1:]),
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

        try:
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
        except:
            # python 3.5 doesnt have is_mount
            if pathObject.is_fifo():
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
            if application == '':
                category = '*'
                application = self.settingsManager.get('mime', category)  
        except:
            return
        application = application.format(shlex.quote(entry['full']))
        application = os.path.expandvars(application)
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
    def formatSize(self, sizeBytes):
        try:
            units = ['B', 'KB', 'MB', 'GB', 'TP', 'PB', 'EB', 'ZB', 'YB']
            currUnitIndex = 0
            while (sizeBytes / 1024) >= 1:
                sizeBytes /= 1024
                currUnitIndex += 1
            return '{0}{1}'.format(int(sizeBytes), units[currUnitIndex])
        except:
            return ''
    def formatTimestamp(self, value):
        try:
            timestampFormat = self.settingsManager.get('folder', 'timestampFormat')
            timestamp = datetime.datetime.fromtimestamp(value)
            dateString = datetime.datetime.strftime(timestamp, timestampFormat)
            return dateString
        except:
            return ''
    def formatMode(self, value):
        try:
            return stat.filemode(value)
        except:
            return ''
    def formatLink(self, value):
        try:
            if value == True:
                return _('Link')
        except:
            return ''
    def formatColumn(self, column, value):
        if column == 'size':
            return str(self.formatSize(value))
        elif column in ['ctime','atime','mtime']:
            return str(self.formatTimestamp(value))
        elif column == 'mode':
            return str(self.formatMode(value))
        elif column == 'link':
            return str(self.formatLink(value))
        else:
            return str(value)
