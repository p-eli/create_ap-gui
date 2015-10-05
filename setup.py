#!/usr/bin/python3
__author__ = 'Jakub Pelikan'
from setuptools import setup
import sys

def getDataFiles():
    if sys.platform == 'linux':
       return [('/usr/share/applications', ['postinst/createApGui.desktop']),('/usr/share/pixmaps/', ['postinst/createApGui.png'])]
    else:
        return []

setup(
    name='create_ap-gui',
    version='1.2',
    description='Easy create Access point',
    long_description='Gui application for easy creating access points. Application allows save configuration for quickly create AP.',
    url='-',
    author='Jakub Pelikan',
    author_email='jakub.pelikan@gmail.com',
    keywords=['AP', 'gui', 'access point'],
    include_package_data=True,
    packages=['createApGui'],
    classifiers=[
			'Programming Language :: Python :: 3',
			'Operating System :: POSIX :: Linux',
            'Development Status :: 3 - Alpha',
			'License :: OSI Approved :: GNU General Public License v3 (GPLv3)'
			],
    entry_points = {
        'gui_scripts': [
            'create_ap-gui = createApGui.__main__:main'
        ]
    },
    #install_requires=['gi'],
    data_files= getDataFiles(),
)

