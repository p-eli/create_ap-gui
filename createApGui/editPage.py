#!/usr/bin/python3
__author__ = 'Jakub Pelikan'
import gi
gi.require_version('Gtk', '3.0')
from gi.repository import Gtk, GObject
from createApGui. guiComponent import GuiComponent

class EditPage(Gtk.Table):
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
        self.store = Gtk.ListStore(GObject.TYPE_STRING, GObject.TYPE_STRING, GObject.TYPE_STRING)
        self.setting['userSetting'].getApStore(self.store)
        self.treeview = Gtk.TreeView(model=self.store)
        GuiComponent.createTextViewColumn(self.treeview, [self._('AP name'),self._('Interface1'),self._('Interface2')])
        scrolled_window = Gtk.ScrolledWindow()
        scrolled_window.set_policy(
            Gtk.PolicyType.NEVER, Gtk.PolicyType.AUTOMATIC)
        scrolled_window.add(self.treeview)
        #delete AP buton
        GuiComponent.createButton(self._('Delete'),[1,2,9,10], self, self.deleteAP)
        #create AP button
        GuiComponent.createButton(self._('Create'),[2,3,9,10], self, self.createAP)
        self.attach(scrolled_window, 0, 3, 0, 9)

    def addToStore(self, newItem):
        self.store.append([newItem[0],newItem[2],newItem[3]])

    def createAP(self, button=None):
        if not self.setting['runningAp'].status['active']:
                createAp = None
                selection = self.treeview.get_selection()
                model, paths = selection.get_selected_rows()
                for path in paths:
                    iter = model.get_iter(path)
                    createAp = self.setting['userSetting'].searchAp(model[iter][0],model[iter][1],model[iter][2])
                if createAp != None:
                    self.setting['runningAp'].activeAp = createAp
                    self.setting['runningAp'].runAp()
        else:
            GuiComponent.sendErrorDialog(self.parent, self._('AP is running'), self._('Before start new one, turn off running AP.'))
        self.parent.showFirstPage()


    def deleteAP(self, button):
        selection = self.treeview.get_selection()
        model, paths = selection.get_selected_rows()
        for path in paths:
            iter = model.get_iter(path)
            self.setting['userSetting'].removeAp(model[iter][0],model[iter][1],model[iter][2])
            model.remove(iter)