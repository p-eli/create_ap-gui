#!/usr/bin/python3
__author__ = 'Jakub Pelikan'
from gi.repository import Gtk
from  createApGui.trayRightClickMenu import TrayRightClickMenu
from createApGui.createEditAp import CreateEditAp

class TrayIcon(Gtk.StatusIcon):
    def __init__(self, setting):
        Gtk.StatusIcon.__init__(self)
        self.setting = setting
     #   self.setting['runningAp'].updatingPage['tray'] = self.updateState
        self.initTray()

    def initTray(self):
        self.set_from_file(self.setting['iconPath'])
        self.connect('popup-menu', self.onRightClick)
        self.connect('activate', self.onLeftClick)

    def onRightClick(self, icon, event_button, event_time):
        self.rightClick = TrayRightClickMenu(self.setting, event_button, event_time)

    def onLeftClick(self, icon):
        if self.setting['createEditAp'] == None:
            self.setting['createEditAp'] = CreateEditAp(self.setting)
            self.setting['createEditAp'].show()