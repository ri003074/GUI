import configparser
import os
import sys

import wx
import wx.adv


def resource_path(relative_path):
    if hasattr(sys, "_MEIPASS"):
        return os.path.join(sys._MEIPASS, relative_path)
    return os.path.join(os.path.abspath("."), relative_path)


class GuiLibWx(wx.Frame):
    def __init__(self, parent, title, height, width, pos, layout="static"):
        super(GuiLibWx, self).__init__(
            parent,
            title=title,
            size=(width, height),
            pos=pos,
            style=wx.MINIMIZE_BOX
            | wx.SYSTEM_MENU
            | wx.CAPTION
            | wx.CLOSE_BOX
            | wx.CLIP_CHILDREN,
        )
        self.layout_items = []
        self.button = {}
        self.static_text = {}
        self.text_ctrl = {}
        self.radio_box = {}

        self.text_data = {}
        self.replace_data = {}
        self.selected_radio_buttons = {}

        # default setup
        self.radio_box_height_per_1_box = 33
        self.layout = layout
        self.gui_height = height
        self.gui_width = width
        self.old_style = None
        self.stay_on_top = None

    def setup_layout(self):
        flex_grid_sizer = wx.FlexGridSizer(30, 1, 10, 10)
        flex_grid_sizer.AddMany(self.layout_items)
        flex_grid_sizer.AddGrowableCol(0)
        flex_grid_sizer.AddGrowableRow(0)

        box_sizer = wx.BoxSizer(wx.VERTICAL)
        box_sizer.Add(
            flex_grid_sizer,
            proportion=2,
            flag=wx.EXPAND | wx.ALL,
            border=10,
        )

        self.SetSizer(box_sizer)
        self.Fit()
        self.Show()

    # menu bar related func
    def create_menu_bar(self):
        menu = wx.Menu()

        reload = menu.Append(-1, "Reload Config File")
        menu.AppendSeparator()
        self.stay_on_top = menu.AppendCheckItem(-1, "App On Top")
        menu.AppendSeparator()

        self.Bind(wx.EVT_MENU, self.reload_config_file, reload)
        self.Bind(wx.EVT_MENU, self.toggle, self.stay_on_top)

        menu_bar = wx.MenuBar()
        menu_bar.Append(menu, "Menu")

        self.SetMenuBar(menu_bar)

    def reload_config_file(self, event):
        os.chdir(os.path.dirname(os.path.abspath(__file__)))
        # setup_default_picture_width()
        # setup_default_picture_top()
        # setup_default_crop()
        # self.setup_default_radio_button()
        # self.setup_default_text_information()
        # self.init_ui()
        # self.Layout()
        self.init()

    def toggle(self, event=None):
        if self.stay_on_top.IsChecked():
            self.set_on_top()
        else:
            self.cancel_on_top()

    def set_on_top(self, event=None):
        # self.SetWindowStyle(self.old_style | wx.STAY_ON_TOP)
        self.SetWindowStyle(wx.STAY_ON_TOP)
        self.stay_on_top.Check(True)

    def cancel_on_top(self, event=None):
        self.SetWindowStyle(self.old_style)
        self.stay_on_top.Check(False)

    # app on top related function
    def init_stay_on_top(self):
        """app on top setup"""
        self.set_style()
        config = configparser.ConfigParser()
        config.read("a.txt", "UTF-8")
        try:
            if config["app_on_top"]["on_top"] == "Yes":
                self.set_on_top()
            else:
                self.cancel_on_top()
        except KeyError:
            self.cancel_on_top()

    def set_style(self, event=None):
        self.old_style = self.GetWindowStyle()

    # main app related func
    def create_choice_layout(self, key, choices, default):
        self.text_ctrl[key] = wx.Choice(self, size=(self.gui_width, 28))
        for choice in choices:
            self.text_ctrl[key].Append(choice)
        self.text_ctrl[key].SetSelection(default)

        self.text_ctrl[key].Bind(wx.EVT_CHOICE, self.save_choice)
        self.text_ctrl[key].key = key
        self.layout_items.append(self.text_ctrl[key])

    def create_text_layout(self, key, label):
        self.static_text[key] = wx.StaticText(
            self, label=label, size=(self.gui_width, -1)
        )
        self.static_text[key].key = key

        try:
            self.static_text[key].SetLabel(self.text_data.get(key))
        except TypeError:
            pass

        self.layout_items.append(self.static_text[key])

    def create_text_control_layout(self, key, hint=""):
        self.text_ctrl[key] = wx.TextCtrl(self, size=(self.gui_width, -1))
        self.text_ctrl[key].SetHint(hint=hint)
        self.text_ctrl[key].Bind(wx.EVT_TEXT, self.save_text)
        self.text_ctrl[key].key = key

        try:
            self.text_ctrl[key].SetLabel(self.text_data.get(key))
        except TypeError:
            pass

        self.layout_items.append(self.text_ctrl[key])

    def create_text_ctrl_and_browse_layout(
        self,
        key,
        func,
        label,
        hint="",
    ):
        self.create_text_control_layout(key=key, hint=hint)
        self.create_button_layout(key=key, func=func, label=label)

    def create_button_layout(self, key, label, func):
        self.button[key] = wx.Button(
            self, size=(self.gui_width, -1), label=label
        )
        self.button[key].key = key
        self.button[key].Bind(wx.EVT_BUTTON, eval(func))
        self.layout_items.append(self.button[key])

    def create_radio_button_layout(
        self,
        key,
        buttons,
        label,
        alignment="horizontal",
        height_coefficient=0.9,
    ):

        button_array = buttons

        if alignment == "horizontal":
            style = wx.HORIZONTAL
            height = 1.5
        else:
            style = wx.VERTICAL
            height = height_coefficient * len(buttons)

        box_height = int(self.radio_box_height_per_1_box * height)
        self.radio_box[key] = wx.RadioBox(
            self,
            id=wx.ID_ANY,
            label=label,
            choices=button_array,
            style=style,
            size=(self.gui_width, box_height),
        )
        self.radio_box[key].key = key
        self.radio_box[key].Bind(
            wx.EVT_RADIOBOX, self.update_selected_radio_button
        )
        self.radio_box[key].EnableItem(
            self.selected_radio_buttons.get(key), True
        )
        self.radio_box[key].SetSelection(self.selected_radio_buttons[key])
        self.layout_items.append(self.radio_box[key])

    def save_text(self, event):
        key = event.GetEventObject().key
        self.text_data[key] = event.GetEventObject().GetValue()

    def save_choice(self, event):
        key = event.GetEventObject().key
        n = event.GetEventObject().GetSelection()
        self.text_data[key] = event.GetEventObject().GetString(n)

    def file_browse(self, event):
        btn = event.GetEventObject()
        key = btn.key

        default_file_path = ""
        default_dir = ""

        file = wx.FileDialog(
            self,
            style=wx.DD_CHANGE_DIR,
            defaultFile=default_file_path,
            defaultDir=default_dir,
        )
        if file.ShowModal() == wx.ID_OK:
            file_path = file.GetPath()
            self.text_ctrl[key].SetLabel(file_path)
            self.text_data[key] = file_path

    def folder_browse(self, event, default_path=os.getcwd()):
        btn = event.GetEventObject()
        key = btn.key

        folder = wx.DirDialog(
            self, style=wx.DD_CHANGE_DIR, defaultPath=default_path
        )
        if folder.ShowModal() == wx.ID_OK:
            folder_path = folder.GetPath()
            try:
                self.text_ctrl[key].SetLabel(folder_path)
                self.text_data[key] = folder_path
            except KeyError:
                pass

    def update_selected_radio_button(self, event):
        key = event.GetEventObject().key
        self.selected_radio_buttons[key] = self.radio_box[key].GetSelection()
        # self.radio_box[key].GetStringSelection() # this is better ?
        if self.layout == "dynamic":
            self.init()

    def init(self):
        self.clean_ui()
        self.init_ui()
        self.Layout()

    def init_ui(self):
        """user needs to add layout to this function"""
        pass

    def clean_ui(self):
        for key in list(self.text_ctrl.keys()):
            self.text_ctrl[key].Destroy()
            del self.text_ctrl[key]

        for key in list(self.button.keys()):
            self.button[key].Destroy()
            del self.button[key]

        for key in list(self.static_text.keys()):
            self.static_text[key].Destroy()
            del self.static_text[key]

        for key in list(self.radio_box.keys()):
            self.radio_box[key].Destroy()
            del self.radio_box[key]

        self.layout_items = []

    def read_config_file(self, file):
        config = configparser.ConfigParser()
        config.read(file, "UTF-8")

        try:
            radio_button_section = config["radio_button"]
            for key, value in radio_button_section.items():
                self.selected_radio_buttons[key] = int(value)
        except KeyError:
            pass

        try:
            text_data_section = config["text_data"]
            for key, value in text_data_section.items():
                self.text_data[key] = value
        except KeyError:
            pass

        try:
            replace_data_section = config["replace_data"]
            for key, value in replace_data_section.items():
                self.replace_data[key] = value
        except KeyError:
            pass

    def set_drop_target(self, key, mode):
        file_drop_target = MyFileDropTarget(self, key=key, mode=mode)
        self.text_ctrl[key].SetDropTarget(file_drop_target)

    def SetInsertionPointEnd(self, key):
        # Put insertion point at end of text control to prevent overwriting
        # This function works when file drop
        self.text_ctrl[key].SetInsertionPointEnd()

    def updateText(self, text, key):
        # Write text to the text control
        # This function works when file drop
        self.text_ctrl[key].Clear()
        self.text_ctrl[key].WriteText(text)
        self.text_data[key] = text

    # noinspection PyMethodMayBeStatic
    def show_message_box(self, message):
        wx.MessageBox(message=message)

    # noinspection PyMethodMayBeStatic
    def show_message_dialog(self, message):
        dialog = wx.MessageDialog(
            None,
            message=message,
            caption="hello world",
            style=wx.YES_NO | wx.ICON_QUESTION,
        )
        reply = dialog.ShowModal()
        if reply == wx.ID_NO:
            return False
        else:
            return True


