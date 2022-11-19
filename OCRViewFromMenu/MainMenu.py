import tkinter as tk
import customtkinter as ck
import os
import logging.config
from platform import machine, node, platform, processor, release, system, version
from socket import gethostbyname, gethostname
from uuid import getnode
from ControlGUI import ControlGUI
from tkinter import messagebox
from PIL import Image, ImageTk
import ViewGUI
import IconCode
import Functions
from functools import wraps

# from line_profiler import LineProfiler

# exe化コマンド↓
# pyinstaller ViewGUI.py --onefile --onedir --noconsole --clean --icon=hasegawa.ico
# 上記コマンドでできた[dist]→[ViewGUI]フォルダ内に
# [poppler-22.01.0フォルダ]・[Tesseract-OCRフォルダ]・[StraightListTate.csv]・[StraightListYoko.csv]・[key.json]
# customtkinterフォルダ・LogConfフォルダ・Logフォルダ・CompanyDataフォルダ・D_curcle_a.png・D_curcle_b.png
# をコピーして完了
# ロガー########################################################################################
logging.config.fileConfig(os.getcwd() + r"\LogConf\logging_debug.conf")
logger = logging.getLogger(__name__)
logger.debug(f"Network: {node()}")  # ネットワーク名
logger.debug(f"Machine: {machine()}")  # 機種
logger.debug(f"Processor: {processor()}")  # プロセッサ名 (CPU)
logger.debug(f"Platform: {platform() }")  # プラットフォーム (OS) 情報
logger.debug(f"System: {system() }")  # OS名
logger.debug(f"Release: {release()}")  # リリース情報
logger.debug(f"Version: {version()}")  # バージョン情報
logger.debug(f"MAC Address: {getnode():_X}")  # MACアドレス
logger.debug(f"Host name: {gethostname()}")  # ホスト名
logger.debug(f"IP Address: {gethostbyname(gethostname())}")  # IPアドレス
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


# ###############################################################################################


class MainMenu(tk.Frame):
    """
    概要: TKinterメインWindowクラス
    """

    def __init__(self, window_root):
        self.control = ControlGUI("./", self.logger)  # セルフコントローラー
        # ルートウィンドウ設定----------------------------------------------------------
        self.window_root = window_root
        self.width_of_window = int(int(self.window_root.winfo_screenwidth()) * 0.5)
        self.height_of_window = int(int(self.window_root.winfo_screenheight()) * 0.5)
        self.x_coodinate = self.width_of_window / 2
        self.y_coodinate = self.height_of_window / 2
        self.padx = self.x_coodinate / 4
        self.pady = self.y_coodinate / 4
        self.window_root.geometry(
            "%dx%d+%d+%d"
            % (
                self.width_of_window,
                self.height_of_window,
                self.x_coodinate,
                self.y_coodinate,
            )
        )
        self.window_root.minsize(self.width_of_window, self.height_of_window)
        self.window_root.title(self.control.Toptitle)
        self.window_root.protocol("WM_DELETE_WINDOW", self.click_close)  # 閉じる処理設定
        self.MenuCreate()  # メニューバー作成
        # ----------------------------------------------------------------------------
        # フレーム
        self.window_rootFrame = tk.Frame(
            self.window_root,
            width=self.width_of_window,
            height=self.height_of_window,
            bg="#60cad1",
        )
        self.window_rootFrame.pack(fill=tk.BOTH, expand=True)

        # 参照URL
        self.Dir = tk.Entry(
            master=self.window_rootFrame, width=int(self.width_of_window / 8)
        )
        self.Dir.pack(padx=self.padx, pady=10, fill=tk.BOTH, expand=True)

        # 画像編集起動ボタン
        btn_img = ImageTk.PhotoImage(
            Image.open(
                r"C:\Users\もちねこ\Desktop\GitHub\RPAScript\OCRViewFromMenu\ImageEdit_btn.png"
            ).resize((200, 200), Image.ANTIALIAS)
        )

        # 参照ダイアログボタン
        self.Dir_btn = ck.CTkButton(
            master=self.window_rootFrame,
            image=btn_img,
            text_font=self.control.btn_font,
            text="関与先フォルダ選択",
            text_color="snow",
            fg_color="#0fb7ff",
            width=int(self.width_of_window / 8),
            height=40,
            compound="left",
            command=lambda: Functions.event_set_folder(self),
            border_width=2,
            corner_radius=8,
            border_color="snow",
        )
        self.Dir_btn.pack(
            side=tk.TOP, padx=self.padx, pady=10, fill=tk.BOTH, expand=True
        )

        # 画像編集起動ボタン
        btn_img = ImageTk.PhotoImage(
            Image.open(
                r"C:\Users\もちねこ\Desktop\GitHub\RPAScript\OCRViewFromMenu\ImageEdit_btn.png"
            ).resize((200, 200), Image.ANTIALIAS)
        )
        self.ImageEdit_btn = ck.CTkButton(
            master=self.window_rootFrame,
            image=btn_img,
            text_font=self.control.btn_font,
            text="画像編集",
            text_color="snow",
            fg_color="#0fb7ff",
            width=190,
            height=40,
            compound="left",
            command=self.Open_View,
            border_width=2,
            corner_radius=8,
            border_color="snow",
        )
        self.ImageEdit_btn.pack(
            side=tk.TOP, padx=self.padx, pady=10, fill=tk.BOTH, expand=True
        )

    # 要素作成######################################################################################
    def MenuCreate(self):
        """
        メニューバー作成
        """
        self.window_root.config(bg="#60cad1")
        self.men = tk.Menu(self.window_root, tearoff=0)
        self.window_root.config(menu=self.men)
        self.menu_file = tk.Menu(self.men)
        self.men.add_command(
            label="フォルダ", command=lambda: Functions.event_set_file(self)
        )

    # セルフ関数#####################################################################################
    def Open_View(self):
        """
        ViewGuiを開く
        """
        if self.control.Kanyosaki_name != "":
            Top_l = tk.Toplevel()
            data = IconCode.icondata()
            Top_l.tk.call(
                "wm",
                "iconphoto",
                Top_l._w,
                tk.PhotoImage(data=data, master=Top_l),
            )
            ViewGUI.ViewGUI(Top_l, self.control)
        else:
            messagebox.askokcancel("確認", "関与先フォルダを指定してください。")

    def click_close(self):
        """
        ウィンドウ×ボタンクリック
        """
        if messagebox.askokcancel("確認", "終了しますか？"):
            self.logger.debug(f"{self.title}完了")  # Log出力
            self.window_root.destroy()

    ################################################################################################


@log_decorator()
def Open():
    main_window = tk.Tk()
    data = IconCode.icondata()
    main_window.tk.call(
        "wm", "iconphoto", main_window._w, tk.PhotoImage(data=data, master=main_window)
    )
    MainMenu(main_window)
    main_window.mainloop()


if __name__ == "__main__":
    Open()
