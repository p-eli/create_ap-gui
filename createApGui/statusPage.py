#!/usr/bin/python3
__author__ = 'Jakub Pelikan'
import gi
gi.require_version('Gtk', '3.0')
from gi.repository import Gtk, Pango
from createApGui. guiComponent import GuiComponent


class StatusPage(Gtk.Table):
    def __init__(self, parent, setting):
        Gtk.Table.__init__(self,10,3, True)
        self.parent = parent
        self.setting = setting
        self._ = self.setting['language'].gettext
        self.set_border_width(10)
        self.set_row_spacings(5)
        self.set_col_spacings(20)
        self.init()

    def init(self):
        #status label
        self.statusTitleLabel = Gtk.Label(self.setting['runningAp'].status['text'])
        pangoFont = Pango.FontDescription("Sans 40")
        self.statusTitleLabel.modify_font(pangoFont)
        self.attach(self.statusTitleLabel, 0,3,0,3)
        #information about conection
        #Name
        GuiComponent.createLabel(self._('AP name'),[0,1,3,4], self, aligment='right')
        self.statusNameAp = Gtk.Label()
        GuiComponent.createLabel('None', [1,3,3,4], self, self.statusNameAp, aligment='left')
        #wifi interface 1
        GuiComponent.createLabel(self._('Wifi interface'),[0,1,4,5], self, aligment='right')
        self.statusInterface1 = Gtk.Label()
        GuiComponent.createLabel('None', [1,3,4,5], self, self.statusInterface1, aligment='left')
        #wifi interface 2
        GuiComponent.createLabel(self._('Interface with Internet'),[0,1,5,6], self, aligment='right')
        self.statusInterface2 = Gtk.Label()
        GuiComponent.createLabel('None', [1,3,5,6], self, self.statusInterface2, aligment='left')
        #Receiving
        GuiComponent.createLabel(self._('Receiving'),[0,1,6,7], self, aligment='right')
        self.statusReciving = Gtk.Label()
        GuiComponent.createLabel(self._('None'), [1,2,6,7], self, self.statusReciving, aligment='left')
        #Total Received
        GuiComponent.createLabel(self._('Total Received'),[0,1,7,8],self, aligment='right')
        self.statusTotalReciving = Gtk.Label()
        GuiComponent.createLabel(self._('None'), [1,2,7,8],self, self.statusTotalReciving, aligment='left')
        #Sending
        GuiComponent.createLabel(self._('Sending'),[1,2,6,7],self, aligment='right')
        self.statusSending = Gtk.Label()
        GuiComponent.createLabel(self._('None'), [2,3,6,7],self, self.statusSending, aligment='left')
        #Total Sent
        GuiComponent.createLabel(self._('Total Sent'),[1,2,7,8],self, aligment='right')
        self.statusTotalSending = Gtk.Label()
        GuiComponent.createLabel(self._('None'), [2,3,7,8], self, self.statusTotalSending, aligment='left')
        #connect / disconect button
        self.errorButton = Gtk.Button()
        GuiComponent.createButton(self._('Error details'),[2,3,9,10],self,self.errorButtonAction,self.errorButton)
        #connect / disconect button
        self.connectButton = Gtk.Button()
        GuiComponent.createButton(self._('Connect'),[2,3,9,10],self,self.connectButtonAction,self.connectButton)
        #connect / disconect button
        self.disconnectButton = Gtk.Button()
        GuiComponent.createButton(self._('Disconnect'),[2,3,9,10],self,self.disconnectButtonAction,self.disconnectButton)

    def errorButtonAction(self, button=None):
        GuiComponent.sendErrorDialog(self.parent, self.setting['runningAp'].errorMsg['title'], self.setting['runningAp'].errorMsg['text'])

    def connectButtonAction(self,button=None):
        self.parent.changeCurrentPage(+1)

    def disconnectButtonAction(self,button=None):
        self.setting['runningAp'].stopAp()

    def updateStatusPage(self, signal=None):
            self.statusTitleLabel.set_text(self.setting['runningAp'].status['text'])
            self.statusNameAp.set_text(self.setting['runningAp'].activeAp['name'])
            self.statusInterface1.set_text(self.setting['runningAp'].activeAp['interface1'])
            self.statusInterface2.set_text(self.setting['runningAp'].activeAp['interface2'])
            self.statusReciving.set_text(self.setting['runningAp'].receiving)
            self.statusTotalReciving.set_text(self.setting['runningAp'].totalReceived)
            self.statusSending.set_text(self.setting['runningAp'].sending)
            self.statusTotalSending.set_text(self.setting['runningAp'].totalSent)
            if self.setting['runningAp'].status['active']:
                self.disconnectButton.show()
                self.connectButton.hide()
                self.errorButton.hide()
            elif self.setting['runningAp'].errorMsg['newMsg']:
                self.disconnectButton.hide()
                self.connectButton.hide()
                self.errorButton.show()
            else:
                self.disconnectButton.hide()
                self.connectButton.show()
                self.errorButton.hide()