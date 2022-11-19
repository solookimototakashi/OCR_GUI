import tkinter as tk
from tkinter import ttk
import ViewGUI
import LineEditGUI
import P_Table

# import ImageViewer


class Page(ttk.Frame):
    def __init__(self, master, **kw):
        super().__init__(master, **kw)

    def verify(self):
        return True


class ViewGUIPage(Page):
    def __init__(self, master, **kw):
        super().__init__(master, **kw)
        # 共通設定読込
        self.control = controlSerach(self)
        self.create_frame_content().pack(fill=tk.BOTH, expand=True)

    def create_frame_content(self) -> ttk.Frame:
        """
        設定のウィジェット作成
        """
        self.fr = ttk.Frame(
            self,
            width=self.control.width_of_window,
            height=self.control.height_of_window,
        )
        self.fr.pack(fill=tk.BOTH, expand=True)
        self.frame_content = ViewGUI.ViewGUI(self.fr, self.control)

        return self.frame_content


class LineEditPage(Page):
    def __init__(self, master, **kw):
        super().__init__(master, **kw)
        # 共通設定読込
        self.control = controlSerach(self)
        self.create_frame_content().pack(fill=tk.BOTH, expand=True)
        self.control.First = False

    def create_frame_content(self) -> ttk.Frame:
        """
        設定のウィジェット作成
        """
        self.fr = ttk.Frame(
            self,
            width=self.control.width_of_window,
            height=self.control.height_of_window,
        )
        self.fr.pack(fill=tk.BOTH, expand=True)
        self.frame_content = LineEditGUI.Application(self.fr, self.control)

        return self.frame_content


class P_TablePage(Page):
    def __init__(self, master, **kw):
        super().__init__(master, **kw)
        # 共通設定読込
        self.control = controlSerach(self)
        self.create_frame_content().pack(fill=tk.BOTH, expand=True)
        self.control.First = False

    def create_frame_content(self) -> ttk.Frame:
        """
        設定のウィジェット作成
        """
        self.fr = ttk.Frame(
            self,
            width=self.control.width_of_window,
            height=self.control.height_of_window,
        )
        self.fr.pack(fill=tk.BOTH, expand=True)
        self.frame_content = P_Table.Application(self.fr, self.control)

        return self.frame_content


def controlSerach(self):
    master_f = True
    m = self.master
    while master_f is True:
        try:
            m = m.master
            if m is None:
                break
            else:
                Em = m
        except:
            master_f = False
    return Em.children["!settingsview"].control


if __name__ == "__main__":
    root = tk.Tk()
    root.geometry("640x480")

    ViewGUIPage(root)

    root.mainloop()
