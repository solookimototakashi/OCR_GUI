import tkinter as tk
from tkinter import ttk
import customtkinter as ck
import Functions
from tkinter import filedialog, messagebox
import ImageViewer
from functools import wraps
import logging.config
import os

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


# ###############################################################################################


class ViewGUI(ttk.Frame):
    """
    概要: TKinterメインWindowクラス
    """

    def __init__(self, master, control):
        super().__init__(master)
        self.control = control
        self.FrameCreate()  # フレーム作成

    # 要素作成######################################################################################
    def FrameCreate(self):
        """
        Frame作成
        """
        try:
            self.Frame = tk.Frame(
                self,
                # bg="#60cad1",
                bg="black",
                relief=tk.GROOVE,
                bd=1,
                height=self.control.height_of_window,
                width=self.control.width_of_window,
            )
            self.BOTTOM = tk.Frame(
                master=self.Frame,
                # master=self,
                bg="#60cad1",
                relief=tk.GROOVE,
                bd=1,
                height=self.control.Bottom_Column,
                width=self.control.width_of_window,
            )
            self.BOTTOM.pack(side=tk.BOTTOM, fill=tk.BOTH, expand=True)
            self.CanvasCreate()
            self.Frame.pack(fill=tk.BOTH, expand=True)
            # ImageViewer.call("", Frame)

            # self.control.window_sub_FrameCanvas = ImageViewer.Application(
            #     tk.Frame(
            #         master=self,
            #         height=self.control.FCH,
            #         # width=self.control.FCW,
            #         width=3000,
            #     ),
            #     self.control,
            # )

            # self.control.window_sub_FrameCanvas.master.pack(
            #     side=tk.TOP, fill="both", expand=True
            # )
            # フォルダ・ファイル選択
            self.window_sub_ctrl1 = self.SubFrame1()
            # 画像加工
            self.window_sub_ctrl2 = self.SubFrame2()
            self.window_sub_ctrl3 = self.SubFrame3()
            return
        except:
            return

    # ----------------------------------------------------------------------------------
    def CanvasCreate(self):
        """
        キャンバス作成
        """
        try:
            # キャンバス
            self.window_sub_canvas = tk.Canvas(
                master=self.Frame,
                # self,
                height=self.control.FCH,
                width=self.control.FCW,
                bg="gray",
            )
            # キャンバス内クリック開始イベントに関数バインド
            self.window_sub_canvas.bind("<ButtonPress-1>", self.event_clip_start)
            # キャンバス内ドラッグイベントに関数バインド
            self.window_sub_canvas.bind("<Button1-Motion>", self.event_clip_keep)
            # キャンバス内クリック終了イベントに関数バインド
            self.window_sub_canvas.bind("<ButtonRelease-1>", self.event_clip_end)
            # キャンバスを配置
            self.window_sub_canvas.pack(side=tk.TOP, fill=tk.BOTH, expand=True)
            self.control.SetCanvas(self.window_sub_canvas)  # キャンバスをセット
        except:
            self.control.logger.debug("キャンバス作成失敗")  # Log出力

    # ------------------------------------------------------------------------------------
    def SubFrame1(self):
        """
        フレーム1作成
        """
        BtnWidth, BtnHeight = 70, 20
        EntWidth, EntHeight = 70, 20
        LabelWidth, LabelHeight = 70, 20
        self.str_dir = tk.StringVar()
        # IntVar生成
        self.radio_intvar1 = tk.IntVar()
        self.radio_intvar2 = tk.IntVar()

        Frame = tk.Frame(
            master=self.BOTTOM,
            height=self.control.Bottom_Column,
            width=300,
            bg="#60cad1",
            relief=tk.GROOVE,
            bd=1,
        )
        # フォルダー・ファイル選択を配置
        Frame.pack(side=tk.LEFT, padx=5, fill=tk.BOTH, expand=True)
        # フォルダ選択ボタン生成
        self.button_setdir = ck.CTkButton(
            master=Frame,
            text="フォルダ選択",
            command=self.event_set_folder,
            width=BtnWidth,
            height=BtnHeight,
            border_width=2,
            corner_radius=8,
            text_color="snow",
            border_color="snow",
            fg_color="seagreen3",
        )
        # 前画像ボタン生成
        self.button_setdir.grid(row=0, column=0, padx=5, pady=5, sticky=tk.W + tk.E)
        self.button_prev = ck.CTkButton(
            master=Frame,
            text="前画像<<",
            command=self.event_prev,
            width=BtnWidth,
            height=BtnHeight,
            border_width=2,
            corner_radius=8,
            text_color="snow",
            border_color="snow",
        )
        self.button_prev.grid(row=0, column=1, padx=5, pady=5, sticky=tk.W + tk.E)
        # 切替ボタン生成
        self.button_next = ck.CTkButton(
            master=Frame,
            text=">>次画像",
            command=self.event_next,
            width=BtnWidth,
            height=BtnHeight,
            border_width=2,
            corner_radius=8,
            text_color="snow",
            border_color="snow",
        )
        self.button_next.grid(row=0, column=2, padx=5, pady=5, sticky=tk.W + tk.E)
        # 　テキストエントリ生成
        self.entry_dir = ck.CTkEntry(
            master=Frame,
            placeholder_text="entry_dir",
            textvariable=self.str_dir,
            width=EntWidth,
            height=EntHeight,
            border_width=2,
            corner_radius=8,
            text_color="black",
            border_color="snow",
        )
        self.entry_dir.grid(
            row=1, column=0, columnspan=3, padx=5, pady=5, sticky=tk.W + tk.E
        )
        # ラベル
        self.label_target = ck.CTkLabel(
            master=Frame,
            text="[ファイル]",
            width=LabelWidth,
            height=LabelHeight,
            corner_radius=8,
        )
        self.label_target.grid(
            row=2, column=0, columnspan=3, padx=5, pady=5, sticky=tk.W
        )
        # コンボBOX生成
        self.combo_file = ck.CTkComboBox(
            master=Frame,
            # text="combo_file",
            # value=self.file_list,
            values=self.control.file_list,
            state="readonly",
            width=EntWidth,
            command=self.event_updatefile,
        )
        self.combo_file.set(self.control.file_list[0])
        self.combo_file.grid(
            row=3, column=0, columnspan=3, padx=5, pady=5, sticky=tk.W + tk.E
        )

    # ------------------------------------------------------------------------------------
    def SubFrame2(self):
        """
        フレーム2作成
        """
        BtnWidth, BtnHeight = 70, 20
        EntWidth, EntHeight = 70, 20
        LabelWidth, LabelHeight = 70, 20
        Frame = tk.Frame(
            master=self.BOTTOM,
            height=self.control.Bottom_Column,
            width=300,
            bg="#60cad1",
            relief=tk.GROOVE,
            bd=1,
        )
        Frame.pack(side=tk.LEFT, padx=5, fill=tk.BOTH, expand=True)
        self.label_rotate = ck.CTkLabel(
            master=Frame,
            text="[画像回転]",
            width=LabelWidth,
            height=LabelHeight,
            corner_radius=8,
        )
        self.label_rotate.grid(row=0, column=0, padx=5, pady=5, sticky=tk.W)
        # 回転角度ラジオボックス生成
        self.radio_intvar1 = tk.IntVar()
        self.radio_intvar2 = tk.IntVar()
        self.radio_intvar1.set(0)  # 0:No select
        self.radio_intvar2.set(0)  # 0:No select
        self.radio_rotate = []
        for val, text in enumerate(
            ["90°", "180°", "270°"]
        ):  # 1:rot90 2:rot180 3:rot270
            self.radio_rotate.append(
                tk.Radiobutton(
                    Frame,
                    text=text,
                    value=val + 1,
                    variable=self.radio_intvar1,
                    command=self.event_rotate,
                    bg="#60cad1",
                )
            )
        self.radio_rotate[0].grid(row=1, column=0, padx=5, pady=5, sticky=tk.W + tk.E)
        self.radio_rotate[1].grid(row=1, column=1, padx=5, pady=5, sticky=tk.W + tk.E)
        self.radio_rotate[2].grid(row=1, column=2, padx=5, pady=5, sticky=tk.W + tk.E)

        self.label_flip = ck.CTkLabel(
            master=Frame,
            text="[反転]",
            width=LabelWidth,
            height=LabelHeight,
            corner_radius=8,
        )
        self.label_flip.grid(row=3, column=0, padx=5, pady=5, sticky=tk.W)
        self.radio_flip = []
        for val, text in enumerate(["U/D", "L/R"]):  # 1:Flip U/L 2:Flip L/R
            self.radio_flip.append(
                tk.Radiobutton(
                    Frame,
                    text=text,
                    value=val + 1,
                    variable=self.radio_intvar2,
                    command=self.event_flip,
                    bg="#60cad1",
                )
            )
        self.radio_flip[0].grid(row=4, column=0, padx=5, pady=5, sticky=tk.W + tk.E)
        self.radio_flip[1].grid(row=4, column=1, padx=5, pady=5, sticky=tk.W + tk.E)

    # ------------------------------------------------------------------------------------
    def SubFrame3(self):
        """
        フレーム2作成
        """
        BtnWidth, BtnHeight = 70, 20
        EntWidth, EntHeight = 70, 20
        LabelWidth, LabelHeight = 70, 20
        Frame = tk.Frame(
            master=self.BOTTOM,
            height=self.control.Bottom_Column,
            width=300,
            bg="#60cad1",
            relief=tk.GROOVE,
            bd=1,
        )
        Frame.pack(side=tk.LEFT, padx=5, fill=tk.BOTH, expand=True)
        self.label_clip = ck.CTkLabel(
            master=Frame,
            text="[トリミング・削除]",
            width=LabelWidth,
            height=LabelHeight,
            corner_radius=8,
        )
        self.label_clip.grid(row=0, column=0, padx=5, pady=5, sticky=tk.W)
        # クリップボタン生成
        self.button_clip_start = ck.CTkButton(
            master=Frame,
            text="選択開始",
            command=self.event_clip_try,
            width=BtnWidth,
            height=BtnHeight,
            border_width=2,
            corner_radius=8,
            text_color="snow",
            border_color="snow",
            fg_color="#7eb000",
        )
        self.button_clip_start.grid(row=1, column=0, padx=5, pady=5, sticky=tk.W + tk.E)
        self.button_clip_done = ck.CTkButton(
            master=Frame,
            text="範囲トリミング",
            command=self.event_clip_done,
            width=BtnWidth,
            height=BtnHeight,
            border_width=2,
            corner_radius=8,
            text_color="snow",
            border_color="snow",
            fg_color="#6100b0",
        )
        self.button_clip_done.grid(row=1, column=1, padx=5, pady=5, sticky=tk.W + tk.E)
        self.button_clip_Erace = ck.CTkButton(
            master=Frame,
            text="範囲削除",
            command=self.event_clip_Erace,
            width=BtnWidth,
            height=BtnHeight,
            border_width=2,
            corner_radius=8,
            text_color="snow",
            border_color="snow",
            fg_color="#c7048c",
        )
        self.button_clip_Erace.grid(row=1, column=2, padx=5, pady=5, sticky=tk.W + tk.E)
        self.label_run = ck.CTkLabel(
            master=Frame,
            text="[編集確定]",
            width=LabelWidth,
            height=LabelHeight,
            corner_radius=8,
        )
        self.label_run.grid(row=2, column=0, columnspan=2, padx=5, pady=5, sticky=tk.W)
        # Save/Undoボタン生成
        self.button_Oversave = ck.CTkButton(
            master=Frame,
            text="上書保存",
            command=self.event_Oversave,
            width=BtnWidth,
            height=BtnHeight,
            border_width=2,
            corner_radius=8,
            text_color="snow",
            border_color="snow",
            fg_color="#cf94ff",
        )
        self.button_Oversave.grid(row=3, column=0, padx=5, pady=5, sticky=tk.W + tk.E)
        self.button_undo = ck.CTkButton(
            master=Frame,
            text="編集取消",
            command=self.event_undo,
            width=BtnWidth,
            height=BtnHeight,
            border_width=2,
            corner_radius=8,
            text_color="snow",
            border_color="snow",
            fg_color="gray",
        )
        self.button_undo.grid(row=3, column=1, padx=5, pady=5, sticky=tk.W + tk.E)
        self.button_save = ck.CTkButton(
            master=Frame,
            text="別名保存",
            command=self.event_save,
            width=BtnWidth,
            height=BtnHeight,
            border_width=2,
            corner_radius=8,
            text_color="snow",
            border_color="snow",
            fg_color="hotpink1",
        )
        self.button_save.grid(row=3, column=2, padx=5, pady=5, sticky=tk.W + tk.E)
        # LineOCR起動ボタン生成
        self.button_LinOCR = ck.CTkButton(
            master=Frame,
            text="OCR起動",
            # command=self.LinOCROpen,
            width=BtnWidth,
            height=BtnHeight,
            border_width=2,
            corner_radius=8,
            text_color="snow",
            border_color="snow",
            fg_color="tomato",
        )
        self.button_LinOCR.grid(row=4, column=0, padx=5, pady=5, sticky=tk.W + tk.E)
        # # Exposeイベントbind
        # for event_type in EventType.__members__.keys():
        #     if event_type == "Expose":
        #         event_seq = "<" + event_type + ">"
        #         try:
        #             self.bind_all(
        #                 event_seq, self.event_handler
        #             )
        #             # print(event_type)
        #         except TclError:
        #             # print("bind error:", event_type)
        #             pass
        # -------------------------------------------------------------------

    # ボタンクリックイベント#######################################################################
    def event_set_folder(self):
        """
        フォルダ選択ボタンクリックイベント
        """
        self.control.dir_path = filedialog.askdirectory(
            title="関与先フォルダを開く",
            initialdir=r"C:\Users\もちねこ\Desktop\GitHub\RPAScript\OCRView\CompanyData\1869",
        )
        self.control.Kanyosaki_name = os.path.basename(self.control.dir_path)
        self.entry_dir.insert(0, self.control.dir_path)
        self.control.file_list = self.control.SetDirlist(self.control.dir_path)
        self.combo_file.configure(values=self.control.file_list)

    # ----------------------------------------------------------------------------------
    def event_updatefile(self, event):
        """
        ファイル選択ウィンドウクリックイベント
        """
        self.control.file_list = self.control.SetDirlist(self.control.dir_path)
        self.combo_file["value"] = self.control.file_list
        self.control.imgurl.set(self.control.dir_path + r"/" + self.combo_file.get())

        self.control.img_name = os.path.splitext(
            os.path.basename(self.control.imgurl.get())
        )[0]

        FN = os.path.basename(self.control.imgurl.get())
        f_r = 0
        for f_l in self.control.file_list:
            if f_l == FN:
                set_pos = f_r
                break
            f_r += 1
        self.control.DrawImage("set", set_pos=set_pos)

    # ----------------------------------------------------------------------------------
    def event_save(self):
        """
        Saveボタンクリックイベント
        """
        try:
            if self.control.Kanyosaki_name != "":
                # 一時保存ファイルを確認
                if self.control.model.stock_url != "":
                    os.remove(self.control.model.stock_url)
                self.Newfilename = filedialog.asksaveasfilename(
                    filetypes=[("PNG", ".png"), ("JPEG", ".jpg")]
                )
                self.control.SaveImage(self.Newfilename)
                self.file_list = self.control.SetDirlist(
                    self.control.dir_path
                )  # ファイルリストリロード
                for F_r in range(len(self.file_list)):
                    if self.file_list[F_r] in self.Newfilename:
                        self.control.model.stock_url = ""
                        self.combo_file.set(self.file_list[F_r])
            else:
                messagebox.showinfo("確認", "画像ファイルが選択されていません。")
        except:
            messagebox.showinfo("確認", "画像ファイルが選択されていません。")

    def event_Searchsave(self):
        """
        編集履歴確認イベント
        """
        try:
            # 一時保存ファイルを確認
            if self.control.model.stock_url != "":
                if messagebox.askokcancel("確認", "編集履歴が残っています。上書きしますか？"):
                    os.remove(self.control.model.stock_url)
                    self.control.model.stock_url = ""
                    self.control.OverSaveImage()
        except:
            messagebox.showinfo("確認", "編集履歴確認でエラーが起きました。")

    def event_prev(self):
        """
        prevボタンクリックイベント
        """
        pos = int(self.control.DrawImage("prev")[0])
        self.combo_file.set(self.control.file_list[pos])

    def event_next(self):
        """
        nextボタンクリックイベント
        """
        pos = int(self.control.DrawImage("next")[0])
        self.combo_file.set(self.control.file_list[pos])

    def event_rotate(self):
        """
        画像回転変更イベント
        """
        val = self.radio_intvar1.get()
        cmd = "rotate-" + str(val)
        self.control.EditImage(cmd)

    def event_flip(self):
        """
        画像反転イベント
        """
        val = self.radio_intvar2.get()
        cmd = "flip-" + str(val)
        self.control.EditImage(cmd)

    def event_clip_try(self):
        """
        Tryボタンイベント
        """
        self.clip_enable = True

    def event_clip_done(self):
        """
        Doneボタンイベント
        """
        if self.clip_enable:
            self.control.EditImage("clip_done")
            self.clip_enable = False

    def event_clip_Erace(self):
        """
        Eraceボタンイベント
        """
        if self.clip_enable:
            self.control.EditImage("clip_Erace")
            self.clip_enable = False

    def event_clip_start(self, event):
        """
        画像処理Saveイベント
        """
        if self.clip_enable:
            self.control.DrawRectangle("clip_start", event.y, event.x)

    def event_clip_keep(self, event):
        """
        画像処理Undoイベント
        """
        if self.clip_enable:
            self.control.DrawRectangle("clip_keep", event.y, event.x)

    def event_clip_end(self, event):
        """
        キャンバス画像左クリック範囲指定で終端まで確定後
        """
        if self.clip_enable:
            self.control.DrawRectangle("clip_end", event.y, event.x)

    def event_Oversave(self):
        """
        OverSaveボタンクリックイベント
        """
        self.control.OverSaveImage()

    def event_undo(self):
        """
        Undoボタンクリックイベント
        """
        self.control.UndoImage("None")
        self.radio_intvar1.set(0)
        self.radio_intvar2.set(0)

    # #######################################################################################


def Open():
    import ControlGUI
    import logging.config
    import os

    logging.config.fileConfig(os.getcwd() + r"\LogConf\logging_debug.conf")
    logger = logging.getLogger(__name__)
    control = ControlGUI.ControlGUI("./", logger)  # セルフコントローラー
    main_window = tk.Tk()
    top = tk.Toplevel()
    ViewGUI(top, control)
    main_window.mainloop()


if __name__ == "__main__":
    Open()