class MyFileDropTarget(wx.FileDropTarget):
    def __init__(self, window, key, mode):
        wx.FileDropTarget.__init__(self)
        self.window = window
        self.key = key
        self.mode = mode  # folder or file

    def OnDropFiles(self, x, y, filenames):
        self.window.SetInsertionPointEnd(key=self.key)

        if self.mode == "folder" and os.path.isdir(filenames[0]):
            self.window.updateText(filenames[0], self.key)
        if self.mode == "file" and os.path.isfile(filenames[0]):
            self.window.updateText(filenames[0], self.key)

        return True


class MyGui(GuiLibWx):
    def __init__(self, parent, title, height, width, pos, layout):
        super(MyGui, self).__init__(
            parent,
            title=title,
            height=height,
            width=width,
            pos=pos,
            layout=layout,
        )
        self.selected_radio_buttons = {"radio_button": 0}
        self.text_data = {"folder_browse": os.getcwd()}

        self.read_config_file(file="config.txt")

        self.SetIcon(wx.Icon(resource_path("./image/python.png")))
        self.taskbar = wx.adv.TaskBarIcon()
        self.taskbar.SetIcon(
            wx.Icon(resource_path("./image/python.png"), wx.BITMAP_TYPE_PNG), ""
        )
        self.init()

    def init_ui(self):
        self.create_menu_bar()
        self.create_text_layout(key="MyApp", label="MyApp")
        self.create_text_control_layout(key="text_ctrl", hint="text_ctrl")

        self.create_text_ctrl_and_browse_layout(
            key="file_browse", func="self.file_browse", label="browse"
        )
        self.set_drop_target(key="file_browse", mode="file")

        self.create_text_ctrl_and_browse_layout(
            key="folder_browse", func="self.folder_browse", label="browse"
        )
        self.set_drop_target(key="folder_browse", mode="folder")
        self.create_radio_button_layout(
            key="radio_button", buttons=["a", "b"], label="button layout"
        )
        if self.selected_radio_buttons["radio_button"] == 1:
            self.create_text_layout(key="MyApp", label="MyApp")

        self.create_button_layout(
            key="execute",
            label="execute",
            func="self.execute",
        )
        self.create_choice_layout(
            key="choice", choices=["1", "2", "3"], default=1
        )

        self.setup_layout()
        self.init_stay_on_top()

    def execute(self, event=None):
        print(self.text_data["folder_browse"])
        print(self.selected_radio_buttons)
        print(self.text_data)


