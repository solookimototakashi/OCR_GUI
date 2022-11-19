import tkinter as tk

from PIL import Image, ImageTk
import customtkinter as ck

# from CV2Setting import straightlinesetting
from GCloudVision import AutoLine, LineTomlOut

# import ScrollableFrame as SF
# import tomlCreate as toml_c
from tkinter import filedialog, messagebox

from functools import wraps
import os
import MyTable as MT
import Functions
from pandastable import config
import numpy as np
import OCRFlow as OCRF

# 要素作成######################################################################################
def Frame1(self):
    # 配置
    # ボトムメニューフレーム##########################################################
    t_font = (1, int(8))

    Tframe = tk.Frame(
        self.bottumFrame,
        width=self.control.SideWidth,
        height=self.control.SideHeight,
        bg="#ecb5f5",
        relief=tk.GROOVE,
    )
    Tframe.pack(side=tk.LEFT, fill=tk.Y)  # , fill=tk.BOTH, expand=True)
    # LineNo表示テキスト
    ck.CTkLabel(
        master=Tframe,
        text="選択ライン名",
        width=self.control.Btn_width,
        height=self.control.Btn_height,
        corner_radius=8,
        text_font=t_font,
    ).grid(row=0, column=0, pady=5, sticky=tk.W)
    # テキストボックスの作成と配置
    self.Line_txt = ck.CTkEntry(
        master=Tframe,
        width=self.control.Btn_width,
        height=self.control.Btn_height,
        border_width=2,
        corner_radius=8,
        text_color="black",
        border_color="white",
        fg_color="white",
    )
    self.Line_txt.grid(row=0, column=1, padx=5, pady=5, sticky=tk.W)
    # テキスト変換一致率
    ck.CTkLabel(
        master=Tframe,
        text="テキスト変換一致率",
        width=self.control.Btn_width,
        height=self.control.Btn_height,
        corner_radius=8,
        text_font=t_font,
    ).grid(row=1, column=0, pady=5, sticky=tk.W)
    # テキストボックスの作成と配置
    self.ChangeVar = ck.CTkEntry(
        master=Tframe,
        width=self.control.Btn_width,
        height=self.control.Btn_height,
        border_width=2,
        corner_radius=8,
        text_color="black",
        border_color="white",
        fg_color="white",
    )
    self.ChangeVar.insert(0, 50)
    self.ChangeVar.grid(row=1, column=1, padx=5, pady=5, sticky=tk.W)
    # 行数表示テキスト
    ck.CTkLabel(
        master=Tframe,
        text="設定ファイル",
        width=self.control.Btn_width,
        height=self.control.Btn_height,
        corner_radius=8,
        text_font=t_font,
    ).grid(row=3, column=0, pady=5, sticky=tk.W)
    self.tomlurl = ck.CTkEntry(
        master=Tframe,
        width=self.control.Btn_width,
        height=self.control.Btn_height,
        border_width=2,
        corner_radius=8,
        text_color="black",
        border_color="white",
        fg_color="white",
    )
    self.tomlurl.insert(0, self.control.tomlurl)
    self.tomlurl.grid(row=3, column=1, padx=5, pady=5, sticky=tk.W)
    # 行数表示テキスト
    # 設定ファイル変更ボタン--------------------------------------------------------
    self.tomlbutton = ck.CTkButton(
        master=Tframe,
        text="設定ファイル変更",
        command=self.ChangeToml,
        width=self.control.Btn_width,
        height=self.control.Btn_height,
        border_width=2,
        corner_radius=8,
        text_color="white",
        border_color="white",
    )
    self.tomlbutton.grid(row=4, column=0, columnspan=2, padx=5, sticky=tk.W + tk.E)


# ------------------------------------------------------------------------------------
def Frame2(self):
    # ボトムメニュー内フレーム2########################################################
    Tframe2 = tk.Frame(
        self.bottumFrame,
        width=self.control.SideWidth,
        height=self.control.SideHeight,
        bg="#ecb5f5",
        relief=tk.GROOVE,
    )
    Tframe2.pack(side=tk.LEFT, fill=tk.Y)  # , fill=tk.BOTH, expand=True)
    self.control.SettingTB = create_table(
        self,
        Tframe2,
        "各列指定",
        self.control.LineEditGUI_df,
        int(self.control.width_of_window / 6),
        int(self.control.height_of_window / 10),
    )
    self.control.SettingTB2 = create_table(
        self,
        Tframe2,
        "出力列名",
        self.control.LineEditGUI_CS__df,
        int(self.control.width_of_window / 9),
        int(self.control.height_of_window / 10),
    )


