import tkinter as tk
from tkinter import ttk
import numpy as np
import WarekiHenkan as wh
import pandas as pd
import re
import logging.config
import toml
import os
import IconCode
import customtkinter as ck
import ImageViewer

from difflib import SequenceMatcher
from mojimoji import han_to_zen
import P_Table_btn
from csv import QUOTE_NONNUMERIC
import Functions
import MyTable as MT
from pandastable import config

###################################################################################################
# class Application(tk.Frame):
class Application(tk.Frame):
    def __init__(self, master, control):
        super().__init__(master)
        # コントロール
        self.control = control
        # ルートウィンドウ#########################################################################
        self.control.P_Table_root = tk.Frame(
            self,
            # bg="#60cad1",
            bg="black",
            relief=tk.GROOVE,
            bd=1,
            height=self.control.height_of_window,
            width=self.control.width_of_window,
        )
        # ルートフレームの行列制限
        self.control.P_Table_root.grid_rowconfigure(2, weight=1)
        self.control.P_Table_root.grid_columnconfigure(2, weight=1)

        self.control.P_Table_root.pack(fill=tk.BOTH, expand=True)
        # トップフレーム
        self.Top_Frame = tk.Frame(
            self.control.P_Table_root,
            # bg="#60cad1",
            bg="black",
            relief=tk.GROOVE,
            bd=1,
            height=int(self.control.height_of_window / 2),
            width=self.control.width_of_window,
        )
        self.Top_Frame.pack(fill=tk.BOTH, expand=True)

        self.OCR_Table = self.SetTable("OCR抽出表")
        self.OCR_Table.pack(side=tk.LEFT, fill=tk.BOTH, expand=True)
        # self.OCR_Table.grid(row=0, column=0, sticky=tk.NSEW)
        self.pt1 = self.OCR_Table.children["!frame"].children["!mytable"]
        self.pt1._name = "OCR抽出表"

        self.DIFF_Table = self.SetTable("比較表")
        # self.DIFF_Table.grid(row=0, column=1, sticky=tk.NSEW)
        self.DIFF_Table.pack(side=tk.RIGHT, fill=tk.BOTH, expand=True)
        self.pt2 = self.DIFF_Table.children["!frame"].children["!mytable"]
        self.pt2._name = "比較表"

        # ボトムフレーム
        self.Bottom_Frame = P_Table_btn.CreateBOTTOM_Frame(self)
        self.Bottom_Frame.pack(fill=tk.BOTH, expand=True)
        # self.Bottom_Frame.grid(row=1, column=0, columnspan=2, sticky=tk.NSEW)

        self.pt1_OpenFlag = True
        self.pt2_OpenFlag = False
        self.select_var.set(1)  # select_var変数に数値をセット

    def SetTable(self, t_title) -> tk.Frame:
        """
        テーブルフレーム
        """
        Table_Frame = tk.Frame(
            master=self.Top_Frame,
            width=int(self.control.width_of_window / 2)
            - int(self.control.SideWidth / 2),
            height=int(self.control.height_of_window / 2),
        )
        # tk.Label(Table_Frame, text=t_title, bg="#fce4d2").grid(
        #     row=0, column=0, sticky=tk.W + tk.E
        # )
        tk.Label(Table_Frame, text=t_title, bg="#fce4d2").pack(
            fill=tk.BOTH, expand=True
        )
        Table_Sub_Frame = tk.Frame(
            master=Table_Frame,
            width=int(self.control.width_of_window / 2)
            - int(self.control.SideWidth / 2),
            height=int(self.control.height_of_window / 2),
        )

        Table = MT.MyTable(
            Table_Sub_Frame,
            width=int(self.control.width_of_window / 2)
            - int(self.control.SideWidth / 2),
            height=int(self.control.height_of_window / 2),
            sticky=tk.NSEW,
            control=self.control,
        )  # テーブルをサブクラス化
        Table.importCSV(self.control.Reset_csv, encoding="cp932")
        Table.show()
        options = {"fontsize": self.control.t_font[1]}
        config.apply_options(options, Table)
        # Table_Sub_Frame.grid(row=1, column=0, sticky=tk.NSEW)
        Table_Sub_Frame.pack(fill=tk.BOTH, expand=True)

        return Table_Frame
        # df変換

        # P_Table_btn.CreateFrame(self)  # フレーム作成

    # 以下関数----------------------------------------------------------------------
    def OutMoneyClick(self):
        """
        出金列指定
        """
        C_n = self.control.activetable_column
        self.OMtxt.delete(0, tk.END)
        self.OMtxt.insert(0, C_n)

    # -------------------------------------------------------------------------------------
    def InMoneyClick(self):
        """
        入金列指定
        """
        C_n = self.control.activetable_column
        self.IMtxt.delete(0, tk.END)
        self.IMtxt.insert(0, C_n)

    # -------------------------------------------------------------------------------------
    def DSSetClick(self):
        """
        日付列指定
        """
        C_n = self.control.activetable_column
        self.DStxt.delete(0, tk.END)
        self.DStxt.insert(0, C_n)

    # ----------------------------------------------------------------------
    def TableSave(self):
        enc = Functions.getFileEncoding(self.FileName)
        self.pt1.model.df.to_csv(
            self.control.OCR_outcsv,
            index=False,
            encoding=enc,
            quoting=QUOTE_NONNUMERIC,
        )

    def chk_click(self, pt_bln):
        """
        チェックボックス切替
        """
        print(pt_bln.get())
        if pt_bln.get() is True:
            pt_bln.set(False)
        else:
            pt_bln.set(True)

    # ----------------------------------------------------------------------
    def JournalView(self):
        """
        仕訳フレーム起動
        """
        try:
            self.master.withdraw()
            self.AJset = os.path.dirname(self.FileName) + r"\AJSet.csv"
            DG.Main(
                self,
                self.master,
                self.FileName,
                self.AJ_u,
                self.AJset,
                "",
                self.changetxturl,
                self.Banktoml,
                self.BanktomlUrl,
            )
        except:
            tk.messagebox.showinfo("確認", " 仕訳検索フレーム起動エラーです。")

    # ----------------------------------------------------------------------
    def ReadRepView(self):
        """
        置換フレーム起動
        """
        try:
            # m = self.children_get()
            m.ColumnHeader = ["変更前", "変更後"]
            self.RView.destroy()
            self.RView = ReplaceView.Main(
                self, self.FileName, self.OCR_tbname
            )  # 置換テーブルの読込
            # ReplaceView.CreateDB.readsql(self, self.OCR_dbname, self.OCR_tbname, m)
            self.RView.update()
        except:
            tk.messagebox.showinfo("確認", " 置換フレーム起動エラーです。")

    # ----------------------------------------------------------------------
    def children_get(self):
        """
        置換フレームからテーブル取得
        """
        try:
            m = self.RView
            m = m.children["!frame"]
            m = m.children["!frame2"]
            m = m.children["!mytablesql"]
            m.ColumnHeader = ["変更前", "変更後"]
            return m
        except:
            return False

    # -------------------------------------------------------------------------------------
    def ReadImg(self):
        """
        画像フレーム起動
        """
        try:
            if self.Img_c != 1:
                self.OCR_frame2.pack_forget()
                self.IMG_frame.pack(side=tk.LEFT, fill=tk.BOTH, expand=True)
                try:
                    print(self.IView.master)
                except:
                    self.IView = ImageViewer.call(self.imgurl, self.IMG_frame)
                self.Img_c = 1
            else:
                self.IMG_frame.pack_forget()
                self.OCR_frame2.pack(side=tk.LEFT, fill=tk.BOTH, expand=True)
                self.Img_c = 0
        except:
            tk.messagebox.showinfo("確認", " 画像フレーム起動エラーです。")

    # -------------------------------------------------------------------------------------
    def DifftxtCol(self, event):
        """
        OCR列名更新
        """
        ColList = self.Diff_col.get().split(",")
        if len(self.pt2.model.df.columns) == len(ColList):
            self.pt2.model.df.columns = ColList
            Functions.Pandas_mem_usage(self.pt2.model.df)
            self.pt2.show()
        else:
            tk.messagebox.showinfo("確認", "指定列名数と比較表の列数が一致しません。再確認してください。")

    # -------------------------------------------------------------------------------------
    def OCRtxtCol(self, event):
        """
        OCR列名更新
        """
        ColList = self.OCR_col.get().split(",")
        self.ColumnsDelete(self.pt1)
        if len(self.pt1.model.df.columns) == len(ColList):
            self.pt1.model.df.columns = ColList
            Functions.Pandas_mem_usage(self.pt1.model.df)
            self.pt1.show()
        else:
            tk.messagebox.showinfo("確認", "指定列名数とOCR表の列数が一致しません。再確認してください。")

    # -------------------------------------------------------------------------------------
    def Extract_Character_column(self, pt, col):
        """
        金額列の数値・文字列分割
        """
        df = pt.df
        df = df.fillna("")

        ptCol = np.array(df.columns)
        col = np.where(ptCol == col)
        # 対象列スライス
        ptIn = df.values[:, col]

        for r in range(ptIn.shape[0]):
            txt = str(ptIn[r])
            txt = txt.replace("[['", "").replace("']]", "")

            re_txt = re.sub(r"\D", "", txt)
            if re_txt != "":
                # 文字列から数字を抽出して分割
                ptIn[r] = re_txt
                if self.ExtractColumn[r] == "":
                    for rt in re_txt:
                        txt = txt.replace(rt, "")
                    self.ExtractColumn[r] = txt
                else:
                    for rt in re_txt:
                        txt = txt.replace(rt, "")
                    self.ExtractColumn[r] = self.ExtractColumn[r] + "," + txt
            else:
                ptIn[r] = ""
                for rt in re_txt:
                    txt = txt.replace(rt, "")
                self.ExtractColumn[r] = txt
        df.values[:, col] = ptIn

        return df

    # -------------------------------------------------------------------------------------
    def DaysCheck(self, pt):
        """
        日付列の形式を揃える
        """
        try:
            ptCol = np.array(pt.model.df.columns)
            Day_col = np.where(ptCol == self.DStxt.get())
            ptDay = np.array(pt.model.df)[:, Day_col]

            for r in range(ptDay.shape[0]):
                txt = self.ChangeD_Txt(str(ptDay[r]))
                if txt[0] is True:
                    ptDay[r] = txt[1]
            pt = np.array(pt.model.df)
            pt[:, Day_col] = ptDay
            pt = pd.DataFrame(pt, columns=ptCol)
            Functions.Pandas_mem_usage(pt)
            # self.pt1.show()
            return pt
        except:
            tk.messagebox.showinfo("確認", "日付列の書式整理エラーです。")

    # -------------------------------------------------------------------------------------
    def ChangeList(self):
        """
        データ整理分岐処理
        """

        if self.DStxt.get() == "":
            msg = tk.messagebox.askokcancel("確認", "日付列名が未設定です。実行しますか？")
            if msg is False:
                tk.messagebox.showinfo("確認", "処理を中断します。")
                return False
        if self.OMtxt.get() == "":
            msg = tk.messagebox.askokcancel("確認", "出金列名が未設定です。実行しますか？")
            if msg is False:
                tk.messagebox.showinfo("確認", "処理を中断します。")
                return False
        if self.IMtxt.get() == "":
            msg = tk.messagebox.askokcancel("確認", "入金列名が未設定です。実行しますか？")
            if msg is False:
                tk.messagebox.showinfo("確認", "処理を中断します。")
                return False
        try:
            # m = self.children_get()
            self.control.Rep_DB.readsql_to_df(self.control.table_name)
            # self.RView_df = m.model.df
        except:
            self.control.Rep_DB.replaceText_to_sql(
                self.control.table_name, [["TEST", "TEST"]]
            )
            tk.messagebox.showinfo("確認", " 置換フレーム起動エラーです。")

        self.ChangeList_sub()

        return True

    # -------------------------------------------------------------------------------------
    def ChangeList_sub(self):
        # 日付列処理
        if self.DStxt.get() != "":
            if self.pt2_OpenFlag is True:
                self.pt1.df = self.DaysCheck(self.pt1)
                self.pt2.df = self.DaysCheck(self.pt2)
            else:
                self.pt1.df = self.DaysCheck(self.pt1)
        # 出金列処理
        if self.OMtxt.get() != "":
            if self.pt2_OpenFlag is True:
                self.ExtractColumn = np.full(self.pt1.df.shape[0], "")  # 分割文字列リスト
                self.pt1.df = self.Extract_Character_column(self.pt1, self.OMtxt.get())
                self.ExtractColumn = np.full(self.pt2.df.shape[0], "")  # 分割文字列リスト
                self.pt2.df = self.Extract_Character_column(self.pt2, self.OMtxt.get())
            else:
                self.ExtractColumn = np.full(self.pt1.df.shape[0], "")  # 分割文字列リスト
                self.pt1.df = self.Extract_Character_column(self.pt1, self.OMtxt.get())
        # 入金列処理
        if self.IMtxt.get() != "":
            if self.pt2_OpenFlag is True:
                self.ExtractColumn = np.full(self.pt1.df.shape[0], "")  # 分割文字列リスト
                self.pt1.df = self.InMCheck(self.pt1)
                self.ExtractColumn = np.full(self.pt2.df.shape[0], "")  # 分割文字列リスト
                self.pt2.df = self.InMCheck(self.pt2)
            else:
                self.ExtractColumn = np.full(self.pt1.df.shape[0], "")  # 分割文字列リスト
                self.pt1.df = self.InMCheck(self.pt1)

    # ----------------------------------------------------------------------------
    def ChangeD_Txt(self, Txt):
        """
        日付西暦和暦変換
        """
        try:
            TxtSP = re.findall(r"\d+", Txt)
            Y_key = Txt
            for TxtSPItem in TxtSP:
                Y_key = Y_key.replace(TxtSPItem, "")
            code_regex = re.compile(
                "[!\"#$%&'\\\\()*+,-./:;<=>?@[\\]^_`{|}~「」〔〕“”〈〉『』【】＆＊・（）＄＃＠。、？！｀＋￥％]"
            )
            Y_key = code_regex.sub("", Y_key)
            T_Nen = len(TxtSP[0])
            if T_Nen <= 2:
                if Y_key != "":
                    if Y_key[0] == "H" or Y_key[0] == "h":
                        D_strYear = "平成"
                    elif Y_key[0] == "S" or Y_key[0] == "s":
                        D_strYear = "昭和"
                    else:
                        D_strYear = "令和"
                else:
                    D_strYear = "令和"
                print("和暦")
                D_str = (
                    D_strYear
                    + str(TxtSP[0].zfill(2))
                    + "年"
                    + str(TxtSP[1].zfill(2))
                    + "月"
                    + str(TxtSP[2].zfill(2))
                    + "日"
                )
                D_str = wh.SeirekiSTRDate(D_str)
            elif T_Nen <= 4:
                print("西暦")
                D_str = TxtSP[0] + "/" + TxtSP[1].zfill(2) + "/" + TxtSP[2].zfill(2)
            else:
                print("西暦")
            return True, D_str
        except:
            return False, ""

    # ---------------------------------------------------------------------
    def EntrySelect(self, pt, r):
        """
        Entry選択
        """
        try:
            pt.setSelectedRow(r)
            pt.setSelectedCol(0)
            pt.drawSelectedRect(r, 0)
            pt.drawSelectedRow()
            x, y = pt.getCanvasPos(pt.currentrow, pt.currentcol - 1)
            rmin = pt.visiblerows[0]
            rmax = pt.visiblerows[-1] - 2
            cmax = pt.visiblecols[-1] - 1
            cmin = pt.visiblecols[0]
            FirstPos = pt.currentrow

            if x is None:
                return

            if pt.currentcol > cmax or pt.currentcol <= cmin:
                pt.xview("moveto", x)
                pt.colheader.xview("moveto", x)
                pt.redraw()

            if pt.currentrow < rmin and FirstPos == 0:
                vh = len(pt.visiblerows) / 2
                x, y = pt.getCanvasPos(pt.currentrow - vh, 0)

            if pt.currentrow >= rmax or pt.currentrow <= rmin:
                pt.yview("moveto", y)
                pt.rowheader.yview("moveto", y)
                pt.redraw()

            pt.drawSelectedRect(pt.currentrow, pt.currentcol)
            # coltype = pt.model.getColumnType(pt.currentcol)
            return

        # ---------------------------------------------------------------------

        except:
            tk.messagebox.showinfo("確認", "表選択操作に失敗しました。")

    # ---------------------------------------------------------------------
    def SingleSearchStart(self):
        """
        単一通帳整理
        """
        try:
            CL = self.ChangeList()
            if CL is True:
                self.SinglePtSearch()
        except:
            tk.messagebox.showinfo("確認", "比較表が指定されていません。")

    # ---------------------------------------------------------------------
    def SinglePtSearch(self):
        """
        検索開始
        """
        try:
            pt = np.array(self.pt1.model.df)
            ptCol = list(self.pt1.model.df.columns)
            if self.select_var.get() != 1:
                self.OutM_col = int(np.where(np.array(ptCol) == self.OMtxt.get())[0])
                self.InM_col = int(np.where(np.array(ptCol) == self.IMtxt.get())[0])
            pt2 = np.array(self.pt2.model.df)
            ptCol2 = list(self.pt2.model.df.columns)
            if self.select_var.get() != 1:
                self.OutM_col2 = int(np.where(np.array(ptCol2) == self.OMtxt.get())[0])
                self.InM_col2 = int(np.where(np.array(ptCol2) == self.IMtxt.get())[0])
            pt_r_list = np.array(self.pt1.model.df)[:, 0]
            r = self.pt1.startrow
            if r is None:
                tk.messagebox.showinfo("確認", "検索したいOCR抽出表のセルを選択してください。")
                return
            if pt[r, self.OutM_col] == pt[r, self.OutM_col]:
                if pt[r, self.OutM_col] != "" and pt[r, self.OutM_col] != float("nan"):
                    ptstr = pt[r, self.Day_col] + pt[r, self.OutM_col]
                    for rr in range(pt2.shape[0]):
                        if pt2[rr, self.InM_col2] == pt2[rr, self.InM_col2]:
                            try:
                                pt2str = pt2[rr, self.Day_col2] + pt2[rr, self.InM_col2]
                                if ptstr == pt2str:
                                    self.EntrySelect(self.pt2, r)
                                    break
                                else:
                                    pt_r_list[r] = ""
                            except:
                                pt_r_list[r] = ""
                elif pt[r, self.InM_col] != "" and pt[r, self.InM_col] != float("nan"):
                    ptstr = pt[r, self.Day_col] + pt[r, self.InM_col]
                    for rr in range(pt2.shape[0]):
                        if pt2[rr, self.OutM_col2] == pt2[rr, self.OutM_col2]:
                            try:
                                pt2str = (
                                    pt2[rr, self.Day_col2] + pt2[rr, self.OutM_col2]
                                )
                                if ptstr == pt2str:
                                    self.EntrySelect(self.pt2, r)
                                    break
                                else:
                                    pt_r_list[r] = ""
                            except:
                                pt_r_list[r] = ""
        except:
            tk.messagebox.showinfo("確認", "比較表が指定されていません。")

    # ---------------------------------------------------------------------
    def ColumnsDelete(self, DF):
        """
        テーブル1に比較対象行番号列があるか確認
        """
        DF_Columns = DF.model.df.columns
        if (self.control.PlusCol in DF_Columns) is True:
            Col_n = int(np.where(DF_Columns == self.control.PlusCol)[0])
            npDF = np.array(DF.model.df)
            DF_Columns = DF_Columns[0:Col_n]
            npDF = npDF[:, 0:Col_n]
            Ret_DF = pd.DataFrame(npDF, columns=DF_Columns)
            DF.model.df = Ret_DF
            DF.show()

    # ---------------------------------------------------------------------
    def SearchStart(self):
        """
        検索開始
        """
        try:
            self.ColumnsDelete(self.pt1)
            if len(self.pt1.model.df.columns) == len(self.pt2.model.df.columns):
                try:
                    CL = self.ChangeList()
                    if CL is True:
                        self.PtSearch()
                except:
                    tk.messagebox.showinfo("確認", "書式整理時にエラーが発生しました。")
            else:
                tk.messagebox.showinfo("確認", "OCR抽出表と比較表の設定列数が一致しません。")
        except:
            tk.messagebox.showinfo("確認", "比較表が指定されていません。")

    # ---------------------------------------------------------------------
    def PtSearch_Sub(
        self,
        r,
        pt,
        pt2,
        pt_r_list,
    ):
        try:
            if pt[r, self.OutM_col] == pt[r, self.OutM_col]:
                if pt[r, self.OutM_col] != "" and pt[r, self.OutM_col] != float("nan"):
                    ptstr = pt[r, self.Day_col] + pt[r, self.OutM_col]
                    try:
                        for rr in range(pt2.shape[0]):
                            if pt2[rr, self.InM_col2] == pt2[rr, self.InM_col2]:
                                try:
                                    pt2str = (
                                        pt2[rr, self.Day_col2] + pt2[rr, self.InM_col2]
                                    )
                                    if ptstr == pt2str:
                                        pt_r_list[r] = rr + 1
                                        break
                                    else:
                                        pt_r_list[r] = ""
                                except:
                                    pt_r_list[r] = ""
                    except:
                        pt_r_list[r] = ""
                elif pt[r, self.InM_col] != "" and pt[r, self.InM_col] != float("nan"):
                    try:
                        ptstr = pt[r, self.Day_col] + pt[r, self.InM_col]
                        for rr in range(pt2.shape[0]):
                            if pt2[rr, self.OutM_col2] == pt2[rr, self.OutM_col2]:
                                try:
                                    pt2str = (
                                        pt2[rr, self.Day_col2] + pt2[rr, self.OutM_col2]
                                    )
                                    if ptstr == pt2str:
                                        pt_r_list[r] = rr + 1
                                        break
                                    else:
                                        pt_r_list[r] = ""
                                except:
                                    pt_r_list[r] = ""
                    except:
                        pt_r_list[r] = ""
                else:
                    pt_r_list[r] = ""
            else:
                pt_r_list[r] = ""
        except:
            pt_r_list[r] = pt_r_list[r]
            self.pt1search_F = False

    # ---------------------------------------------------------------------
    def PtSearch(self):
        """
        検索開始
        """
        try:
            pt = np.array(self.pt1.model.df)
            ptCol = list(self.pt1.model.df.columns)
            if self.select_var.get() != 1:
                self.OutM_col = int(np.where(np.array(ptCol) == self.OMtxt.get())[0])
                self.InM_col = int(np.where(np.array(ptCol) == self.IMtxt.get())[0])
            pt2 = np.array(self.pt2.model.df)
            ptCol2 = list(self.pt2.model.df.columns)
            if self.select_var.get() != 1:
                self.OutM_col2 = int(np.where(np.array(ptCol2) == self.OMtxt.get())[0])
                self.InM_col2 = int(np.where(np.array(ptCol2) == self.IMtxt.get())[0])
            pt_r_list = np.array(self.pt1.model.df)[:, 0]
            self.pt1search_F = True
            for r in range(pt.shape[0]):
                self.PtSearch_Sub(
                    r,
                    pt,
                    pt2,
                    pt_r_list,
                )
            if self.pt1search_F is False:
                if self.select_var.get() != 1:
                    tk.messagebox.showinfo("確認", "単一検索で失敗しました。\n検索設定を確認してください。")
                else:
                    tk.messagebox.showinfo("確認", "複数検索で失敗しました。\n検索設定を確認してください。")
            else:
                ptCol.append(self.control.PlusCol)
                pt_r_list = np.reshape(pt_r_list, (pt_r_list.shape[0], 1))
                pt = np.hstack([pt, pt_r_list])
                pt = pd.DataFrame(pt, columns=ptCol)
                self.pt1.model.df = pt
                Functions.Pandas_mem_usage(self.pt1.model.df)
                self.pt1.show()
        except:
            tk.messagebox.showinfo("確認", "比較表が指定されていません。")

    # -------------------------------------------------------------------------------------
    def ChangeFileSingleRead(self):
        """
        比較対象CSVの追加
        """
        fTyp = [("CSV", ".csv")]
        read_list = tk.filedialog.askopenfilename(filetypes=fTyp, initialdir="./")
        aplist = list(self.module)
        aplist.append(read_list)
        self.module = tuple(aplist)
        self.listbox_var.set(self.module)
        JCSV = Functions.JoinCSV(list(self.module))
        if JCSV[0] is True:
            self.pt2.model.df = JCSV[1]
            self.pt2.update()
            self.pt2.show()
            self.pt2_OpenFlag = True

    # -------------------------------------------------------------------------------------
    def ChangeFileRead(self):
        """
        比較対象CSVの複数追加
        """
        fTyp = [("CSV", ".csv")]
        read_list = tk.filedialog.askopenfilenames(filetypes=fTyp, initialdir="./")
        self.module = read_list
        self.listbox_var.set(self.module)
        JCSV = Functions.JoinCSV(list(self.module))
        if JCSV[0] is True:
            self.pt2.model.df = JCSV[1]
            self.pt2.update()
            self.pt2.show()
            self.pt2_OpenFlag = True

    # -------------------------------------------------------------------------------------
    def click_close(self):
        """
        ウィンドウ×ボタンクリック
        """
        if tk.messagebox.askokcancel("確認", "終了しますか？"):
            self.master.destroy()
        else:
            print("")

    # ---------------------------------------------------------------------------------------------
    def ReturnBack(self):
        """
        前UI起動
        """
        self.master.destroy()
        C_MT.deiconify()
        C_TP.deiconify()

    def OCRFileRead(self):
        try:
            # ファイル→開く
            filename = tk.filedialog.askopenfilename(
                filetypes=[
                    ("CSV", ".csv"),
                ],  # ファイルフィルタ
                initialdir=os.getcwd(),  # カレントディレクトリ
            )
            self.FileName = filename
            if filename != "":
                self.OCR_dbname = "ReplaceView.db"
                self.OCR_tbname = (
                    "TB_" + os.path.splitext(os.path.basename(self.FileName))[0]
                )
                self.OCR_fname = os.path.splitext(os.path.basename(self.FileName))[0]
                self.changetxturl = (
                    os.path.dirname(self.FileName)
                    # + r"\\"
                    # + os.path.basename(os.path.dirname(self.FileName))
                    + r"\\ChangeTxtList.csv"
                )

                self.AJ_u = (
                    os.path.dirname(self.FileName)
                    + r"\\"
                    + self.OCR_fname
                    + "_AutoJounal.csv"
                )
                enc = Functions.CSVO.getFileEncoding(self.FileName)
                self.table = self.pt1.importCSV(self.FileName, encoding=enc)
                options = {"fontsize": self.t_font[1]}
                Functions.config.apply_options(options, self.pt1)
                # DF型変換------------------------------
                Functions.Pandas_mem_usage(self.pt1.model.df)
                # --------------------------------------
                self.pt1.show()
                self.pt1.update()
                self.pt1_OpenFlag = True
                self.OCR_url.delete(0, tk.END)
                self.OCR_url.insert(0, self.FileName)
                # m = self.children_get()

                self.RView.destroy()
                self.RView = ReplaceView.Main(
                    self, self.FileName, self.OCR_tbname
                )  # 置換テーブルの読込
                # ReplaceView.CreateDB.readsql(self, self.OCR_dbname, self.OCR_tbname, m)
                self.RView.update()
        except:
            return


