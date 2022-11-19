import tkinter as tk
from tkinter import *
from pandastable import Table, TableModel, config


class MyTable(Table):
    """Custom table class inherits from Table. You can then override required methods"""

    def __init__(self, parent=None, **kwargs):
        Table.__init__(self, parent, **kwargs)
        return

        def handle_left_click(self, event):
            # """Example - override left click"""

            Table.handle_left_click(self, event)

        # do custom code here
        return

    def popupMenu(self, event, rows=None, cols=None, outside=None):
        """Custom right click menu"""

        popupmenu = self.Menu(self, tearoff=0)

        def popupFocusOut(event):
            popupmenu.unpost()
            # add commands here

        # self.app is a reference to the parent app
        popupmenu.add_command(label="do stuff", command=self.app.stuff)
        popupmenu.bind("<FocusOut>", popupFocusOut)
        popupmenu.focus_set()
        popupmenu.post(event.x_root, event.y_root)
        return popupmenu
