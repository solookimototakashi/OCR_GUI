import tkinter as tk
from tkinter import ttk
from PIL import Image, ImageTk

import os
import logging.config
from platform import machine, node, platform, processor, release, system, version
from socket import gethostbyname, gethostname
from uuid import getnode

import ControlGUI
import Functions
import IconCode

# 自作のページビューをインポート
from page_view import ViewGUIPage, LineEditPage, P_TablePage

# from line_profiler import LineProfiler

# exe化コマンド↓
# pyinstaller ViewGUI.py --onefile --onedir --noconsole --clean --icon=hasegawa.ico
# 上記コマンドでできた[dist]→[ViewGUI]フォルダ内に
# [poppler-22.01.0フォルダ]・[Tesseract-OCRフォルダ]・[StraightListTate.csv]・[StraightListYoko.csv]・[key.json]
# customtkinterフォルダ・LogConfフォルダ・Logフォルダ・CompanyDataフォルダ・D_curcle_a.png・D_curcle_b.png
# をコピーして完了
# ロガー########################################################################################
# logging.config.fileConfig(os.getcwd() + r"\LogConf\logging_debug.conf")
# logger = logging.getLogger(__name__)
# logger.debug(f"Network: {node()}")  # ネットワーク名
# logger.debug(f"Machine: {machine()}")  # 機種
# logger.debug(f"Processor: {processor()}")  # プロセッサ名 (CPU)
# logger.debug(f"Platform: {platform() }")  # プラットフォーム (OS) 情報
# logger.debug(f"System: {system() }")  # OS名
# logger.debug(f"Release: {release()}")  # リリース情報
# logger.debug(f"Version: {version()}")  # バージョン情報
# logger.debug(f"MAC Address: {getnode():_X}")  # MACアドレス
# logger.debug(f"Host name: {gethostname()}")  # ホスト名
# logger.debug(f"IP Address: {gethostbyname(gethostname())}")  # IPアドレス
# デコレーター##################################################################################
# def log_decorator():
#     def _log_decorator(func):
#         def wrapper(*args, **kwargs):
#             try:
#                 logger.info("処理を開始します")
#                 return func(*args, **kwargs)

#             except Exception as e:
#                 logger.error("エラーが発生しました")
#                 raise e

#             finally:
#                 logger.info("処理を終了します")

#         return wrapper

#     return _log_decorator


# ############################################################################################
class SettingsView(ttk.Frame):
    def __init__(self, master, **kw):
        super().__init__(master, **kw)
        self.control = ControlGUI.ControlGUI(master, os.getcwd())
        self.pages = {}
        # ルートフレームの行列制限
        self.grid_rowconfigure(0, weight=1)
        self.grid_columnconfigure(1, weight=1)
        # サイドツリーフレームを作成
        self.create_frame_treeview().grid(row=0, column=0, sticky="ens")
        # フレーム作成
        self.create_frame_page().grid(row=0, column=1, sticky=tk.NSEW)
        # 共通設定読込
        master._name = "BOTTOM_Main"
        self.control.MenuCreate(master)  # メニューバー作成
        # ######################################################################
        master.geometry(
            "%dx%d+%d+%d"
            % (
                self.control.width_of_window,
                self.control.height_of_window,
                self.control.x_coodinate,
                self.control.y_coodinate,
            )
        )
        # root.minsize(control.width_of_window, control.height_of_window)
        # 　メインウィンドウタイトル
        master.title(self.control.Toptitle)

    def create_frame_page(self) -> ttk.Frame:
        """
        選択したページ設定のフレーム作成
        return:ttk.Frame
        """

        self.frame_page = ttk.Frame(master=self)

        return self.frame_page

    def create_frame_treeview(self) -> ttk.Frame:
        """
        設定ツリービューフレームクラスの作成、インスタンス化
        return:ttk.Frame
        """
        self.frame_treeview = ttk.Frame(master=self, width=self.control.Left_Column)

        self.treeview_settings = SettingsTreeview(self.frame_treeview)
        self.treeview_settings.bind_all(
            "<<TreeviewSelect>>", self.on_treeview_selection_changed
        )
        self.treeview_settings.pack(fill=tk.BOTH, expand=True)

        return self.frame_treeview

    def on_treeview_selection_changed(self, event):
        """
        設定ツリービュー操作によるフレーム切替イベント
        """

        selected_item = self.treeview_settings.focus()
        setting_name = self.treeview_settings.item(selected_item).get("text")

        self.show_page(setting_name)

    def show_page(self, setting_name: str):
        """
        引数ページ名から該当のページを読み込む
        """
        # アクティブウィンドウサイズを取得
        pm = self.master.geometry()

        for page_name in self.pages.keys():
            self.pages[page_name].pack_forget()

        if setting_name == "Audio":
            self.pages[setting_name].pack(fill=tk.BOTH, expand=True)
            self.master.geometry(pm)
            self.control.top.geometry(pm)
            self.control.top.deiconify()
            self.control.top.wm_attributes("-topmost", True)  # 常に一番上のウィンドウに指定

        else:
            self.pages[setting_name].pack(fill=tk.BOTH, expand=True)
            self.control.top.withdraw()

    def add_page(self, image_path: str, setting_name: str, page):
        """
        ページフレームをインスタンス化し、ディクショナリ追加
        """
        with Image.open(image_path) as img:
            photo_image = ImageTk.PhotoImage(img.resize((100, 20)), master=self)

        self.pages[setting_name] = page(self.frame_page)
        self.pages[setting_name].image = photo_image
        self.treeview_settings.add_setting(image=photo_image, section_text=setting_name)

        self.pages[setting_name].pack(fill=tk.BOTH, expand=True)


