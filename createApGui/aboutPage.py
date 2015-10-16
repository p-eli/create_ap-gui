#!/usr/bin/python3
__author__ = 'Jakub Pelikan'
import gi
gi.require_version('Gtk', '3.0')
from gi.repository import Gtk, Pango
from createApGui import __version__
from createApGui. guiComponent import GuiComponent

class AboutPage(Gtk.Table):
    def __init__(self,parent, setting):
        Gtk.Table.__init__(self,10,3, False)
        self.parent = parent
        self.setting = setting
        self._ = self.setting['language'].gettext
        self.set_border_width(10)
        self.set_col_spacings(10)
        self.init()

    def init(self):
        #application name
        aboutTitleLabel = Gtk.Label(self._('Create AP Gui'))
        pangoFont = Pango.FontDescription("Sans 40")
        aboutTitleLabel.modify_font(pangoFont)
        self.attach(aboutTitleLabel, 0,3,0,2)
        #Description
        GuiComponent.createLabel(self._('\t Gui application for easy creating access points.\n Application allows save configuration for quickly create AP.'),[0,3,2,3],self, aligment='center')
        #version
        GuiComponent.createLabel(self._('Version:'),[0,1,3,4],self, aligment='right')
        GuiComponent.createLabel(__version__,[1,3,3,4],self, aligment='left')
        #author
        GuiComponent.createLabel(self._('Author:'),[0,1,4,5],self, aligment='right')
        GuiComponent.createLabel(self._('Jakub Pelikan'),[1,3,4,5],self, aligment='left')
        #nick
        GuiComponent.createLabel(self._('Nick:'),[0,1,5,6],self, aligment='right')
        GuiComponent.createLabel(self._('P-eli'),[1,3,5,6],self, aligment='left')
        #email
        GuiComponent.createLabel(self._('Email:'),[0,1,6,7],self, aligment='right')
        GuiComponent.createLabel(self._('jakub.pelikan@gmail.com'),[1,3,6,7],self, aligment='left')
        #Website
        GuiComponent.createLabel(self._('Website:'),[0,1,7,8],self, aligment='right')
        website = Gtk.Label()
        GuiComponent.createLabel('',[1,3,7,8],self,website, aligment='left')
        website.set_markup("<a href=\"http://github.com/p-eli/create_ap-gui\" " "title=\"Click to open website\">http://github.com/p-eli/create_ap-gui</a>")
        GuiComponent.createLabel('',[0,1,8,9],self, aligment='right')
        GuiComponent.createLabel('',[0,1,9,10],self, aligment='right')



