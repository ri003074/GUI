import wx
from lib.gui_lib_wx import MyGui
if __name__ == "__main__":
    app = wx.App()
    MyGui(
        None,
        title="",
        height=300,
        width=300,
        pos=(100, 100),
        layout="dynamic",
        # layout="static",
    )
    app.MainLoop()
