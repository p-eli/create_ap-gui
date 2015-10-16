#!/usr/bin/python3
__author__ = 'Jakub Pelikan'
import gi
gi.require_version('Gtk', '3.0')
from gi.repository import Gtk, GObject
from createApGui.statusPage import StatusPage
from createApGui.editPage import EditPage
from createApGui.createPage import CreatePage
from createApGui.settingPage import SettingPage
from createApGui.aboutPage import AboutPage


class MainWindow(Gtk.Window):

    GObject.signal_new("interfaceListMsg", GObject.GObject, GObject.SIGNAL_RUN_FIRST, GObject.TYPE_NONE, ())
    def __init__(self, setting):
        Gtk.Window.__init__(self, title='Create AP')
        self.setting = setting
        self._ = self.setting['language'].gettext
        self.initWindow()

        self.setting['runningAp'].registerPage(self.updateStatusPage)
        self.set_default_icon_from_file(self.setting['iconPath'])

    def show(self, page=None):
        self.show_all()
        self.updateStatusPage()
        if page != None:
            Gtk.Notebook.do_change_current_page(self.notebook,page-self.notebook.get_current_page())

    def initWindow(self):
        self.connect("destroy", self.on_destroy)
        self.set_border_width(3)
        self.notebook = Gtk.Notebook()
        self.add(self.notebook)

        self.statusPage = StatusPage(self, self.setting)
        self.notebook.append_page(self.statusPage, Gtk.Label(self._('Running AP')))

        self.editPage = EditPage(self, self.setting)
        self.notebook.append_page(self.editPage, Gtk.Label(self._('New AP')))

        self.createPage = CreatePage(self, self.setting)
        self.notebook.append_page(self.createPage, Gtk.Label(self._('Create AP')))

        self.settingPage = SettingPage(self, self.setting)
        self.notebook.append_page(self.settingPage, Gtk.Label(self._('Setting')))

        self.aboutPage = AboutPage(self, self.setting)
        self.notebook.append_page(self.aboutPage, Gtk.Label(self._('About')))

    def updateStatusPage(self, signal=None):
        self.statusPage.updateStatusPage()

    def on_destroy(self, widget):
        self.setting['runningAp'].unregisterPage()
        self.setting['createEditAp'] = None
        self.destroy()

    def changeCurrentPage(self, page):
        Gtk.Notebook.do_change_current_page(self.notebook,page)

    def showFirstPage(self):
        Gtk.Notebook.do_change_current_page(self.notebook,-self.notebook.get_current_page())