# ------------------------------------------------------------------------------------
def Frame3(self):
    # ボトムメニュー内ボタンフレーム3###################################################
    Tframe3 = tk.Frame(
        self.bottumFrame,
        width=self.control.SideWidth,
        height=self.control.SideHeight,
        bg="#ecb5f5",
        relief=tk.GROOVE,
    )
    Tframe3.pack(side=tk.LEFT, fill=tk.BOTH, expand=True)
    # 自動直線描画ボタン---------------------------------------------------------------
    button3 = ck.CTkButton(
        master=Tframe3,
        text="自動直線描画",
        command=lambda: AutoNewLineCreate(self),
        width=self.control.Btn_width,
        height=self.control.Btn_height,
        border_width=2,
        corner_radius=8,
        text_color="white",
        border_color="white",
        fg_color="#2b5cff",
    )
    # button3.pack(side=tk.TOP, fill=tk.X, expand=True)
    button3.grid(row=0, column=0, padx=10, pady=5, sticky=tk.W + tk.E)
    # 削除ボタン---------------------------------------------------------------
    button5 = ck.CTkButton(
        master=Tframe3,
        text="全直線削除",
        command=lambda: AllLineDelete(self, self.control.top.forward),
        width=self.control.Btn_width,
        height=self.control.Btn_height,
        border_width=2,
        corner_radius=8,
        text_color="white",
        border_color="white",
        fg_color="Orange",
    )
    # button5.pack(side=tk.TOP, fill=tk.X, expand=True)
    button5.grid(row=1, column=0, padx=10, pady=5, sticky=tk.W + tk.E)
    # 確定ボタン---------------------------------------------------------------
    button4 = ck.CTkButton(
        master=Tframe3,
        text="確定",
        command=lambda: EnterP(self, self.control.top.forward),
        width=self.control.Btn_width,
        height=self.control.Btn_height,
        border_width=2,
        corner_radius=8,
        text_color="white",
        border_color="white",
        fg_color="steelblue3",
    )
    # button4.pack(side=tk.TOP, fill=tk.X, expand=True)
    button4.grid(row=2, column=0, padx=10, pady=5, sticky=tk.W + tk.E)


# ------------------------------------------------------------------------------------
def create_table(self, frame, t_title, df, wid, hei):
    """
    csv読込テーブル
    arg:self
    arg:tk.frame
    arg:str(title)
    arg:df
    return:tk.Frame
    """
    # ツリーフレーム設定---------------------------------------------------------------------
    f = tk.Frame(
        frame,
        width=wid,
        height=hei,
        bd=2,
        bg="#fce4d2",
        relief=tk.RIDGE,
    )  # 親フレーム
    f.pack(side=tk.LEFT, fill=tk.BOTH, expand=True)
    f_tree = tk.Frame(
        f,
        width=wid,
        height=hei,
        bg="#fce4d2",
    )  # 子フレーム
    # サイズグリップ
    # sizegrip = ttk.Sizegrip(self.OCR_frame)
    # sizegrip.grid(row=0, column=0, sticky=(tk.S, tk.E))
    tk.Label(f, text=t_title, bg="#fce4d2").grid(
        row=0, column=0, sticky=tk.N + tk.W
    )  # 位置指定
    f_tree.grid(row=2, column=0, padx=30, sticky=tk.N + tk.S + tk.W + tk.E)
    pt = MT.MyTable(
        f_tree,
        width=wid,
        height=hei,
        sticky=tk.N + tk.S + tk.W + tk.E,
        control=self.control,
    )  # テーブルをサブクラス化
    # df変換
    c_df = df
    c_df = c_df.fillna("Nan")  # nanを文字列で置換
    c_df = c_df.astype("str")  # df型変換
    c_df = c_df.replace("Nan", "", regex=True).replace(".0", "", regex=True)  # 文字列を置換
    # DF型変換------------------------------
    Functions.Pandas_mem_usage(c_df)
    # --------------------------------------
    pt.model.df = c_df
    pt._name = t_title
    # options is a dict that you can set yourself
    options = {"fontsize": self.control.t_font[1]}
    config.apply_options(options, pt)
    # --------------------------------------
    # 列幅設定
    # pt.columnwidths['Peak Frequency (Hz)'] = 225
    # pt.columnwidths['Channel'] = 25

    # pt.resized
    pt.show()  # テーブルモデルを一旦フレーム配置
    pt.showIndex()  # インデックス表示設定をオン
    pt.redraw()  # テーブル再表示
    return pt


