from os.path import expanduser

def normalizePath(location, withSlash = True):
    if location == None:
        return ''
    if location == '':
        return ''
    location = expanduser(location)
    if withSlash:
        if not location.endswith('/'):
            location += '/'
    return location
