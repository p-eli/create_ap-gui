#!/usr/bin/python3
__author__ = 'Jakub Pelikan'
from gi.repository import Gtk, Pango
from createApGui.terminalInterface import TerminalInterface
import re
class CreateEditAp(Gtk.Window):
    def __init__(self, setting):
        Gtk.Window.__init__(self, title='Create AP')
        self.setting = setting
        self._ = self.setting['language'].gettext
        self.initWindow()
        self.setting['runningAp'].updatingPage['statusWindow'] = self.updateStatusPage
        self.set_default_icon_from_file(self.setting['iconPath'])

    def show(self, page=None):
        self.show_all()
        if page != None:
            Gtk.Notebook.do_change_current_page(self.notebook,page-self.notebook.get_current_page())

    def initWindow(self):
        self.connect("destroy", self.on_destroy)
        self.set_border_width(3)
        self.notebook = Gtk.Notebook()
        self.add(self.notebook)
        self.initStatusPage()
        self.initInterfaceList()
        self.initEditPage()
        self.initCreatePage()
        self.initSettingPage()
        self.initAboutPage()

    def initStatusPage(self):
        table = Gtk.Table(10,3, True)
        table.set_border_width(10)
        table.set_row_spacings(5)
        table.set_col_spacings(20)
        #status label
        self.statusTitleLabel = Gtk.Label(self.setting['runningAp'].status)
        pangoFont = Pango.FontDescription("Sans 40")
        self.statusTitleLabel.modify_font(pangoFont)
        table.attach(self.statusTitleLabel, 0,3,0,3)
        #information about conection
        #Name
        self.createLabel(self._('AP name'),[0,1,3,4], table,aligmentRight=False)
        self.statusNameAp = Gtk.Label()
        self.createLabel('None', [1,3,3,4], table, self.statusNameAp, False)
        #wifi interface 1
        self.createLabel(self._('Wifi interface'),[0,1,4,5], table,aligmentRight=False)
        self.statusInterface1 = Gtk.Label()
        self.createLabel('None', [1,3,4,5], table, self.statusInterface1, False)
        #wifi interface 2
        self.createLabel(self._('Interface with Internet'),[0,1,5,6], table,aligmentRight=False)
        self.statusInterface2 = Gtk.Label()
        self.createLabel('None', [1,3,5,6], table, self.statusInterface2, False)
        #Receiving
        self.createLabel(self._('Receiving'),[0,1,6,7], table,aligmentRight=False)
        self.statusReciving = Gtk.Label()
        self.createLabel(self._('None'), [1,2,6,7], table, self.statusReciving, False)
        #Total Received
        self.createLabel(self._('Total Received'),[0,1,7,8],table,aligmentRight=False)
        self.statusTotalReciving = Gtk.Label()
        self.createLabel(self._('None'), [1,2,7,8],table, self.statusTotalReciving, False)
        #Sending
        self.createLabel(self._('Sending'),[1,2,6,7],table)
        self.statusSending = Gtk.Label()
        self.createLabel(self._('None'), [2,3,6,7],table, self.statusSending, False)
        #Total Sent
        self.createLabel(self._('Total Sent'),[1,2,7,8],table)
        self.statusTotalSending = Gtk.Label()
        self.createLabel(self._('None'), [2,3,7,8], table, self.statusTotalSending, False)
        #connect / disconect button
        self.connectDisconectButton = Gtk.Button()
        self.createButton(self._('Connect'),[2,3,9,10],table,self.connectDisconnect,self.connectDisconectButton )
        self.updateStatusPage()
        self.notebook.append_page(table, Gtk.Label(self._('Running AP')))

    def connectDisconnect(self, button=None):
        if self.setting['runningAp'].errorMsg['newMsg']:
            self.sendErrorDialog(self.setting['runningAp'].errorMsg['title'], self.setting['runningAp'].errorMsg['text'])
        else:
            if self.setting['runningAp'].status['active']:
                self.setting['runningAp'].stopAp()
            else:
                Gtk.Notebook.do_change_current_page(self.notebook,+1)


    def initCreatePage(self):
        table = Gtk.Table(10,3, True)
        table.set_border_width(10)
        table.set_row_spacings(10)
        table.set_col_spacings(10)
        #create New Form
        #acces point name
        self.createLabel(self._('AP name'),[0,1,0,1], table)
        #access point name set text
        self.apName = Gtk.Entry()
        self.createEntry(self.apName, [1,3,0,1],table, "")
        #acces point password
        self.createLabel(self._('Password'),[0,1,1,2],table)
        #access point password set text
        self.apPassword = Gtk.Entry()
        self.createEntry(self.apPassword, [1,3,1,2],table,"",False)
        #Show password
        self.showPassword = Gtk.CheckButton(self._("Show password"),table)
        self.createCheckButton(self.showPassword, [1,3,2,3],table , self.showHidePasswd, True)
        #wifi interface label
        self.createLabel(self._('Wifi interface'),[0,1,3,4],table)
        #wifi interface Combobox
        self.interface1ComboBox = Gtk.ComboBox.new_with_model(self.interfaceListStore)
        self.createComboBox(self.interface1ComboBox, [1,3,3,4],table , None)
        #interface with internet Label
        self.createLabel(self._('Interface with Internet'),[0,1,4,5],table)
        #interface with internet Combobox
        self.interface2ComboBox = Gtk.ComboBox.new_with_model(self.interfaceListStore)
        self.createComboBox( self.interface2ComboBox, [1,3,4,5], table, None)
        #refresh interface list button
        self.createButton(self._('Refresh'),[2,3,5,6], table, self.refreshInterfaceList)
        #Save and Create AP
        self.createButton(self._("Only Create"), [1,2,9,10], table, self.onlyCreateAction)
        self.createButton(self._("Save and Create"), [2,3,9,10], table, self.saveCreateAction)
        self.notebook.append_page(table, Gtk.Label(self._('New AP')))

    def initEditPage(self):
        table = Gtk.Table(10,3,True)
        table.set_border_width(10)
        table.set_row_spacings(10)
        table.set_col_spacings(10)
        self.store = Gtk.ListStore(str, str, str)
        self.setting['userSetting'].getApStore(self.store)
        self.treeview = Gtk.TreeView(model=self.store)
        self.createTextViewColumn([self._('AP name'),self._('Interface1'),self._('Interface2')])
        scrolled_window = Gtk.ScrolledWindow()
        scrolled_window.set_policy(
            Gtk.PolicyType.NEVER, Gtk.PolicyType.AUTOMATIC)
        scrolled_window.add(self.treeview)
        #delete AP buton
        self.createButton(self._('Delete'),[1,2,9,10], table, self.deleteAP)
        #create AP button
        self.createButton(self._('Create'),[2,3,9,10], table, self.createAP)
        table.attach(scrolled_window, 0, 3, 0, 9)
        self.notebook.append_page(table, Gtk.Label(self._('Create AP')))

    def initSettingPage(self):
        self.settingPage = Gtk.Box()
        self.settingPage.set_border_width(10)
        self.settingPage.add(Gtk.Label('Setting'))
        self.notebook.append_page(self.settingPage, Gtk.Label(self._('Setting')))

    def initAboutPage(self):
        self.aboutPage = Gtk.Box()
        self.aboutPage.set_border_width(10)
        self.aboutPage.add(Gtk.Label(self._('AboutAs')))
        self.notebook.append_page(self.aboutPage, Gtk.Label(self._('About')))

    def createButton(self, text, pos, table, action, button=None):
        if button == None:
            button = Gtk.Button.new_with_mnemonic(text)
        else:
            button.set_label(text)
        button.connect("clicked", action)
        table.attach(button,pos[0],pos[1],pos[2],pos[3])

    def createLabel(self, text, pos, table, interfaceLabel=None, aligmentRight=True):
        if interfaceLabel == None:
            interfaceLabel = Gtk.Label(text)
        else:
            try:
                interfaceLabel.set_text(text)
            except:
                interfaceLabel.set_text('None')
        if aligmentRight:
            interfaceLabel.set_alignment(1, 0)
        else:
            interfaceLabel.set_alignment(0, 0)
        table.attach(interfaceLabel,pos[0],pos[1],pos[2],pos[3])

    def createComboBox(self, name, pos, table, default=None):
        renderer_text = Gtk.CellRendererText()
        name.pack_start(renderer_text, True)
        name.add_attribute(renderer_text, "text", 0)
        table.attach(name ,pos[0],pos[1],pos[2],pos[3])

    def createEntry(self, name, pos, table, text="", visible=True):
        name.set_text(text)
        name.set_visibility(visible)
        table.attach(name ,pos[0],pos[1],pos[2],pos[3])

    def createCheckButton(self, name, pos, table, action, check=True):
        name.set_active(check)
        name.connect("clicked", action)
        table.attach(name ,pos[0],pos[1],pos[2],pos[3])

    def createTextViewColumn(self, names):
        renderer = Gtk.CellRendererText()
        id = 0
        for name in names:
            column_name = Gtk.TreeViewColumn(name, renderer, text=id)
            column_name.set_sort_column_id(id)
            self.treeview.append_column(column_name)
            id=id+1

    def initInterfaceList(self):
        self.interfaceListStore = Gtk.ListStore(str)
        self.interface = TerminalInterface(self.readInterfaceList)
        self.interface.command = ['ifconfig']
        self.interface.start()

    def readInterfaceList(self):
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


    def refreshInterfaceList(self, button):
        self.initInterfaceList()
        self.interface1ComboBox.set_model(self.interfaceListStore)
        self.interface2ComboBox.set_model(self.interfaceListStore)

    def getComboBoxSelect(self, comboBox):
        tree_iter = comboBox.get_active_iter()
        if tree_iter != None:
            model = comboBox.get_model()
            return (model[tree_iter][0])
        return None

    def createAP(self, button=None, createAp=None):
        if self.setting['runningAp'].errorMsg['newMsg']:
            self.setting['runningAp'].stopAp()
            self.setting['runningAp'].createNew()
        if not self.setting['runningAp'].status['active']:
            if createAp == None:
                selection = self.treeview.get_selection()
                model, paths = selection.get_selected_rows()
                for path in paths:
                    iter = model.get_iter(path)
                    createAp = self.setting['userSetting'].searchAp(model[iter][0],model[iter][1],model[iter][2])
            if createAp != None:
                self.setting['runningAp'].activeAp = createAp
                self.setting['runningAp'].runAp()
        else:
            self.sendErrorDialog(self._('AP is running'), self._('Before start new one, turn off running AP.'))
        Gtk.Notebook.do_change_current_page(self.notebook,-self.notebook.get_current_page())

    def updateStatusPage(self):
        self.statusTitleLabel.set_text(self.setting['runningAp'].status['text'])
        self.statusNameAp.set_text(self.setting['runningAp'].activeAp['name'])
        self.statusInterface1.set_text(self.setting['runningAp'].activeAp['interface1'])
        self.statusInterface2.set_text(self.setting['runningAp'].activeAp['interface2'])
        self.statusReciving.set_text('None')
        self.statusTotalReciving.set_text('None')
        self.statusSending.set_text('None')
        self.statusTotalSending.set_text('None')
        self.connectDisconectButton.set_label(self.setting['runningAp'].status['button'])

    def saveCreateAction(self, button=None):
        try:
            newApConfiguration = self.elaborationNewApForm()
            self.setting['userSetting'].addAp(newApConfiguration[0],newApConfiguration[1],newApConfiguration[2],newApConfiguration[3])
            self.store.append([newApConfiguration[0],newApConfiguration[2],newApConfiguration[3]])
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
                newApConfiguration = [self.apName.get_text(), self.apPassword.get_text(), self.getComboBoxSelect(self.interface1ComboBox),self.getComboBoxSelect(self.interface2ComboBox)]
                self.apName.set_text("")
                self.apPassword.set_text("")
                return newApConfiguration
            else:
                self.sendErrorDialog(self._('Invalid password length'), self._('expected length 8..63'))
                raise ValueError
        else:
            self.sendErrorDialog(self._('Ap name is Empty'), self._('Please fill it.'))
            raise ValueError

    def sendErrorDialog(self, primaryText, secondaryText):
        dialog = Gtk.MessageDialog(self, 0, Gtk.MessageType.ERROR, Gtk.ButtonsType.CANCEL, primaryText)
        dialog.format_secondary_text(secondaryText)
        dialog.run()
        dialog.destroy()

    def deleteAP(self, button):
        selection = self.treeview.get_selection()
        model, paths = selection.get_selected_rows()
        for path in paths:
            iter = model.get_iter(path)
            self.setting['userSetting'].removeAp(model[iter][0],model[iter][1],model[iter][2])
            model.remove(iter)

    def showHidePasswd(self, stat):
        self.apPassword.set_visibility(not stat.get_active())

    def on_destroy(self, widget):
        self.setting['runningAp'].updatingPage['statusWindow'] = None
        self.setting['createEditAp'] = None
        self.destroy()