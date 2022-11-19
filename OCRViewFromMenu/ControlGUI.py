import os
from ModelImage import ModelImage
import sqlite3 as sql
from pandas import DataFrame
import toml
from tkinter import font
from PIL import Image, ImageTk
import tkinter as tk
from Functions import dump_toml, CreateDB
from tkinter import messagebox, filedialog
from numpy import where


class ControlGUI:
    def __init__(self, root, default_path):
        """
        初期設定
        """
        # Model Class生成
        self.model = ModelImage()
        self.DB = CreateDB("LineSettingData.db")
        self.Rep_DB = CreateDB("ReplaceData.db")
        # ディスプレイサイズ
        self.width_of_window = int(int(root.winfo_screenwidth()) * 0.98)
        self.height_of_window = int(int(root.winfo_screenheight()) * 0.9)
        # ディスプレイ初期表示位置
        self.x_coodinate = 0  # self.width_of_window / 4
        self.y_coodinate = 0  # self.height_of_window / 4

        # グリッドサイズ
        self.Left_Column = int(int(root.winfo_screenwidth()) * 0.105)  # 0.105)
        self.Bottom_Column = int(int(root.winfo_screenheight()) * 0.2)
        self.SideWidth = int(self.width_of_window / 7)
        self.SideHeight = int(self.height_of_window / 90)

        # 標準ボタンサイズ
        self.Btn_width = int(self.width_of_window / 10)
        self.Btn_height = int(self.height_of_window / 70)

        # 各オブジェクト配置間隔
        self.padx = self.x_coodinate / 4
        self.pady = self.y_coodinate / 4
        # 各キャンバスサイズ
        self.FCW = int(self.width_of_window * 0.98)
        self.FCH = int(self.height_of_window * 0.75)
        # 各リサイズ比率
        self.HCW = 1
        self.HCH = 1

        # ディレクトリパス
        self.dir_path = default_path
        # 画像ファイルパス初期設定
        self.imgurl = tk.StringVar()
        if os.path.isfile(os.getcwd() + r"\OCR.png") is True:
            self.imgurl.set(os.getcwd() + r"\OCR.png")
        else:
            self.imgurl.set(os.getcwd() + r"\OCRViewFromMenu\OCR.png")
        # 初期化CSVURL
        if os.path.isfile(os.getcwd() + r"\First.csv") is True:
            self.Reset_csv = os.getcwd() + r"\First.csv"
        else:
            self.Reset_csv = os.getcwd() + r"\OCRViewFromMenu\First.csv"
        # OCR出力CCSV
        # self.OCR_outcsv = self.Reset_csv
        self.OCR_outcsv = tk.StringVar()
        self.OCR_outcsv.set(self.Reset_csv)

        # 画像ファイル名称
        self.img_name = os.path.splitext(os.path.basename(self.imgurl.get()))[0]
        self.tomlTitle = self.img_name.split(".")[0]
        # Table名
        self.table_name = f"TB_{self.tomlTitle}"
        # 画像ファイルから抽出した関与先名
        self.Kanyosaki_name = ""
        # 取扱画像ファイル指定
        self.ext_keys = [".png", ".jpg", ".jpeg", ".JPG", ".PNG", "PDF", "pdf"]

        self.target_files = []
        self.file_pos = 0
        self.file_list = ["..[select file]"]
        # tomlファイルオブジェクト
        self.tomlsetting = self.tomlread("Setting.toml")
        # LinEditGUItomlファイルオブジェクト
        self.LineEditGUISetting = self.tomlread("LineEditGUISetting.toml")
        # LinEditGUI設定をdf化
        self.LineEditGUI_df = self.toml_LGUI_todf("_ListSetting")
        self.LineEditGUI_CS__df = self.toml_LGUI_todf("_ColumnSetting")
        self.ReadDB()
        self.Toptitle = self.tomlsetting["Title"]["title"]
        self.PlusCol = "比較対象行番号"

        self.clip_sx = 0
        self.clip_sy = 0
        self.clip_ex = 0
        self.clip_ey = 0

        self.DaySet = []  # 日付列番号
        self.MoneySet = []  # 金額列番号
        self.OutColumn = []  # 出力列名

        self.canvas = None
        self.DefDB_name = "OCR_DB"
        CreateDB(self.DefDB_name)
        self.btn_font = ("", 50)  # ボタンフォントサイズ
        self.t_font = (1, int(8))  # テーブルフォントサイズ

    # ----------------------------------------------------------------------------------
    def MenuCreate(self, master):
        """
        メニューバー作成
        """
        try:
            # メニューバー作成
            self.men = tk.Menu(master, background="blue", tearoff=0)
            # ファイルメニューを作成する
            self.menu_file = tk.Menu(
                self.men,
                background="blue",
            )
            self.men.add_command(
                label="ファイル", command=lambda: self.event_set_file(master._name)
            )
            # 保存メニューを作成する
            self.savemenu = tk.Menu(master, background="blue", tearoff=False)
            self.men.add_cascade(label="保存", menu=self.savemenu)
            self.savemenu.add_command(label="上書保存", command=self.event_save)
            self.savemenu.add_separator()  # 仕切り線
            # self.savemenu.add_command(label="別名保存", command=lambda: event_Searchsave(self))
            # メニューバーを画面にセット
            master.config(menu=self.men)
        except:
            print("メニューバー作成失敗")  # Log出力

    # ----------------------------------------------------------------------------------
    def event_set_folder(self):
        """
        フォルダ選択ボタンクリックイベント
        """
        self.dir_path = filedialog.askdirectory(
            title="関与先フォルダを開く",
            initialdir=r"C:\Users\もちねこ\Desktop\GitHub\RPAScript\OCRView\CompanyData\1869",
        )
        self.Kanyosaki_name = os.path.basename(self.dir_path)
        self.entry_dir.insert(0, self.dir_path)
        self.file_list = self.SetDirlist(self.dir_path)
        self.combo_file.configure(values=self.file_list)

    # ----------------------------------------------------------------------------------
    def event_set_file(self, name):
        """
        ファイル選択ボタンクリックイベント
        """
        # event_Searchsave(self)  # 編集履歴判定後上書き
        if name != "BOTTOM_Main":  # 呼出元がトップフレームなら閉じる
            self.top.withdraw()
        typ = [("PNG", "*.png"), ("PDF", "*.pdf")]
        self.imgurl.set(
            filedialog.askopenfilename(
                title="画像ファイルを開く", filetypes=typ, initialdir="./"
            )
        )
        self.dir_path = os.path.dirname(self.imgurl.get())
        self.img_name = os.path.basename(self.imgurl.get())
        self.tomlTitle = self.img_name.split(".")[0]
        self.table_name = f"TB_{self.tomlTitle}"
        self.file_list = self.SetDirlist(self.dir_path)

        if (
            ".PDF" == os.path.splitext(os.path.basename(self.img_name))[1]
            or ".pdf" == os.path.splitext(os.path.basename(self.img_name))[1]
        ):
            msg = messagebox.askokcancel(
                "確認", "PDFが選択されています。PNGに変換しますか？\n10ページ以上の処理は処理時間が長時間になる可能性があります。"
            )
            if msg is True:
                # プログレスバーの起動
                # PBAR = PB.Open(tk.Toplevel())  # サブWindow作成
                PBAR = ""
                spd = self.pdf_image(self.img_name, "png", 300, PBAR)
                if spd is True:
                    f_r = 0
                    for f_l in self.file_list:
                        if f_l == self.img_name:
                            set_pos = f_r
                            break
                        f_r += 1
                    msg = messagebox.askokcancel("確認", "PNG変換完了しました。")
                    self.DrawImage("set", set_pos=set_pos)
                else:
                    f_r = 0
                    for f_l in self.file_list:
                        if f_l == self.img_name:
                            set_pos = f_r
                            break
                        f_r += 1
                    msg = messagebox.askokcancel(
                        "確認", "PNG変換に失敗しました。指定DPIが高すぎる可能性があります。"
                    )
                    self.DrawImage("set", set_pos=set_pos)
        else:
            f_r = 0
            for f_l in self.file_list:
                if f_l == self.img_name:
                    set_pos = f_r
                    break
                f_r += 1
            self.DrawImage("set", set_pos=set_pos)

        if name != "BOTTOM_Main":  # 呼出元がトップフレームなら開く
            self.top.deiconify()

    # ------------------------------------------------------------------------------------
    def Transparent_Create(self, master):
        """
        透過キャンバス(上ウィンドウ)に罫線描画処理
        """
        # .create_line(Ⅹ座標（始点）, Ｙ座標（始点）,Ⅹ座標（終点）, Ｙ座標（終点）)
        self.AllLineDelete(master)
        BtagsList = []
        self.tagsList = []
        ri = 0
        for readcsv1Item in self.YokoList:
            ri += 1
            ripar0, ripar1, ripar2, ripar3 = self.Zero_Check(readcsv1Item)
            master.TName = "Line" + str(ri)
            try:
                self.top.forward.dtag(master.TName, master.TName)
            except:
                print("dtagErr")
            self.top.forward.create_line(
                ripar0,
                ripar1,
                ripar2,
                ripar3,
                tags=master.TName,
                width=7,
                fill="#FF0000",
                activefill="#DBDD6F",
            )
            self.top.forward.tag_bind(master.TName, "<ButtonPress-1>", master.click1)
            self.top.forward.tag_bind(
                master.TName, "<Control-Double-1>", master.EventDelete
            )
            self.top.forward.tag_bind(master.TName, "<B1-Motion>", master.drag1)

            self.top.forward.place(x=0, y=0)
            BtagsList.append([master.TName, ripar0, ripar1, ripar2, ripar3, "Yoko"])
        for readcsv2Item in self.TateList:
            ri += 1
            ripar0, ripar1, ripar2, ripar3 = self.Zero_Check(readcsv2Item)
            master.TName = "Line" + str(ri)
            self.top.forward.create_line(
                ripar0,
                ripar1,
                ripar2,
                ripar3,
                tags=master.TName,
                width=7,
                fill="#00FF40",
                activefill="#DBDD6F",
            )
            self.top.forward.tag_bind(master.TName, "<ButtonPress-1>", master.click1)
            self.top.forward.tag_bind(
                master.TName, "<Control-Double-1>", master.EventDelete
            )
            self.top.forward.tag_bind(master.TName, "<B1-Motion>", master.drag1)

            self.top.forward.place(x=0, y=0)
            BtagsList.append([master.TName, ripar0, ripar1, ripar2, ripar3, "Tate"])
        TL = len(BtagsList)
        for TTL in range(TL):
            tagsListItem = BtagsList[TTL]
            BB = self.top.forward.bbox(tagsListItem[0])
            BSS = [
                tagsListItem[1] - BB[0],
                tagsListItem[2] - BB[1],
                tagsListItem[3] - BB[2],
                tagsListItem[4] - BB[3],
            ]
            self.tagsList.append([tagsListItem, BSS])
        return

    # ------------------------------------------------------------------------------------
    def Zero_Check(self, readcsv1Item):
        """
        軸値が0なら1に
        """
        ripar0 = round(readcsv1Item[0] * self.HCW, 0)  # * CHh
        if ripar0 == 0:
            ripar0 = 1
        ripar1 = round(readcsv1Item[1] * self.HCH, 0)  # * CWw
        if ripar1 == 0:
            ripar1 = 1
        ripar2 = round(readcsv1Item[2] * self.HCW, 0)  # * CHh
        if ripar2 == 0:
            ripar2 = 1
        ripar3 = round(readcsv1Item[3] * self.HCH, 0)  # * CWw
        if ripar3 == 0:
            ripar3 = 1
        return ripar0, ripar1, ripar2, ripar3

    # ----------------------------------------------------------------------------------
    def AllLineDelete(self, selfC):
        """
        選択直線の削除
        """
        try:
            r = len(self.tagsList) - 1
            self.top.forward.delete("all")
            for tagsListItem in reversed(self.tagsList):
                self.top.forward.delete(tagsListItem[0][0])
                self.tagsList.pop(r)
                r -= 1
            return
        except:
            return

    # ----------------------------------------------------------------------------------
    def event_save(self):
        """
        Saveボタンクリックイベント
        """
        try:
            if self.Kanyosaki_name != "":
                self.logger.debug("Saveボタン起動")  # Log出力
                # 一時保存ファイルを確認
                if self.model.stock_url != "":
                    os.remove(self.model.stock_url)
                self.Newfilename = filedialog.asksaveasfilename(
                    filetypes=[("PNG", ".png"), ("JPEG", ".jpg")]
                )
                self.SaveImage(self.Newfilename)
                self.file_list = self.SetDirlist(self.dir_path)  # ファイルリストリロード
                for F_r in range(len(self.file_list)):
                    if self.file_list[F_r] in self.Newfilename:
                        self.model.stock_url = ""
                        self.combo_file.set(self.file_list[F_r])
            else:
                messagebox.showinfo("確認", "画像ファイルが選択されていません。")
        except:
            messagebox.showinfo("確認", "画像ファイルが選択されていません。")

    # ----------------------------------------------------------------------------------
    def tomlread(self, filename):
        """
        tomlリード
        """
        try:
            r_toml = os.getcwd() + r"\\OCRViewFromMenu\\" + filename
            with open(r_toml, encoding="utf-8") as f:
                Banktoml = toml.load(f)
            if "LineEditGUISetting.toml" in filename:
                self.Linetomlurl = r_toml
            else:
                self.tomlurl = r_toml

            return Banktoml
        except:
            r_toml = os.getcwd() + r"\\" + filename
            with open(r_toml, encoding="utf-8") as f:
                Banktoml = toml.load(f)
            if "LineEditGUISetting.toml" in filename:
                self.Linetomlurl = r_toml
            else:
                self.tomlurl = r_toml

            return Banktoml

    # ----------------------------------------------------------------------------------
    def DF_to_toml(self, df, title):
        """
        df→toml
        """
        t_columns = list(df.columns)
        t_Index = list(df.index)

        # tomlファイルがない場合コピーして結合
        NewDict = {
            self.tomlTitle
            + title: {
                "Columns": str(t_columns),
                "Index": str(t_Index),
            }
        }
        r = 0
        for t_IndexItem in t_Index:
            dfseries = df.iloc[r].dropna()
            # 条件テキストボックスのリスト化---------------------------
            row_list = [str(a) for a in list(dfseries) if a != "" or a is not None]
            In_Dict = {str(t_IndexItem): row_list}
            NewDict[self.tomlTitle + title].update(In_Dict)
            r += 1

        self.LineEditGUISetting.update(NewDict)  # 辞書を結合

        dump_toml(self.LineEditGUISetting, self.Linetomlurl)  # 辞書を保存

    # ----------------------------------------------------------------------------------
    def str_to_list(self, t_str):
        t_str = (
            t_str.replace("[", "").replace("]", "").replace("'", "").replace(" ", "")
        )
        try:
            r = t_str.split(",")
            return r
        except:
            r = list(t_str)
            return r

    # ----------------------------------------------------------------------------------
    def toml_LGUI_todf(self, title):
        """
        tomlリード→df
        """
        try:
            t_columns = self.LineEditGUISetting[self.tomlTitle + title]["Columns"]
            if type(t_columns) == str:
                t_columns = self.str_to_list(t_columns)
            t_Index = self.LineEditGUISetting[self.tomlTitle + title]["Index"]
            if type(t_Index) == str:
                t_Index = self.str_to_list(t_Index)

            list = []

            for ii in t_Index:
                list_c = []
                for iii in self.LineEditGUISetting[self.tomlTitle + title][ii]:
                    list_c.append(iii)
                list.append(list_c)

            df = DataFrame(
                list,
                columns=t_columns,
                index=t_Index,
            )
            try:
                if "ListSetting" in title:
                    self.SettingTB.model.df = df
                else:
                    self.SettingTB2.model.df = df
            except:
                print("NoTable")

            return df
        except:
            Dandtitle = title.replace("_", "")
            if "ListSetting" in title:
                t_columns = self.LineEditGUISetting[Dandtitle]["Columns"]
            else:
                t_columns = ["列名"]
            if type(t_columns) == str:
                t_columns = self.str_to_list(t_columns)

            t_Index = self.LineEditGUISetting[Dandtitle]["Index"]
            if type(t_Index) == str:
                t_Index = self.str_to_list(t_Index)

            list = []

            for ii in t_Index:
                list_c = []
                for iii in self.LineEditGUISetting[Dandtitle][ii]:
                    list_c.append(iii)
                list.append(list_c)

            # DF化
            df = DataFrame(
                list,
                columns=t_columns,
                index=t_Index,
            )
            try:
                if "ListSetting" in title:
                    self.SettingTB.model.df = df
                else:
                    self.SettingTB2.model.df = df
            except:
                print("NoTable")

            self.DF_to_toml(df, title)
            return df

    # ----------------------------------------------------------------------------------
    def ReadDB(self):
        """
        tomlからtoml線軸リストを取得
        """

        try:
            self.DB.readsql_to_df(self.table_name)
            asdf = self.DB.df[["x1", "y1", "x2", "y2"]].astype("int")
            self.YokoList = list(
                asdf.values[where(self.DB.df.values[:, 5] == "Yoko")].tolist()
            )
            self.TateList = list(
                asdf.values[where(self.DB.df.values[:, 5] == "Tate")].tolist()
            )
        except:
            self.DB.readsql_to_df("OCR")

            self.YokoList = list(
                self.DB.df.values[where(self.DB.df.values[:, 4] == "Yoko")]
            )
            self.TateList = list(
                self.DB.df.values[where(self.DB.df.values[:, 4] == "Tate")]
            )

    # ----------------------------------------------------------------------------------
    def is_target(self, name, key_list):
        """
        self.ext_keysで指定した拡張子のみリスト化
        """
        valid = False
        for ks in key_list:
            if ks in name:
                valid = True

        return valid

    # ----------------------------------------------------------------------------------
    def get_file(self, command, set_pos=-1):
        """
        画像プレビュー機能の設定
        """
        if command == "prev":
            self.file_pos = self.file_pos - 1
        elif command == "next":
            self.file_pos = self.file_pos + 1
        elif command == "set":
            self.file_pos = set_pos
        else:  # current
            self.file_pos = self.file_pos

        num = len(self.target_files)
        if self.file_pos < 0:
            self.file_pos = num - 1

        elif self.file_pos >= num:
            self.file_pos = 0
        cur_file = os.path.join(self.dir_path, self.target_files[self.file_pos])
        print("{}/{} {} ".format(self.file_pos, num - 1, cur_file))
        return cur_file

    # Public

    # ----------------------------------------------------------------------------------
    def SetDirlist(self, dir_path):
        """
        フォルダー内画像ファイルをリスト化
        """
        self.dir_path = dir_path
        self.target_files = []

        file_list = os.listdir(self.dir_path)
        for fname in file_list:
            if self.is_target(fname, self.ext_keys):
                self.target_files.append(fname)
                print(fname)

        self.file_pos = 0
        if len(self.target_files) > 0:
            cur_file = self.get_file("current")
            print(cur_file)

        return self.target_files

    # ----------------------------------------------------------------------------------
    def SetCanvas(self, window_canvas):
        """
        キャンバス配置
        """
        self.canvas = window_canvas

    # ----------------------------------------------------------------------------------
    def DrawImage(self, command, set_pos=-1):
        """
        キャンバスに画像を読込む
        """
        try:
            fname = self.get_file(command, set_pos)
            self.Yoko_N = self.tomlTitle + "_Yoko"
            self.Tate_N = self.tomlTitle + "_Tate"
            if command == "Map":
                self.model.DrawImage(fname, self.canvas, "Map")
                self.ImportIMG()
                self.ImportIMG_readtoml()
                self.ReadDB()
                self.Transparent_Create(self.App)
            else:
                self.model.DrawImage(fname, self.canvas, "None")
                self.ImportIMG()
                self.ImportIMG_readtoml()
                self.ReadDB()
                self.Transparent_Create(self.App)
            return self.file_pos, self.model
        except:
            print("DrawImageSkip")

    # ----------------------------------------------------------------------------------
    def ImportIMG(self):
        """
        LinEditGUI下ウィンドウに画像をリサイズして配置
        """
        self.img = Image.open(self.imgurl.get())
        print(self.back.winfo_width())
        print(self.back.winfo_height())

        if self.back.winfo_width() >= 50:
            self.FCW = self.back.winfo_width()
            self.FCH = self.back.winfo_height()

        self.HCW = self.back.winfo_width() / self.img.width  # 幅リサイズ比率
        self.HCH = self.back.winfo_height() / self.img.height  # 高さリサイズ比率

        self.img = self.img.resize((self.FCW, self.FCH))  # 画像リサイズ

        self.TkPhoto = ImageTk.PhotoImage(
            self.img, master=self.back
        )  # 下Windowに表示する画像オブジェクト
        self.back.create_image(
            0, 0, image=self.TkPhoto, anchor=tk.NW
        )  # 下Windowのキャンバスに画像挿入

    # ----------------------------------------------------------------------------------
    def ImportIMG_readtoml(self):
        """
        LinEditGUI下ウィンドウに画像をリサイズして配置
        """
        self.Kanyosaki_name = os.path.basename(self.dir_path)
        self.tomlTitle = self.img_name.split(".")[0]
        self.table_name = f"TB_{self.tomlTitle}"
        self.toml_LGUI_todf("_ListSetting")
        self.toml_LGUI_todf("_ColumnSetting")

    # ----------------------------------------------------------------------------------

    def pdf_image(self, pdf_file, fmtt, dpi, PBAR):
        mpd = self.model.pdf_image(pdf_file, fmtt, dpi, PBAR)
        if mpd is True:
            return True
        else:
            return False

    # ----------------------------------------------------------------------------------
    def MenuFuncRun(self, command, whlist, set_pos=-1):
        """
        menuボタンクリック
        """
        try:
            fname = self.get_file(command, set_pos)
        except:
            fname = ""
        if fname == "":
            return "画像無"
        else:
            try:
                # 線形検出パラメータ設定########################################
                disth = 1.41421356
                canth1 = 50.0
                canth2 = 50.0
                casize = 3
                do = True
                # ############################################################
                if command == "Noise":
                    limg = self.model.TotalNoise(fname, 7)
                    fname = limg.filename
                    self.model.stock_url = limg.filename
                # elif command == "LineLotate":
                #     limg = self.model.ImageLotate(
                #         fname, disth, canth1, canth2, casize, do
                #     )
                #     fname = limg.filename
                #     self.model.stock_url = limg.filename
                elif command == "Resize":
                    limg = self.model.edit_img
                    fname = limg.filename
                    self.model.stock_url = limg.filename
                elif command == "LineDelete":
                    disth = whlist
                    limg = self.model.StraightLineErase(
                        fname, disth, canth1, canth2, casize, do
                    )
                    fname = limg.filename
                    self.model.stock_url = limg.filename
                # -----------------------------------------------------------
                self.model.edit_img = limg
                args = {}
                self.model.DrawImage(fname, self.canvas, command, args=args)
                return "完了"
            except:
                return "Err"

    # ----------------------------------------------------------------------------------
    # def ResizeRun(self, command, set_pos=-1):
    #     """
    #     resizeボタンクリック
    #     """
    #     fname = self.get_file(command, set_pos)

    # ----------------------------------------------------------------------------------
    def DrawRectangle(self, command, pos_y, pos_x):
        """
        キャンバス画像クリックで範囲指定完了後
        """
        if command == "clip_start":
            self.clip_sy, self.clip_sx = pos_y, pos_x
            self.clip_ey, self.clip_ex = pos_y + 1, pos_x + 1

        elif command == "clip_keep":
            self.clip_ey, self.clip_ex = pos_y, pos_x

        elif command == "clip_end":
            self.clip_ey, self.clip_ex = pos_y, pos_x
            self.clip_sy, self.clip_sx = self.model.GetValidPos(
                self.clip_sy, self.clip_sx
            )
            self.clip_ey, self.clip_ex = self.model.GetValidPos(
                self.clip_ey, self.clip_ex
            )

        self.model.DrawRectangle(
            self.canvas, self.clip_sy, self.clip_sx, self.clip_ey, self.clip_ex
        )

    # ----------------------------------------------------------------------------------
    def EditImage(self, command):
        """
        画像トリミング
        """
        args = {}
        if command == "clip_done" or command == "clip_Erace":  # トリミング確定ボタンが押されたら
            # キャンバスサイズと表示画像サイズの比率を算出---------------------------
            CWiPar = self.model.canvas_w / self.model.resize_w  # 幅
            CHePar = self.model.canvas_h / self.model.resize_h  # 高さ
            # --------------------------------------------------------------------
            # キャンバスサイズと元画像サイズの比率を算出---------------------------
            WiPar = self.model.original_width / self.model.canvas_w
            HePar = self.model.original_height / self.model.canvas_h
            # --------------------------------------------------------------------
            if CWiPar < 1:  # 幅が圧縮されていたら
                minus = ["width", CWiPar]
            elif CHePar < 1:  # 高さが圧縮されていたら
                minus = ["height", CHePar]
            else:  # 比率変更なしの場合(キャンバスと表示画像サイズが一致)
                minus = ["Nothing", 0]
            # --------------------------------------------------------------------
            if minus[0] == "width":  # 幅が圧縮されていたら
                # 幅圧縮率を高さにかける
                IMGSize = [
                    int(self.model.resize_w),
                    int(self.model.resize_h * CWiPar),
                ]
                SXPOS = 0  # スタート幅ポジション
                SYPOS = (self.model.canvas_h - IMGSize[1]) / 2  # スタート高さポジション
                sx = int(((self.clip_sx - SXPOS) / CHePar) * WiPar)
                sy = int(((self.clip_sy - SYPOS) / CWiPar) * HePar)
                ex = int(((self.clip_ex - SXPOS) / CHePar) * WiPar)
                ey = int(((self.clip_ey - SYPOS) / CWiPar) * HePar)
            elif minus[0] == "height":  # 高さが圧縮されていたら
                # 高さ圧縮率を幅にかける
                IMGSize = [
                    int(self.model.resize_w * CHePar),
                    int(self.model.resize_h),
                ]
                SXPOS = (self.model.canvas_w - IMGSize[0]) / 2  # スタート幅ポジション
                SYPOS = 0  # スタート高さポジション
                sx = int(((self.clip_sx - SXPOS) / CHePar) * WiPar)
                sy = int(((self.clip_sy - SYPOS) / CWiPar) * HePar)
                ex = int(((self.clip_ex - SXPOS) / CHePar) * WiPar)
                ey = int(((self.clip_ey - SYPOS) / CWiPar) * HePar)
            else:
                IMGSize = [
                    int(self.model.resize_w),
                    int(self.model.resize_h),
                ]
                SXPOS = (self.model.canvas_w - IMGSize[0]) / 2  # スタート幅ポジション
                SYPOS = (self.model.canvas_h - IMGSize[1]) / 2  # スタート高さポジション
                sx = int(((self.clip_sx - SXPOS) * CWiPar) * WiPar)
                sy = int(((self.clip_sy - SYPOS) * CHePar) * HePar)
                ex = int(((self.clip_ex - SXPOS) * CWiPar) * WiPar)
                ey = int(((self.clip_ey - SYPOS) * CHePar) * HePar)

            # 元画像と比較してポジション調整-------------------------------------------

            if sx < 0:
                sx = 0
            elif sx > self.model.original_width:
                sx = self.model.original_width
            if ex < 0:
                ex = 0
            elif ex > self.model.original_width:
                ex = self.model.original_width
            if sy < 0:
                sy = 0
            elif sy > self.model.original_height:
                sy = self.model.original_height
            if ey < 0:
                ey = 0
            elif ey > self.model.original_height:
                ey = self.model.original_height
            # --------------------------------------------------------------------
            # WiPar = self.model.original_width / self.model.resize_w
            # HePar = self.model.original_height / self.model.resize_h
            args["sx"], args["sy"] = sx, sy
            args["ex"], args["ey"] = ex, ey
            # args["sx"], args["sy"] = self.clip_sx, self.clip_sy
            # args["ex"], args["ey"] = self.clip_ex, self.clip_ey

        fname = self.get_file("current")
        self.model.DrawImage(fname, self.canvas, command, args=args)

    # ----------------------------------------------------------------------------------
    def SaveImage(self, fname):
        """
        画像ファイル名日付追加保存
        """

        self.model.SaveImage(fname)

    # ----------------------------------------------------------------------------------
    def OverSaveImage(self):
        """
        画像上書き保存
        """
        fname = self.get_file("current")
        self.model.OverSaveImage(fname)

    # ----------------------------------------------------------------------------------
    def UndoImage(self, command):
        """
        画像編集復元
        """
        fname = self.get_file("current")
        self.model.DrawImage(fname, self.canvas, command)

    # ----------------------------------------------------------------------------------