# ###########################################################################################
class SettingsTreeview(ttk.Treeview):
    """
    サイドメニューに要素挿入
    """

    def _init(self, master, **kw):
        super().__init__(master, **kw)
        self.heading("#0", text="Settings")

    def add_setting(self, image, section_text: str):
        """
        行挿入
        """
        self.insert(parent="", index=tk.END, image=image, text=section_text)


# ###########################################################################################


if __name__ == "__main__":

    # ルート作成
    root = tk.Tk()

    width_of_window = int(int(root.winfo_screenwidth()) * 0.98)
    height_of_window = int(int(root.winfo_screenheight()) * 0.9)

    data = IconCode.icondata()
    root.tk.call("wm", "iconphoto", root._w, tk.PhotoImage(data=data, master=root))
    # ######################################################################

    # ttk.style設定
    style = ttk.Style()
    style.theme_use("clam")
    # ツリービューヘッダーカラー設定
    style.configure(
        "Treeview.Heading",
        relief="flat",
        background="#CCFFFF",
    )
    # ツリービューメニュースタイル設定
    style.configure("Treeview", rowheight=28)
    # ツリービューメニュー外スタイル設定
    style.configure("Treeview", fieldbackground="#CCFFFF")
    # ツリービューホバーカラー設定
    style.map(
        "Treeview",
        foreground=[("disabled", "#CCFFFF"), ("selected", "darkgreen")],
        background=[("disabled", "#CCFFFF"), ("selected", "lightgreen")],
    )
    style.configure("TLabel", font=("tkDefaultFont", 18))
    settings = SettingsView(root, relief="flat")
    # settings = SettingsView(root)
    settings.add_page(
        # image_path=r"C:\Users\もちねこ\Desktop\GitHub\RPAScript\OCRViewFromMenu\ImageCreate_btn.png",
        image_path=r"D:\PythonScript\RPAScript\OCRViewFromMenu\ImageCreate_btn.png",
        setting_name="Language",
        page=ViewGUIPage,
    )
    settings.add_page(
        # image_path=r"C:\Users\もちねこ\Desktop\GitHub\RPAScript\OCRViewFromMenu\ImageCreate_btn.png",
        image_path=r"D:\PythonScript\RPAScript\OCRViewFromMenu\ImageCreate_btn.png",
        setting_name="Audio",
        page=LineEditPage,
    )
    settings.add_page(
        # image_path=r"C:\Users\もちねこ\Desktop\GitHub\RPAScript\OCRViewFromMenu\ImageCreate_btn.png",
        image_path=r"D:\PythonScript\RPAScript\OCRViewFromMenu\ImageCreate_btn.png",
        setting_name="P_Table",
        page=P_TablePage,
    )
    settings.pack(fill=tk.BOTH, expand=True)
    root.mainloop()
