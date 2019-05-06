#!/bin/python
#https://python-packaging.readthedocs.io/en/latest/minimal.html
import os, glob, sys
import os.path
from shutil import copyfile
from setuptools import find_packages
from setuptools import setup

dragonFileManagerVersion = '0.0.1'
packageVersion = 'post1'

# handle flags for package manager like aurman and pacaur.
forceSettings = False
if "--force-settings" in sys.argv:
    forceSettings = True
    sys.argv.remove("--force-settings")

data_files = []
directories = glob.glob('config/*')
for directory in directories:
    files = glob.glob(directory+'/*')
    destDir = ''
    if 'config/settings' in directory:
        destDir = '/etc/dragonfm/settings'
        if not forceSettings:
            try:
                del(files[files.index('config/settings/settings.conf')])
            except:
                pass
    elif 'config/plugins' in directory:
        destDir = '/usr/share/dragonfm/plugins'
    if destDir != '':
        data_files.append((destDir, files))

data_files.append((destDir, files))
#data_files.append(('/usr/share/man/man1', ['docu/dragonfm.1']))

def read(fname):
    return open(os.path.join(os.path.dirname(__file__), fname)).read()

setup(
    # Application name:
    name="dragon-filemanager",
    # Version number:
    version=dragonFileManagerVersion + '.' + packageVersion,
    # description
    description="A command line file manager for Linux.",
    long_description=read('README.md'),
    keywords=['file', 'directory', 'folder', 'filemanager', 'a11y', 'accessibility', 'terminal', 'TTY', 'console'],
    license="License :: OSI Approved :: GNU General Public License v3 or later (GPLv3+)",
    url="https://github.com/chrys87/dragonfm/",
    download_url = 'https://github.com/chrys87/dragonfm/archive/' + dragonFileManagerVersion + '.tar.gz',	
    classifiers=[
        "Programming Language :: Python",
        "License :: OSI Approved :: GNU Lesser General Public License v3 (LGPLv3)",
        "Development Status :: 5 - Production/Stable",
        "Topic :: Multimedia :: Sound/Audio :: Speech",
        "Environment :: Console",
    ],

    # Application author details:
    author="Chrys and Storm_dragon",
    author_email="chrysg@linux-a11y.org",

    # Packages
    packages=find_packages('src/'),
    package_dir={'': 'src/'},
    scripts=['src/dragonfm'],

    # Include additional files into the package
    include_package_data=True,
    zip_safe=False,

    data_files=data_files,

    # Dependent packages (distributions)
    install_requires=[
        "dbus-python>=1.2.8",
        "setuptools",
        "pexpect"
    ],

)

if not forceSettings:
    print('')
    # create settings file from example if not exist
    if not os.path.isfile('/etc/dragonfm/settings/settings.conf'):
        try:
            copyfile('/etc/dragonfm/settings/settings.conf.example', '/etc/dragonfm/settings/settings.conf')
            print('create settings file in /etc/dragonfm/settings/settings.conf')
        except:
            pass
    else:
        print('settings.conf file found. It is not overwritten automatically')
