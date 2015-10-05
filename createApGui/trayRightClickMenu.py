#!/usr/bin/python3
__author__ = 'Jakub Pelikan'
from gi.repository import Gtk
from createApGui.createEditAp import CreateEditAp


class TrayRightClickMenu(Gtk.Menu):
    def __init__(self, setting, event_button, event_time):
        Gtk.Menu.__init__(self)
        self.setting = setting
        self._ = self.setting['language'].gettext
        self.initMenu()
        self.popup(None, None,None, None, event_button, event_time)
        self.show()

    def initMenu(self):
        #AP status
        self.apStatusItem = Gtk.MenuItem(self.setting['runningAp'].status['text'])
        self.append(self.apStatusItem)
        self.apStatusItem.set_sensitive(False)
        #Disconnect AP
        if self.setting['runningAp'].status['active'] or self.setting['runningAp'].errorMsg['newMsg']:
            self.disconnectItem = Gtk.MenuItem(self.setting['runningAp'].status['button'])
            self.append(self.disconnectItem)
            self.disconnectItem.connect('activate',self.disconnectAp)
        self.addSeparator()
        #Show AP Status
        self.createMenuItem(self._('Show AP Status'), self.showApStatusPage)
        #Run existing configuration
        self.initCreateApSubMenu()
        #Create new AP
        self.createMenuItem(self._('Setup New AP'), self.showCreateNewApPage)
        #About
        self.addSeparator()
        self.createMenuItem(self._('About'), self.showAboutPage)
        #Setting
        self.createMenuItem(self._('Setting'), self.showSettingPage)
        #Exit
        self.createMenuItem(self._('Exit'), self.exitAction)
        self.show_all()

    def initCreateApSubMenu(self):
        apSubMenu = Gtk.Menu()
        createAp = Gtk.MenuItem(self._('Create AP'))
        createAp.set_submenu(apSubMenu)
        self.append(createAp)
        self.initApList(apSubMenu)

    def initApList(self, menu):
        apList = []
        self.setting['userSetting'].getApStore(apList)
        for item in apList:
            self.createMenuItem(item[0], self.createAp, menu)

    def createAp(self, button):
        if self.setting['runningAp'].errorMsg['newMsg'] or self.setting['runningAp'].status['active']:
            self.setting['runningAp'].stopAp()
        if not self.setting['runningAp'].status['active']:
            self.setting['runningAp'].activeAp = self.setting['userSetting'].searchAp(button.get_label())
            self.setting['runningAp'].runAp()

    def showCreateNewApPage(self, parent=None):
        self.newAp(2)

    def showApStatusPage(self, parent=None):
        self.newAp(0)

    def showAboutPage(self, parent=None):
        self.newAp(4)

    def showSettingPage(self, parent=None):
        self.newAp(3)

    def newAp(self,page):
        if self.setting['createEditAp'] == None:
            self.setting['createEditAp'] = CreateEditAp(self.setting)
        self.setting['createEditAp'].show(page)

    def disconnectAp(self, button):
        if self.setting['runningAp'].errorMsg['newMsg']:
            self.showApStatusPage(self)
        else:
            self.setting['runningAp'].stopAp()

    def createMenuItem(self, itemText, action=None, menu=None, newItem=None):
        if newItem == None:
            newItem = Gtk.MenuItem(itemText)
        if menu == None:
            self.append(newItem)
        else:
            menu.append(newItem)
        if action != None:
            newItem.connect('activate',action)

    def addSeparator(self):
        separator = Gtk.SeparatorMenuItem()
        self.append(separator)

    def exitAction(self, button=None):
        if self.setting['runningAp'].status['active']:
            self.setting['runningAp'].stopAp()
        Gtk.main_quit(button)
        exit()