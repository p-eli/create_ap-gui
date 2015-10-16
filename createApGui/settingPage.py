#!/usr/bin/python3
__author__ = 'Jakub Pelikan'
import gi
gi.require_version('Gtk', '3.0')
from gi.repository import Gtk
from createApGui. guiComponent import GuiComponent

class SettingPage(Gtk.Table):
    def __init__(self, parent, setting):
        Gtk.Table.__init__(self,10,3, True)
        self.parent = parent
        self.setting = setting
        self._ = self.setting['language'].gettext
        self.set_border_width(20)
        self.set_row_spacings(10)
        self.set_col_spacings(10)
        self.init()

    def init(self):
        #language label
        GuiComponent.createLabel(self._('Language'),[0,1,0,1],self, aligment='right')
        #init language comboBox
        self.createLanguageListStore()
        self.languageComboBox = Gtk.ComboBox.new_with_model(self.languageListStore)
        defaultPosition = self.setting['language'].getLanguageList().index(self.setting['userSetting'].language['name'])
        GuiComponent.createComboBox(self.languageComboBox, [1,3,0,1],self , defaultPosition)
        #Automatic check update
        GuiComponent.createLabel(self._('Automatic update'),[0,1,1,2],self, aligment='right')
        GuiComponent.createSwitchButton([2,3,1,2], self, self.automaticCheckUpdate, self.setting['userSetting'].version['autoCheck'])
        #save
        GuiComponent.createButton(self._('Save'),[2,3,9,10], self, self.saveSetting)


    def saveSetting(self, button=None):
        self.setting['userSetting'].language['name'] = GuiComponent.getComboBoxSelect(self.languageComboBox)
        self.setting['language'].update(self.setting)
        self.setting['userSetting'].save()

    def createLanguageListStore(self):
        self.languageListStore = Gtk.ListStore(str)
        for item in self.setting['language'].getLanguageList():
            self.languageListStore.append([item])

    def automaticCheckUpdate(self, switch, gparam):
        if switch.get_active():
            self.setting['userSetting'].version['autoCheck'] = True
        else:
            self.setting['userSetting'].version['autoCheck'] = False