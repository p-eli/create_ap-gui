#!/usr/bin/python3
__author__ = 'Jakub Pelikan'
from createApGui.trayIcon import TrayIcon
from createApGui.userSetting import UserSetting
from createApGui.createEditAp import CreateEditAp
from createApGui.language import Languge
from createApGui.runningAp import RunningAp
from gi.repository import Gtk
import os

class Gui():
    def __init__(self):


        if os.geteuid() != 0:
            self.window = Gtk.Window()
            dialog = Gtk.MessageDialog(self.window, 0, Gtk.MessageType.ERROR, Gtk.ButtonsType.OK, 'Root privileges are required for running Create AP')
            dialog.format_secondary_text('Please run as root')
            dialog.run()
            dialog.destroy()
        else:
            self.setting={'userSetting':UserSetting(),'lang':None, 'path':self.getPath(), 'runningAp':None, 'createEditAp':None, 'iconPath':os.path.join(self.getPath(),'image','icon.png')}
            self.setting['language'] = Languge(self.setting)
            self.setting['runningAp'] = RunningAp(self.setting)
            if not os.path.exists(self.setting['userSetting'].saveFile['path']):
                os.makedirs(self.setting['userSetting'].saveFile['path'])
            if not self.setting['userSetting'].saveFile['fileName'] in os.listdir(self.setting['userSetting'].saveFile['path']):
                self.firstStart()
            else:
                self.start()

    def firstStart(self):
        self.setting['userSetting'].save()
        self.setting['createEditAp'] = CreateEditAp(self.setting)
        self.setting['createEditAp'].show()
        self.start()

    def start(self):
        self.setting['userSetting'] = self.setting['userSetting'].load()
        tray = TrayIcon(self.setting)
        Gtk.main()

    def getPath(self):
        root = __file__
        if os.path.islink(root):
            root = os.path.realpath(root)
        return(os.path.dirname (os.path.abspath (root)))