# ------------------------------------------------------------------------------------
def AutoNewLineCreate(self):
    """
    自動直線描画ボタン処理
    """
    unmap(self)
    MSG = messagebox.askokcancel("確認", "自動直線描画しますか？")
    if MSG is True:
        AL = AutoLine(self.control.imgurl, 1)
        if AL[0] is True:
            ####################################################################################
            self.control.Yoko_N = self.control.tomlTitle + "_Yoko"
            self.control.Tate_N = self.control.tomlTitle + "_Tate"
            AL[1].sort()
            AL[2].sort(key=lambda x: x[1])

            YokoList = []
            for A in AL[1]:
                A.append("Yoko")
                YokoList.append(A)

            TateList = []
            for A in AL[2]:
                A.append("Tate")
                TateList.append(A)

            YokoList.extend(TateList)
            self.control.DB.list_to_df_replace_to_sql(self.control.table_name, YokoList)
            self.control.ReadDB()
            ####################################################################################
            self.control.Transparent_Create(self)  # 透過キャンバスに罫線描画

            MSG = messagebox.showinfo("確認", "自動直線描画完了")
            map(self)
        else:
            MSG = messagebox.showinfo("確認", "自動直線描画に失敗しました。")
            map(self)
    else:
        map(self)


# ---------------------------------------------------------------------------------------------
def AllLineDelete(self, selfC):
    """
    選択直線の削除
    """
    r = len(self.control.tagsList) - 1
    selfC.delete("all")
    for tagsListItem in reversed(self.control.tagsList):
        selfC.delete(tagsListItem[0][0])
        self.control.tagsList.pop(r)
        r -= 1


# ---------------------------------------------------------------------------------------------
def DFget(self, dfModel):
    """
    設定DFから必要項目取得
    """

    if dfModel._name == "各列指定":
        Daydf = dfModel.model.df.loc["日付列"]
        Moneydf = dfModel.model.df.loc["金額列"]
        Daydf = Daydf.dropna()
        Moneydf = Moneydf.dropna()
        # 条件テキストボックスのリスト化---------------------------
        self.control.DaySet = [a for a in list(Daydf) if a != ""]
        self.control.MoneySet = [a for a in list(Moneydf) if a != ""]
        return
    else:
        self.control.OutColumn = list(dfModel.model.df["列名"])
        return


# ---------------------------------------------------------------------------------------------
def listintCheck(list):
    """
    条件DFの型チェック
    """
    for listItem in list:
        try:
            int(listItem)
        except:
            return False
    return True


