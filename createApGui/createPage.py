#!/usr/bin/python3
__author__ = 'Jakub Pelikan'
import gi
gi.require_version('Gtk', '3.0')
from gi.repository import Gtk, GObject
from createApGui. guiComponent import GuiComponent
from createApGui.terminalInterface import TerminalInterface
import re

class CreatePage(Gtk.Table):
    def __init__(self, parent, setting):
        Gtk.Table.__init__(self,10,3, True)
        self.parent = parent
        self.setting = setting
        self._ = self.setting['language'].gettext
        self.set_border_width(10)
        self.set_row_spacings(10)
        self.set_col_spacings(10)
        self.init()

    def init(self):
        self.refreshingInterface = False
        self.interfaceListSignal = GObject.GObject()
        self.interfaceListSignal.connect('interfaceListMsg', self.readInterfaceList)
        self.initInterfaceList()
        #create New Form
        #acces point name
        GuiComponent.createLabel(self._('AP name'),[0,1,0,1], self, aligment='right')
        #access point name set text
        self.apName = Gtk.Entry()
        GuiComponent.createEntry(self.apName, [1,3,0,1],self, "")
        #acces point password
        GuiComponent.createLabel(self._('Password'),[0,1,1,2],self, aligment='right')
        #access point password set text
        self.apPassword = Gtk.Entry()
        GuiComponent.createEntry(self.apPassword, [1,3,1,2],self,"",False)
        #Show password
        self.showPassword = Gtk.CheckButton(self._("Show password"),self)
        GuiComponent.createCheckButton(self.showPassword, [1,3,2,3],self , self.showHidePasswd, True)
        #wifi interface label
        GuiComponent.createLabel(self._('Wifi interface'),[0,1,3,4],self, aligment='right')
        #wifi interface Combobox
        self.interface1ComboBox = Gtk.ComboBox.new_with_model(self.interfaceListStore)
        GuiComponent.createComboBox(self.interface1ComboBox, [1,3,3,4],self , None)
        #interface with internet Label
        GuiComponent.createLabel(self._('Interface with Internet'),[0,1,4,5],self, aligment='right')
        #interface with internet Combobox
        self.interface2ComboBox = Gtk.ComboBox.new_with_model(self.interfaceListStore)
        GuiComponent.createComboBox( self.interface2ComboBox, [1,3,4,5], self, None)
        #refresh interface list button
        GuiComponent.createButton(self._('Refresh'),[2,3,5,6], self, self.refreshInterfaceList)
        #Save and Create AP
        GuiComponent.createButton(self._("Only Create"), [1,2,9,10], self, self.onlyCreateAction)
        GuiComponent.createButton(self._("Save and Create"), [2,3,9,10], self, self.saveCreateAction)

    def refreshInterfaceList(self, button):
        self.initInterfaceList()
        self.interface1ComboBox.set_model(self.interfaceListStore)
        self.interface2ComboBox.set_model(self.interfaceListStore)

    def saveCreateAction(self, button=None):
        try:
            newApConfiguration = self.elaborationNewApForm()
            self.setting['userSetting'].addAp(newApConfiguration[0],newApConfiguration[1],newApConfiguration[2],newApConfiguration[3])
            self.parent.editPage.addToStore(newApConfiguration)
            self.createAP(createAp=newApConfiguration)
        except ValueError:
            pass

    def onlyCreateAction(self, button=None):
        try:
            newApConfiguration = self.elaborationNewApForm()
            self.createAP(createAp=newApConfiguration)
        except ValueError:
            pass

    def elaborationNewApForm(self):
        if self.apName.get_text() != "":
            if (len(self.apPassword.get_text()) == 0) or len(self.apPassword.get_text()) >= 8:
                newApConfiguration = [self.apName.get_text(), self.apPassword.get_text(), GuiComponent.getComboBoxSelect(self.interface1ComboBox),GuiComponent.getComboBoxSelect(self.interface2ComboBox)]
                self.apName.set_text("")
                self.apPassword.set_text("")
                return newApConfiguration
            else:
                GuiComponent.sendErrorDialog(self.parent, self._('Invalid password length'), self._('expected length 8..63'))
                raise ValueError
        else:
            GuiComponent.sendErrorDialog(self.parent, self._('Ap name is Empty'), self._('Please fill it.'))
            raise ValueError

    def showHidePasswd(self, stat):
        self.apPassword.set_visibility(not stat.get_active())

    def initInterfaceList(self):
        if not self.refreshingInterface:
            self.refreshingInterface = True
            self.interfaceListStore = Gtk.ListStore(str)
            self.interface = TerminalInterface(self.interfaceListSignal, "interfaceListMsg")
            self.interface.command = ['ifconfig']
            self.interface.start()

    def readInterfaceList(self, signal):
        output = self.interface.read()
        if self.interface.is_alive():
            self.interface.stop()
        interfacesList = []
        output = output.split('\n')
        for x in output:
            stra = re.search(r'(^|\n)[^(:| )]*', x).group()
            if stra != '':
                interfacesList.append(stra)
        for interfaceItem in interfacesList:
            self.interfaceListStore.append([interfaceItem])
        self.refreshingInterface = False

    def createAP(self, createAp=None):
        if not self.setting['runningAp'].status['active']:
            self.setting['runningAp'].activeAp = createAp
            self.setting['runningAp'].runAp()
        else:
            GuiComponent.sendErrorDialog(self.parrent, self._('AP is running'), self._('Before start new one, turn off running AP.'))
        self.parent.showFirstPage()