# ---------------------------------------------------------------------------------------------
def tomlread():
    """
    tomlリード
    """
    try:
        r_toml = os.getcwd() + r"\OCRView\Setting.toml"
        return r_toml
    except:
        r_toml = os.getcwd() + r"\Setting.toml"
        return r_toml


# -------------------------------------------------------------------------------------
def Main(MUI, US, logger, MT, TP, imgu, BT, BTURL):
    """
    呼出関数
    """
    global Master
    global G_logger, C_MT, C_TP
    global tomlurl

    Master = MUI
    C_MT = MT
    C_TP = TP
    csv_u = US
    G_logger = logger
    imgurl = imgu

    # -----------------------------------------------------------
    # root = tk.Tk()  # Window生成
    root = tk.Toplevel()  # Window生成
    # root.tk.call("wm", "iconphoto", root._w, tk.PhotoImage(data=data, master=root))
    app = Application(
        csvurl=csv_u, imgurl=imgurl, Banktoml=BT, BanktomlUrl=BTURL, master=root
    )
    # --- 基本的な表示準備 ----------------

    app.mainloop()


# ------------------------------------------------------------------------------------------
if __name__ == "__main__":
    import ControlGUI

    # -----------------------------------------------------------
    root = tk.Tk()  # Window生成
    data = IconCode.icondata()
    root.tk.call("wm", "iconphoto", root._w, tk.PhotoImage(data=data, master=root))
    control = ControlGUI.ControlGUI(root, os.getcwd())
    root.geometry("1200x700")
    frame = tk.Frame(root, width=1280, heigh=700)
    app = Application(frame, control)
    app.pack()
    # --- 基本的な表示準備 ----------------

    app.mainloop()
