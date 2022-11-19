import tkinter as tk

import os
import customtkinter as ck

LabelWidth = 80
LabelHeight = 10
BtnWidth = 80
BtnHeight = 10
EntWidth = 80
EntHeight = 10


def CreateBOTTOM_Frame(self) -> tk.Frame:
    # ボトムフレーム
    BOTTOM_Frame = tk.Frame(
        self.control.P_Table_root,
        width=int(self.control.width_of_window / 2),
        height=int(self.control.height_of_window * 0.8),
        bd=2,
        bg="#fabd91",
        relief=tk.RIDGE,
    )

    ########################################################################################
    # フレーム設定---------------------------------------------------------------------

    # BOTTOM_Sub##############################################################################
    self.BOTTOM_Sub = tk.Frame(
        BOTTOM_Frame,
        width=int(self.control.width_of_window / 4),
        height=int(self.control.height_of_window * 0.8),
        bd=2,
        bg="#fabd91",
        relief=tk.RIDGE,
    )
    self.BOTTOM_Sub.pack(side=tk.LEFT, fill=tk.BOTH, expand=True)
    # --------------------------------------------------------------------------------
    ck.CTkLabel(
        master=self.BOTTOM_Sub,
        text="日付列名",
        width=LabelWidth,
        height=LabelHeight,
        corner_radius=8,
        text_font=self.control.t_font,
    ).grid(row=0, column=0)
    self.DStxt = ck.CTkEntry(
        master=self.BOTTOM_Sub,
        width=EntWidth,
        height=EntHeight,
        border_width=2,
        corner_radius=8,
        text_color="black",
        border_color="snow",
        text_font=self.control.t_font,
    )
    self.DStxt.insert(0, "")  # 日付列名テキストボックスに文字代入
    self.DStxt.grid(row=0, column=1, pady=5, sticky=tk.W)  # 日付列名テキストボックス配置
    self.DSbtn = ck.CTkButton(
        master=self.BOTTOM_Sub,
        text="選択列名転記",
        command=self.DSSetClick,
        width=BtnWidth,
        height=BtnHeight,
        border_width=2,
        corner_radius=8,
        text_color="snow",
        border_color="snow",
        text_font=self.control.t_font,
    )
    self.DSbtn.grid(row=0, column=2, padx=5, pady=5)
    # --------------------------------------------------------------------------------
    ck.CTkLabel(
        master=self.BOTTOM_Sub,
        text="出金列名",
        width=LabelWidth,
        height=LabelHeight,
        corner_radius=8,
        text_font=self.control.t_font,
    ).grid(row=1, column=0)
    self.OMtxt = ck.CTkEntry(
        master=self.BOTTOM_Sub,
        width=EntWidth,
        height=EntHeight,
        border_width=2,
        corner_radius=8,
        text_color="black",
        border_color="snow",
        text_font=self.control.t_font,
    )
    self.OMtxt.insert(0, "")  # 出金列名テキストボックスに文字代入
    self.OMtxt.grid(row=1, column=1, pady=5, sticky=tk.W)  # 出金列名テキストボックス配置
    self.OMbtn = ck.CTkButton(
        master=self.BOTTOM_Sub,
        text="選択列名転記",
        command=self.OutMoneyClick,
        width=BtnWidth,
        height=BtnHeight,
        border_width=2,
        corner_radius=8,
        text_color="snow",
        border_color="snow",
        text_font=self.control.t_font,
    )
    self.OMbtn.grid(row=1, column=2, padx=5)
    # --------------------------------------------------------------------------------
    ck.CTkLabel(
        master=self.BOTTOM_Sub,
        text="入金列名",
        width=LabelWidth,
        height=LabelHeight,
        corner_radius=8,
        text_font=self.control.t_font,
    ).grid(row=2, column=0)
    self.IMtxt = ck.CTkEntry(
        master=self.BOTTOM_Sub,
        width=EntWidth,
        height=EntHeight,
        border_width=2,
        corner_radius=8,
        text_color="black",
        border_color="snow",
        text_font=self.control.t_font,
    )
    self.IMtxt.insert(0, "")  # 入金列名テキストボックスに文字代入
    self.IMtxt.grid(row=2, column=1, pady=5, sticky=tk.W)  # 入金列名テキストボックス配置
    self.IMbtn = ck.CTkButton(
        master=self.BOTTOM_Sub,
        text="選択列名転記",
        command=self.InMoneyClick,
        width=BtnWidth,
        height=BtnHeight,
        border_width=2,
        corner_radius=8,
        text_color="snow",
        border_color="snow",
        text_font=self.control.t_font,
    )
    self.IMbtn.grid(row=2, column=2, padx=5)
    # --------------------------------------------------------------------------------
    ck.CTkLabel(
        master=self.BOTTOM_Sub,
        text="金額列数",
        width=LabelWidth,
        height=LabelHeight,
        corner_radius=8,
        text_font=self.control.t_font,
    ).grid(row=3, column=0)
    # radio1ウィジェット
    self.select_var = tk.IntVar()  # ウィジェット変数select_varを作成
    self.languages = [("複数", 1), ("単一", 2)]  # languagesリストを定義
    for language, val in reversed(self.languages):  # ループ開始
        tk.Radiobutton(
            self.BOTTOM_Sub,
            text=language,
            value=val,
            variable=self.select_var,
            command=lambda: radioclick(self),
            bg="#fabd91",
        ).grid(row=3, column=val, sticky=tk.N)

    self.SplitVarLabel = ck.CTkLabel(
        master=self.BOTTOM_Sub,
        text="貸借判定基準列名",
        width=LabelWidth,
        height=LabelHeight,
        corner_radius=8,
        text_font=self.control.t_font,
    ).grid(row=5, column=0)
    self.SplitVar = ck.CTkEntry(
        master=self.BOTTOM_Sub,
        width=int(EntWidth * 3),
        height=EntHeight,
        border_width=2,
        corner_radius=8,
        text_color="black",
        border_color="snow",
        text_font=self.control.t_font,
    )
    self.SplitVar.delete(0, tk.END)
    self.SplitVar.insert(0, "貸借")
    self.SplitVar.configure(state="readonly")
    self.SplitVar.grid(row=5, column=1, pady=5, columnspan=2)
    self.In_vLabel = ck.CTkLabel(
        master=self.BOTTOM_Sub,
        text="入金文字列",
        width=LabelWidth,
        height=LabelHeight,
        corner_radius=8,
        text_font=self.control.t_font,
    ).grid(row=6, column=0)
    self.In_v = ck.CTkEntry(
        master=self.BOTTOM_Sub,
        width=int(EntWidth * 3),
        height=EntHeight,
        border_width=2,
        corner_radius=8,
        text_color="black",
        border_color="snow",
        text_font=self.control.t_font,
    )
    self.In_v.delete(0, tk.END)
    self.In_v.insert(0, "借")
    self.In_v.configure(state="readonly")
    self.In_v.grid(row=6, column=1, pady=5, columnspan=2)
    self.Out_vLabel = ck.CTkLabel(
        master=self.BOTTOM_Sub,
        text="出金文字列",
        width=LabelWidth,
        height=LabelHeight,
        corner_radius=8,
        text_font=self.control.t_font,
    ).grid(row=7, column=0)
    self.Out_v = ck.CTkEntry(
        master=self.BOTTOM_Sub,
        width=int(EntWidth * 3),
        height=EntHeight,
        border_width=2,
        corner_radius=8,
        text_color="black",
        border_color="snow",
        text_font=self.control.t_font,
    )
    self.Out_v.delete(0, tk.END)
    self.Out_v.insert(0, "貸")
    self.Out_v.configure(state="readonly")
    self.Out_v.grid(row=7, column=1, pady=5, columnspan=2)
    self.Money_Label = ck.CTkLabel(
        master=self.BOTTOM_Sub,
        text="金額列名",
        width=LabelWidth,
        height=LabelHeight,
        corner_radius=8,
        text_font=self.control.t_font,
    ).grid(row=8, column=0)
    self.Money_v = ck.CTkEntry(
        master=self.BOTTOM_Sub,
        width=int(EntWidth * 3),
        height=EntHeight,
        border_width=2,
        corner_radius=8,
        text_color="black",
        border_color="snow",
        text_font=self.control.t_font,
    )
    self.Money_v.delete(0, tk.END)
    self.Money_v.insert(0, "金額")
    self.Money_v.configure(state="readonly")
    self.Money_v.grid(row=8, column=1, pady=5, columnspan=2)
    # #######################################################################################
    # Side_Sub2##############################################################################
    self.BOTTOM_Sub2 = tk.Frame(
        BOTTOM_Frame,
        width=int(self.control.width_of_window / 4),
        height=int(self.control.height_of_window * 0.8),
        bd=2,
        bg="#fabd91",
        relief=tk.RIDGE,
    )
    # self.BOTTOM_Sub2.grid(row=1, column=1, sticky=tk.NSEW)
    self.BOTTOM_Sub2.pack(side=tk.LEFT, fill=tk.BOTH, expand=True)
    # 書式整理-------------------------------------------------------------------------
    self.ChangeL = ck.CTkButton(
        master=self.BOTTOM_Sub2,
        text="書式整理",
        command=self.ChangeList,
        width=BtnWidth,
        height=BtnHeight,
        border_width=2,
        corner_radius=8,
        text_color="snow",
        border_color="snow",
        fg_color="tomato",
        text_font=self.control.t_font,
    )
    self.ChangeL.grid(
        row=0, column=0, columnspan=3, padx=10, pady=5, sticky=tk.N
    )  # 日付列名テキストボックス配置
    # 置換-------------------------------------------------------------------------
    self.ChangeL = ck.CTkButton(
        master=self.BOTTOM_Sub2,
        text="置換起動",
        command=self.ReadRepView,
        width=BtnWidth,
        height=BtnHeight,
        border_width=2,
        corner_radius=8,
        text_color="snow",
        border_color="snow",
        fg_color="#78c7ff",
        text_font=self.control.t_font,
    )
    self.ChangeL.grid(
        row=1, column=0, columnspan=3, padx=10, pady=5, sticky=tk.N
    )  # 日付列名テキストボックス配置

    # OCR抽出ファイル-----------------------------------------------------------
    self.OCRRead = ck.CTkButton(
        master=self.BOTTOM_Sub2,
        text="OCR抽出ファイル選択",
        command=self.OCRFileRead,
        width=BtnWidth,
        height=BtnHeight,
        border_width=2,
        corner_radius=8,
        text_color="snow",
        border_color="snow",
        fg_color="skyblue",
        text_font=self.control.t_font,
    )
    self.OCRRead.grid(
        row=2, column=0, columnspan=3, padx=10, pady=5, sticky=tk.N
    )  # 日付列名テキストボックス配置

    # 選択テーブル上書-----------------------------------------------------------
    self.OCRRead = ck.CTkButton(
        master=self.BOTTOM_Sub2,
        text="OCR抽出ファイル上書",
        command=self.TableSave,
        width=BtnWidth,
        height=BtnHeight,
        border_width=2,
        corner_radius=8,
        text_color="snow",
        border_color="snow",
        fg_color="#ff78f6",
        text_font=self.control.t_font,
    )
    self.OCRRead.grid(
        row=3, column=0, columnspan=3, padx=10, pady=5, sticky=tk.N
    )  # 日付列名テキストボックス配置

    # 比較対象ファイル複数選択-----------------------------------------------------------
    self.FileRead = ck.CTkButton(
        master=self.BOTTOM_Sub2,
        text="比較対象ファイル複数選択",
        command=self.ChangeFileRead,
        width=BtnWidth,
        height=BtnHeight,
        border_width=2,
        corner_radius=8,
        text_color="snow",
        border_color="snow",
        fg_color="seagreen3",
        text_font=self.control.t_font,
    )
    self.FileRead.grid(
        row=4, column=0, columnspan=3, padx=10, pady=5, sticky=tk.N
    )  # 日付列名テキストボックス配置
    # 比較対象ファイル追加---------------------------------------------------------------
    self.SingleFileRead = ck.CTkButton(
        master=self.BOTTOM_Sub2,
        text="比較対象ファイル追加",
        command=self.ChangeFileSingleRead,
        width=BtnWidth,
        height=BtnHeight,
        border_width=2,
        corner_radius=8,
        text_color="snow",
        border_color="snow",
        fg_color="Orange",
        text_font=self.control.t_font,
    )
    self.SingleFileRead.grid(
        row=5, column=0, columnspan=3, padx=10, sticky=tk.N
    )  # 日付列名テキストボックス配置

    # #######################################################################################
    # Side_Sub3##############################################################################
    self.BOTTOM_Sub3 = tk.Frame(
        BOTTOM_Frame,
        width=int(self.control.width_of_window / 4),
        height=int(self.control.height_of_window * 0.8),
        bd=2,
        bg="#fabd91",
        relief=tk.RIDGE,
    )
    self.BOTTOM_Sub3.pack(side=tk.LEFT, fill=tk.BOTH, expand=True)
    # 比較対象ファイルリストボックス------------------------------------------------------
    ck.CTkLabel(
        master=self.BOTTOM_Sub3,
        text="比較対象ファイル",
        width=LabelWidth,
        height=LabelHeight,
        corner_radius=8,
        text_font=self.control.t_font,
    ).grid(row=0, column=0)
    self.module = ""
    self.listbox_var = tk.StringVar(value=self.module)
    self.listbox = tk.Listbox(
        self.BOTTOM_Sub3,
        width=int(self.control.width_of_window / 200),
        height=int(self.control.height_of_window / 200),
        listvariable=self.listbox_var,
    )
    self.listbox.grid(row=1, column=0, padx=5, sticky=tk.E + tk.W)
    # #######################################################################################
    # Side_Sub4##############################################################################
    self.BOTTOM_Sub4 = tk.Frame(
        BOTTOM_Frame,
        width=int(self.control.width_of_window / 4),
        height=int(self.control.height_of_window * 0.8),
        bd=2,
        bg="#fabd91",
        relief=tk.RIDGE,
    )
    self.BOTTOM_Sub4.pack(side=tk.LEFT, fill=tk.BOTH, expand=True)
    # 列名テキストボックス--------------------------------------------------------------
    ck.CTkLabel(
        master=self.BOTTOM_Sub4,
        text="OCR抽出結果表URL",
        width=LabelWidth,
        height=LabelHeight,
        corner_radius=8,
        text_font=self.control.t_font,
    ).grid(row=0, column=0)
    self.OCR_url = ck.CTkEntry(
        master=self.BOTTOM_Sub4,
        textvariable=self.control.OCR_outcsv,
        width=int(EntWidth * 3),
        height=EntHeight,
        border_width=2,
        corner_radius=8,
        text_color="black",
        border_color="snow",
        text_font=self.control.t_font,
    )

    self.OCR_url.grid(
        row=0, column=1, padx=5, pady=5, sticky=tk.W
    )  # OCR抽出結果表列名テキストボックス配置
    ck.CTkLabel(
        master=self.BOTTOM_Sub4,
        text="OCR抽出結果表列名",
        width=LabelWidth,
        height=LabelHeight,
        corner_radius=8,
        text_font=self.control.t_font,
    ).grid(row=1, column=0)
    self.OCR_col = ck.CTkEntry(
        master=self.BOTTOM_Sub4,
        width=int(EntWidth * 3),
        height=EntHeight,
        border_width=2,
        corner_radius=8,
        text_color="black",
        border_color="snow",
        text_font=self.control.t_font,
    )
    try:
        print(self.pt.model.df.columns)
        OCR_colStr = ",".join(self.pt.model.df.columns)
        self.OCR_col.insert(0, OCR_colStr)  # OCR抽出結果表列名テキストボックスに文字代入
    except:
        self.OCR_col.insert(0, "")  # OCR抽出結果表列名テキストボックスに文字代入
    self.OCR_col.bind("<Return>", self.OCRtxtCol)
    self.OCR_col.grid(
        row=1, column=1, padx=5, pady=5, sticky=tk.W
    )  # OCR抽出結果表列名テキストボックス配置
    # 列名テキストボックス--------------------------------------------------------------
    ck.CTkLabel(
        master=self.BOTTOM_Sub4,
        text="比較ファイル列名",
        width=LabelWidth,
        height=LabelHeight,
        corner_radius=8,
        text_font=self.control.t_font,
    ).grid(row=2, column=0)
    self.Diff_col = ck.CTkEntry(
        master=self.BOTTOM_Sub4,
        width=int(EntWidth * 3),
        height=EntHeight,
        border_width=2,
        corner_radius=8,
        text_color="black",
        border_color="snow",
        text_font=self.control.t_font,
    )
    try:
        print(self.pt2.model.df.columns)
        Diff_colStr = ",".join(self.pt2.model.df.columns)
        self.Diff_col.delete(0, tk.END)
        self.Diff_col.insert(0, Diff_colStr)  # OCR抽出結果表列名テキストボックスに文字代入
    except:
        self.Diff_col.insert(0, "")  # OCR抽出結果表列名テキストボックスに文字代入
    self.Diff_col.bind("<Return>", self.DifftxtCol)
    self.Diff_col.grid(row=2, column=1, padx=5, pady=5, sticky=tk.W)  # 入金列名テキストボックス配置
    # 画像ファイルテキストボックス--------------------------------------------------------------
    ck.CTkLabel(
        master=self.BOTTOM_Sub4,
        text="画像ファイル",
        width=LabelWidth,
        height=LabelHeight,
        corner_radius=8,
        text_font=self.control.t_font,
    ).grid(row=3, column=0)
    self.Img_url = ck.CTkEntry(
        master=self.BOTTOM_Sub4,
        textvariable=self.control.imgurl,
        width=int(EntWidth * 3),
        height=EntHeight,
        border_width=2,
        corner_radius=8,
        text_color="black",
        border_color="snow",
        text_font=self.control.t_font,
    )
    self.Img_url.grid(row=3, column=1, padx=5, pady=5, sticky=tk.W)  # 入金列名テキストボックス配置
    # #######################################################################################
    # Side_Sub5##############################################################################
    self.BOTTOM_Sub5 = tk.Frame(
        BOTTOM_Frame,
        width=int(self.control.width_of_window / 4),
        height=int(self.control.height_of_window * 0.8),
        bd=2,
        bg="#fabd91",
        relief=tk.RIDGE,
    )
    # self.BOTTOM_Sub5.grid(row=1, column=4, sticky=tk.NSEW)
    self.BOTTOM_Sub5.pack(side=tk.LEFT, fill=tk.BOTH, expand=True)
    # 検索開始ボタン--------------------------------------------------------------------
    self.SearchBtn = ck.CTkButton(
        master=self.BOTTOM_Sub5,
        text="全検索",
        command=self.SearchStart,
        width=BtnWidth,
        height=BtnHeight,
        border_width=2,
        corner_radius=8,
        text_color="snow",
        border_color="snow",
        fg_color="mediumPurple",
        text_font=self.control.t_font,
    )
    self.SearchBtn.grid(
        row=0, column=0, pady=5, padx=10, sticky=tk.NSEW
    )  # 日付列名テキストボックス配置
    # 選択行検索開始ボタン--------------------------------------------------------------
    self.SingleSearchBtn = ck.CTkButton(
        master=self.BOTTOM_Sub5,
        text="選択行検索",
        command=self.SingleSearchStart,
        width=BtnWidth,
        height=BtnHeight,
        border_width=2,
        corner_radius=8,
        text_color="snow",
        border_color="snow",
        fg_color="hotpink1",
        text_font=self.control.t_font,
    )
    self.SingleSearchBtn.grid(
        row=1, column=0, pady=5, padx=10, sticky=tk.NSEW
    )  # 日付列名テキストボックス配置
    # 読込ボタン--------------------------------------------------------------
    self.ImgOpen = ck.CTkButton(
        master=self.BOTTOM_Sub5,
        text="画像ビューワー起動",
        command=self.ReadImg,
        width=BtnWidth,
        height=BtnHeight,
        border_width=2,
        corner_radius=8,
        text_color="snow",
        border_color="snow",
        fg_color="purple",
        text_font=self.control.t_font,
    )
    self.ImgOpen.grid(
        row=2, column=0, pady=5, padx=10, sticky=tk.NSEW
    )  # 日付列名テキストボックス配置
    # 仕訳検索ボタン--------------------------------------------------------------
    self.ImgOpen = ck.CTkButton(
        master=self.BOTTOM_Sub5,
        text="仕訳検索起動",
        command=self.JournalView,
        width=BtnWidth,
        height=BtnHeight,
        border_width=2,
        corner_radius=8,
        text_color="snow",
        border_color="snow",
        fg_color="brown",
        text_font=self.control.t_font,
    )
    self.ImgOpen.grid(
        row=3, column=0, pady=5, padx=10, sticky=tk.NSEW
    )  # 日付列名テキストボックス配置
    # 戻るボタン--------------------------------------------------------------
    self.ReturnBackBtn = ck.CTkButton(
        master=self.BOTTOM_Sub5,
        text="戻る",
        command=self.ReturnBack,
        width=BtnWidth,
        height=BtnHeight,
        border_width=2,
        corner_radius=8,
        text_color="snow",
        border_color="snow",
        fg_color="gray",
        text_font=self.control.t_font,
    )
    self.ReturnBackBtn.grid(
        row=4, column=0, pady=5, padx=10, sticky=tk.NSEW
    )  # 日付列名テキストボックス配置
    # # フレーム設定---------------------------------------------------------------------
    # DGF.create_Frame2(
    #     self,
    #     int(self.control.width_of_window / self.wid),
    #     int(self.control.height_of_window / self.hei),
    #     list(self.module),
    #     self.control.t_font,
    #     self.hei_Par,
    #     self.G_logger,
    # )  # 比較表フレーム

    # # フレーム設定---------------------------------------------------------------------
    # self.IMG_frame = tk.Frame(
    #     self.Main_Frame,
    #     width=int(self.control.width_of_window / self.wid),
    #     height=int(self.control.height_of_window / self.hei),
    #     bd=2,
    #     bg="#fce4d2",
    #     relief=tk.RIDGE,
    # )  # 親フレーム
    # self.IMG_frame.pack(side=tk.LEFT, fill=tk.BOTH, expand=True)
    # self.IMG_frame.pack_forget()
    # self.Img_c = 0
    # self.RView = ReplaceView.Main(self, self.FileName, self.OCR_tbname)  # 置換テーブルの読込
    # self.RView.withdraw()
    # self.update()

    # ----------------------------------------------------------------------

    return BOTTOM_Frame


def radioclick(self):
    """
    ラジオボタン切替
    """
    if self.select_var.get() == 1:
        # self.select_var.set(0)
        # sm = self.master.children["!application"]
        self.master.children["!application"].SplitVar.configure(
            bg="gray10", state="readonly"
        )
        self.In_v.configure(bg="gray10", state="readonly")
        self.Out_v.configure(bg="gray10", state="readonly")
        self.Money_v.configure(bg="gray10", state="readonly")
        self.IMtxt.configure(bg="snow", state="normal")
        self.OMtxt.configure(bg="snow", state="normal")
        self.update()
    else:
        # sm = self.master.children["!application"]
        # self.select_var.set(1)
        self.SplitVar.configure(bg="snow", state="normal")
        self.In_v.configure(bg="snow", state="normal")
        self.Out_v.configure(bg="snow", state="normal")
        self.Money_v.configure(bg="snow", state="normal")
        self.IMtxt.configure(bg="gray10", state="readonly")
        self.OMtxt.configure(bg="gray10", state="readonly")
        self.update()