# ---------------------------------------------------------------------------------------------
def EnterP(self, selfC):
    """
    確定ボタンクリック
    """

    FList = []
    FYokoList = []
    FTateList = []
    # 各列指定設定テーブル#####################################
    DFget(self, self.control.SettingTB)
    DFget(self, self.control.SettingTB2)
    # ------------------------------------------------------
    # 条件テキストボックスの内容で処理分け-------------------------------------------------------------------
    if listintCheck(self.control.DaySet) is False:
        messagebox.showinfo("エラー", "日付列番号が不正です。数値以外を指定していないか確認してください。")
    elif listintCheck(self.control.MoneySet) is False:
        messagebox.showinfo("エラー", "金額表示列番号が不正です。数値以外を指定していないか確認してください。")
    else:
        if len(self.control.tagsList) == 0:
            messagebox.showinfo("エラー", "軸が設定されていません。")
        else:
            # ライン軸情報にBBox値(キャンバス上ライン軸)を追加
            for tagsListItem in self.control.tagsList:
                BB = self.control.top.forward.bbox(tagsListItem[0][0])
                try:
                    BBS = [BB[0], BB[1], BB[2], BB[3]]
                    FList.append([tagsListItem[0], tagsListItem[1], BBS])
                except:
                    print("BBSErr")
            # ライン軸情報に倍率をかける
            FYokoList, FTateList = EnterP_LineCalc(self, FList)
            # 軸数判定
            if len(FTateList) == 0:
                messagebox.showinfo("エラー", "横軸が設定されていません。")
            elif len(FYokoList) == 0:
                messagebox.showinfo("エラー", "縦軸が設定されていません。")
            else:
                # メッセージボックス（OK・キャンセル）

                if len(FYokoList) == len(self.control.OutColumn):
                    self.control.top.withdraw()
                    MSG = messagebox.askokcancel(
                        "確認", str(",".join(self.control.OutColumn)) + "の列名で出力します。"
                    )
                    if MSG is True:
                        ####################################################################################
                        self.control.Yoko_N = self.control.tomlTitle + "_Yoko"
                        self.control.Tate_N = self.control.tomlTitle + "_Tate"

                        FYokoList.sort()
                        FTateList.sort(key=lambda x: x[1])
                        FYokoList.extend(FTateList)

                        self.control.DB.list_to_df_replace_to_sql(
                            self.control.table_name, FYokoList
                        )
                        ####################################################################################
                        print("Line_toml保存完了")
                        OM = OCRF.Main(self)
                        if OM[0] is True:
                            MSG = messagebox.showinfo("抽出完了", str(OM[1]) + "_に保存しました。")
                        self.control.top.deiconify()
                    else:
                        messagebox.showinfo("エラー", "先頭ページの列数と設定列名の数が一致しません。再確認してください。")
                else:
                    messagebox.showinfo("確認", "縦軸数と設定列名の数が一致しません。再確認してください。")


# ---------------------------------------------------------------------------------------------
def EnterP_LineCalc(self, FList):
    """
    透過キャンバスBBOX値から罫線軸を確定
    """
    FYokoList, FTateList = [], []
    for FListItem in FList:

        if FListItem[2][0] <= 0:
            FSSC1 = 0
        else:
            FSSC1 = int(round(FListItem[2][0] / self.control.HCW, 0))

        if FListItem[2][1] <= 0:
            FSSC2 = 0
        else:
            FSSC2 = int(round(FListItem[2][1] / self.control.HCH, 0))

        if FListItem[2][2] <= 0:
            FSSC3 = 0
        else:
            if FListItem[0][5] == "Tate":
                FSSC3 = int(round(FListItem[2][2] / self.control.HCW, 0))
            else:
                FSSC3 = int(round(FListItem[2][0] / self.control.HCW, 0))

        if FListItem[2][3] <= 0:
            FSSC4 = 0
        else:
            if FListItem[0][5] == "Yoko":
                FSSC4 = int(round(FListItem[2][3] / self.control.HCH, 0))
            else:
                FSSC4 = int(round(FListItem[2][1] / self.control.HCH, 0))

        if FSSC1 < 0 and FSSC1 < self.control.model.original_width:
            FSSC1 = 0
        elif FSSC1 > self.control.model.original_width:
            FSSC1 = self.control.model.original_width
        if FSSC2 < 0 and FSSC2 < self.control.model.original_height:
            FSSC2 = 0
        elif FSSC2 > self.control.model.original_height:
            FSSC2 = self.control.model.original_height
        if FSSC3 < 0 and FSSC3 < self.control.model.original_width:
            FSSC3 = 0
        elif FSSC3 > self.control.model.original_width:
            FSSC3 = self.control.model.original_width
        if FSSC4 < 0 and FSSC4 < self.control.model.original_height:
            FSSC4 = 0
        elif FSSC4 > self.control.model.original_height:
            FSSC4 = self.control.model.original_height
        FSS = [FSSC1, FSSC2, FSSC3, FSSC4, FListItem[0][5]]
        if FListItem[0][5] == "Yoko":
            FYokoList.append(FSS)
        else:
            FTateList.append(FSS)
        print(FSS)
    return FYokoList, FTateList


# ---------------------------------------------------------------------------------------------
def unmap(self):
    """
    最上部ウィンドウを非表示
    """
    self.control.top.withdraw()


# ---------------------------------------------------------------------------------------------
def map(self):
    """
    self.topを最上部へ
    """
    self.lift()
    self.control.top.wm_deiconify()
    self.control.top.attributes("-topmost", True)
