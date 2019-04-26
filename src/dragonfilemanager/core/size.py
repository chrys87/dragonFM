#!/bin/python3
def chrys_file_size(sizeBytes):
    units = ['B', 'KB', 'MB', 'GB', 'TP', 'PB', 'EB', 'ZB', 'YB']
    currUnitIndex = 0
    while (sizeBytes / 1024) >= 1:
        sizeBytes /= 1024
        currUnitIndex += 1
    return '{0} {1}'.format(int(sizeBytes), units[currUnitIndex])

# tests
print(chrys_file_size(102))
print(chrys_file_size(1024))
print(chrys_file_size(2500))
print(chrys_file_size(30090000))
print(chrys_file_size(200000000000))
print(chrys_file_size(20000000000000))
print(chrys_file_size(4000000000000000))
print(chrys_file_size(4000000000000000000))
print(chrys_file_size(80000000000000000000000))
print(chrys_file_size(8006540000000000000000000))


'''    
def file_size(bytes):
    pb = 0
    tb = 0
    gb = 0
    mb = 0
    kb = 0
    b = 0
    while bytes >= 1000000000000000:
        bytes -= 1000000000000000
        pb += 1
    while bytes >= 1099511627776:
        bytes -= 1099511627776
        tb += 1
    while bytes >= 1000000000:
        bytes -= 1000000000
        gb += 1
    while bytes >= 1000000:
        bytes -= 1000000
        mb += 1
    while bytes >= 1000:
        bytes -= 1000
        kb += 1
    if bytes > 0:
        b = bytes
    if pb > 0:
        message = str(pb)
        if tb > 0:
            message += "." + str(tb % 100)
        message += "PB"
        return message
    if tb > 0:
        message = str(tb)
        if gb > 0:
            message += "." + str(gb % 100)
        message += "TB"
        return message
    if gb > 0:
        message = str(gb)
        if mb > 0:
            message += "." + str(mb % 100)
        message += "GB"
        return message
    if mb > 0:
        message = str(mb)
        if kb > 0:
            message += "." + str(kb % 100)
        message += "MB"
        return message
    if kb > 0:
        message = str(kb)
        if b > 0:
            message += "." + str(b % 100)
        message += "KB"
        return message
    return str(b) + "B"
'''
