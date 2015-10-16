from gi.repository import Gtk


class GuiComponent:
    @staticmethod
    def createButton(text, pos, table, action, button=None):
        if text != None:
            if button == None:
                button = Gtk.Button.new_with_mnemonic(text)
            else:
                button.set_label(text)
        button.connect("clicked", action)
        table.attach(button,pos[0],pos[1],pos[2],pos[3])

    @staticmethod
    def createLabel(text, pos, table, interfaceLabel=None, aligment='right'):
        if interfaceLabel == None:
            interfaceLabel = Gtk.Label(text)
        else:
            try:
                interfaceLabel.set_text(text)
            except:
                interfaceLabel.set_text('None')
        if aligment == 'right':
            interfaceLabel.set_alignment(1, 0.5)
        elif aligment == 'left':
            interfaceLabel.set_alignment(0, 0.5)
        elif aligment == 'center':
            interfaceLabel.set_alignment(0.5, 0.5)
        table.attach(interfaceLabel,pos[0],pos[1],pos[2],pos[3])

    @staticmethod
    def createComboBox(name, pos, table, default=None):
        renderer_text = Gtk.CellRendererText()
        name.pack_start(renderer_text, True)
        name.add_attribute(renderer_text, "text", 0)
        if default != None:
            name.set_active(default)
        table.attach(name ,pos[0],pos[1],pos[2],pos[3])

    @staticmethod
    def createEntry(name, pos, table, text="", visible=True):
        name.set_text(text)
        name.set_visibility(visible)
        table.attach(name ,pos[0],pos[1],pos[2],pos[3])

    @staticmethod
    def createCheckButton(name, pos, table, action, check=True):
        name.set_active(check)
        name.connect("clicked", action)
        table.attach(name ,pos[0],pos[1],pos[2],pos[3])

    @staticmethod
    def createSwitchButton(pos, table, function,active=True):
        switch = Gtk.Switch()
        switch.connect("notify::active", function)
        switch.set_active(active)
        table.attach(switch ,pos[0],pos[1],pos[2],pos[3])

    @staticmethod
    def getComboBoxSelect(comboBox):
        tree_iter = comboBox.get_active_iter()
        if tree_iter != None:
            model = comboBox.get_model()
            return (model[tree_iter][0])
        return None

    @staticmethod
    def sendErrorDialog(parent ,primaryText, secondaryText):
        dialog = Gtk.MessageDialog(parent, 0, Gtk.MessageType.ERROR, Gtk.ButtonsType.CANCEL, primaryText)
        dialog.format_secondary_text(secondaryText)
        dialog.run()
        dialog.destroy()

    @staticmethod
    def createTextViewColumn(treeview, names):
        renderer = Gtk.CellRendererText()
        id = 0
        for name in names:
            column_name = Gtk.TreeViewColumn(name, renderer, text=id)
            column_name.set_sort_column_id(id)
            treeview.append_column(column_name)
            id=id+1