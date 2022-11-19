import tkinter as tk
from tkinter import ttk

from PIL import Image, ImageTk

# from tkinter import messagebox
import os

# import OCRFlow as OCRF
# import toml
import customtkinter as ck

# from CV2Setting import straightlinesetting
from GCloudVision import AutoLine, LineTomlOut

# import ScrollableFrame as SF
# import tomlCreate as toml_c
from tkinter import filedialog, messagebox

# import FrameClass

from functools import wraps
import traceback

import ControlGUI
import logging.config
import os
import LineEditGUI_Frame

import Functions

import IconCode

# import threading

# ロガー########################################################################################
logging.config.fileConfig(os.getcwd() + r"\LogConf\logging_debug.conf")
logger = logging.getLogger(__name__)
# デコレーター##################################################################################
def log_decorator():
    def _log_decorator(func):
        def wrapper(*args, **kwargs):
            try:
                logger.info("処理を開始します")
                return func(*args, **kwargs)

            except Exception as e:
                logger.error("エラーが発生しました")
                raise e

            finally:
                logger.info("処理を終了します")

        return wrapper

    return _log_decorator


###################################################################################################
# class Application(tk.Frame):
class Application(ttk.Frame):
    def __init__(self, master, control):
        super().__init__(master)

        # ルートフレームの行列制限
        self.grid_rowconfigure(0, weight=1)
        self.grid_columnconfigure(1, weight=1)

        # コントロール
        self.control = control
        self.control.App = self
        self.control.wid_Par = self.control.width_of_window / 1459
        self.control.hei_Par = self.control.height_of_window / 820

        # ルートウィンドウ#########################################################################
        self.control.LineEdit_root = tk.Frame(master=master)
        self.control.LineEdit_root.pack(fill=tk.BOTH, expand=True)
        self.control.LineEdit_root.bind("<Motion>", self.change)  # 下ウィンドウにマウス移動関数bind

        # トップウィンドウ#########################################################################
        self.control.top = tk.Toplevel(master=master)
        self.control.top._name = "TOP_Main"
        # トップウィンドウの行列制限
        self.control.top.grid_rowconfigure(1, weight=1)
        self.control.top.grid_columnconfigure(1, weight=1)
        data = IconCode.icondata()
        self.control.top.tk.call(
            "wm",
            "iconphoto",
            self.control.top._w,
            tk.PhotoImage(data=data, master=self.control.top),
        )
        self.control.top.geometry(
            "%dx%d+%d+%d"
            % (
                self.control.width_of_window,
                self.control.height_of_window,
                self.control.x_coodinate,
                self.control.y_coodinate,
            )
        )
        self.control.top.wm_attributes("-transparentcolor", "snow")  # トップWindowの白色を透過
        self.control.top.wm_attributes("-topmost", True)  # 常に一番上のウィンドウに指定
        self.control.top.bind("<Motion>", self.change)  # 透過ウィンドウにマウス移動関数bind
        self.control.MenuCreate(self.control.top)  # メニューバー作成

        # トップウィンドウフレーム##################################################################
        self.control.top.window_rootFrame = tk.Frame(
            master=self.control.top,
            width=self.control.width_of_window,
            height=self.control.height_of_window,
        )
        self.control.top.window_rootFrame.pack(fill=tk.BOTH, expand=True)

        self.FrameCreate()  # フレーム作成
        self.control.top.withdraw()

    # 要素作成######################################################################################
    def FrameCreate(self):
        # # サイドメニュー作成
        self.SideFrame = tk.Frame(
            self.control.top.window_rootFrame,
            width=self.control.Left_Column,
            height=self.control.height_of_window,
            bg="snow",
            relief=tk.GROOVE,
        )
        self.SideFrame.pack(side=tk.LEFT, fill=tk.Y)
        # self.SideFrame.grid(row=0, column=0, rowspan=2, sticky=tk.N + tk.S)

        # サイドメニュー幅調整の為ツリービュー等挿入
        tree = ttk.Treeview(self.SideFrame)
        tree.pack(side=tk.BOTTOM)

        # ボトムメニュー作成
        self.bottumFrame = tk.Frame(
            self.control.top.window_rootFrame,
            width=self.control.FCW,
            height=self.control.Bottom_Column,
            bg="black",
            relief=tk.GROOVE,
        )
        self.bottumFrame.pack(side=tk.BOTTOM, fill=tk.BOTH, expand=True)
        # self.bottumFrame.grid(row=1, column=1, sticky=tk.N + tk.S)

        # 透過キャンバスフレーム
        self.control.topFrame = tk.Frame(
            self.control.top.window_rootFrame,
            bg="white",
            width=self.control.FCW,
            height=self.control.FCH,
            relief=tk.GROOVE,
            bd=2,
        )
        self.control.topFrame.pack(side=tk.RIGHT, fill=tk.BOTH, expand=True)
        # self.control.topFrame.grid(row=0, column=1, sticky=tk.NSEW)

        # 透過キャンバス作成
        self.control.top.forward = tk.Canvas(
            self.control.topFrame,
            background="snow",
            width=self.control.FCW,
            height=self.control.FCH,
        )
        self.control.top.forward.pack(side=tk.TOP, fill=tk.BOTH, expand=True)
        self.control.top.forward.bind("Enter", self.change)
        self.control.Transparent_Create(self)  # 透過キャンバス描画

        self.bottumFrame.propagate(0)
        #################################################################################

        self.control.back = tk.Canvas(
            self.control.LineEdit_root,
            background="snow",
            width=self.control.FCW,
            height=self.control.FCH,
        )

        self.control.back.pack(side=tk.TOP, fill=tk.BOTH, expand=True)  # 下Windowを配置

        self.backBottom = tk.Frame(
            self.control.LineEdit_root, height=self.control.Bottom_Column
        )
        self.backBottom.pack(side=tk.BOTTOM, fill=tk.BOTH, expand=True)

        self.control.ImportIMG()
        self.control.LineEdit_root.bind("<Configure>", self.change)
        # self.control.LineEdit_root.bind("<Unmap>", self.unmap)
        # self.control.LineEdit_root.bind("<Map>", self.map)
        self.control.back.bind("<Double-1>", self.backbind)  # 下ウィンドウにダブルクリックbind
        self.control.back.bind("<Double-3>", self.Right_backbind)  # 下ウィンドウにダブルクリックbind
        self.control.back.bind("<Motion>", self.change)  # 透過ウィンドウにマウス移動関数bind
        LineEditGUI_Frame.Frame1(self)
        LineEditGUI_Frame.Frame2(self)
        LineEditGUI_Frame.Frame3(self)

    # ------------------------------------------------------------------------------------

    # 関数##############################################################################
    # 円、矩形、直線を描画＆ドラッグできるようにする【tkinter】
    def click1(self, event):
        """
        縦直線描画処理(画面クリック)
        """
        self.Line_txt.delete(0, tk.END)
        self.x2 = event.x
        self.y2 = event.y
        self.id1 = event.widget.find_closest(self.x2, self.y2)
        self.TName = event.widget.gettags(self.id1[0])[0]
        self.Line_txt.insert(tk.END, self.TName)
        self.x1 = self.x2
        self.y1 = self.y2

    # ---------------------------------------------------------------------------------------------
    def EventDelete(self, event):
        """
        線削除処理(画面ダブルクリック)
        """
        self.x2 = event.x
        self.y2 = event.y
        self.id1 = event.widget.find_closest(self.x2, self.y2)
        self.TName = event.widget.gettags(self.id1[0])[0]
        event.widget.delete(self.TName)
        r = 0
        for tagsListItem in self.control.tagsList:
            if self.TName == tagsListItem[0][0]:
                self.control.tagsList.pop(r)
                break
            r += 1
        nptag_L = LineTomlOut(self.control.tagsList, self.control.HCW, self.control.HCH)
        if nptag_L[0] is True:
            ####################################################################################
            self.control.Yoko_N = self.control.tomlTitle + "_Yoko"
            self.control.Tate_N = self.control.tomlTitle + "_Tate"
            nptag_L[1].sort()
            nptag_L[2].sort(key=lambda x: x[1])
            self.control.tomlsetting["LineSetting"][self.control.Yoko_N] = nptag_L[1]
            self.control.tomlsetting["LineSetting"][self.control.Tate_N] = nptag_L[2]
            Functions.dump_toml(self.control.tomlsetting, self.control.tomlurl)
            ####################################################################################
        else:
            print("Err")
        self.Line_txt.delete(0, tk.END)

    # ---------------------------------------------------------------------------------------------
    def serchmaster(self):
        sm = False
        m = self.master
        while sm is False:
            m = m.master
            if m is not None:
                Em = m
            else:
                sm = True
        return Em

    # ---------------------------------------------------------------------------------------------
    def change(self, event):
        """
        上下ウィンドウ連携処理(ウィンドウサイズ変更)
        """
        top_geometry = self.control.top.geometry()
        w_diff = self.control.width_of_window - int(top_geometry.split("x")[0])
        if w_diff <= 1500:
            self.control.top.attributes("-topmost", True)
            sm = self.serchmaster()
            sm.geometry(top_geometry)

    # ---------------------------------------------------------------------------------------------
    def ChangeToml(self):
        """
        tomlリストを変更
        """
        try:
            typ = [("tomlファイル", "*.toml")]
            self.control.top.withdraw()
            tomlurl = filedialog.askopenfilename(filetypes=typ)
            if tomlurl != "":
                try:
                    self.control.top.destroy()
                    self.master.destroy()
                except:
                    print("")
                messagebox.showinfo("設定ファイル再読込", "設定ファイルを再読み込みします。")
                self.control.debug("tomlファイル再読込")  # Log出力
                Open()
                self.control.debug("tomlファイル再読込完了")  # Log出力
            else:
                messagebox.showinfo("確認", "設定ファイルを指定してください。")
                self.control.top.deiconify()
        except:
            self.control.debug("tomlファイル変更Err")  # Log出力
            self.control.top.deiconify()

    # ---------------------------------------------------------------------------------------------
    def blankno(self):
        if len(self.control.tagsList) != 0:
            TN_List = [
                int(str(t[0][0]).replace("Line", "")) for t in self.control.tagsList
            ]
            TN_List.sort()
            N_TN_r = 0
            for TN_r in TN_List:
                if N_TN_r == 0:
                    N_TN_r = TN_r + 1
                else:
                    if N_TN_r == TN_r:
                        N_TN_r = TN_r + 1
                    else:
                        return N_TN_r
            N_TN_r = TN_r + 1
            return N_TN_r
        else:
            return 1

    # ---------------------------------------------------------------------------------------------
    def backbind(self, event):
        """
        縦直線追加ダブルクリック処理
        """

        self.TName = "Line" + str(self.blankno())
        # sm = self.control.topFrame.children["!canvas"]
        self.control.top.forward.create_line(
            event.x,
            0,
            event.x,
            self.control.FCH,
            tags=self.TName,
            width=7,
            fill="#FF0000",
            activefill="#DBDD6F",
        )
        self.control.top.forward.tag_bind(self.TName, "<ButtonPress-1>", self.click1)
        self.control.top.forward.tag_bind(
            self.TName, "<Control-Double-1>", self.EventDelete
        )
        self.control.top.forward.tag_bind(self.TName, "<B1-Motion>", self.drag1)
        BSS = [0, 0, 0, 0]
        TSS = [self.TName, event.x, 0, event.x, self.control.FCH, "Yoko"]
        self.control.tagsList.append([TSS, BSS])

    # ---------------------------------------------------------------------------------------------
    def Right_backbind(self, event):
        """
        横直線追加ボタン処理
        """

        self.TName = "Line" + str(self.blankno())
        sm = self.control.topFrame.children["!canvas"]
        sm.create_line(
            0,
            event.y,
            self.control.FCW,
            event.y,
            tags=self.TName,
            width=7,
            fill="#00FF40",
            activefill="#DBDD6F",
        )
        sm.tag_bind(self.TName, "<ButtonPress-1>", self.click1)
        sm.tag_bind(self.TName, "<Control-Double-1>", self.EventDelete)
        sm.tag_bind(self.TName, "<B1-Motion>", self.drag1)
        TSS = [self.TName, 0, event.y, self.control.FCW, event.y, "Tate"]
        BSS = [0, 0, 0, 0]
        self.control.tagsList.append([TSS, BSS])

    # ---------------------------------------------------------------------------------------------
    def drag1(self, event):
        """
        縦直線移動処理(ドラッグ)
        """
        self.x2 = event.x
        self.y2 = event.y
        self.del_x1 = self.x2 - self.x1
        self.del_y1 = self.y2 - self.y1
        self.x0, self.y0, self.x1, self.y1 = event.widget.coords(self.id1)
        event.widget.coords(
            self.id1,
            self.x0 + self.del_x1,
            self.y0 + self.del_y1,
            self.x1 + self.del_x1,
            self.y1 + self.del_y1,
        )
        self.x1 = self.x2
        self.y1 = self.y2

    # ---------------------------------------------------------------------------------------------


@log_decorator()
def Open():
    control = ControlGUI.ControlGUI("./", logger)  # セルフコントローラー
    main_window = tk.Tk()
    top = tk.Toplevel()
    Application(top, control)
    main_window.mainloop()


if __name__ == "__main__":
    Open()
