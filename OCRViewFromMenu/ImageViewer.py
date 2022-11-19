import tkinter as tk  # ウィンドウ作成用
from PIL import Image, ImageTk  # 画像データ用
import numpy as np  # アフィン変換行列演算用
import os  # ディレクトリ操作用
import IconCode


class Application(tk.Frame):
    def __init__(self, Frame, control, master=None):

        self.control = control

        self.master = Frame
        self.pil_image = None  # 表示する画像データ
        # self.back_color = "#60cad1"  # 背景色
        self.back_color = "gray"  # 背景色
        self.create_widget_forFrame()  # ウィジェットの作成

        # self.set_image(imgurl)
        # self.update()

    def menu_open_clicked(self, event=None):
        global imgurl
        # ファイル→開く
        filename = tk.filedialog.askopenfilename(
            filetypes=[
                ("Image file", ".bmp .png .jpg .tif"),
                ("Bitmap", ".bmp"),
                ("PNG", ".png"),
                ("JPEG", ".jpg"),
                ("Tiff", ".tif"),
            ],  # ファイルフィルタ
            initialdir=os.getcwd(),  # カレントディレクトリ
        )
        try:
            m = self.master
            while m is not None:
                L_m = m
                m = m.master
            L_m.children["!application"].Img_url.delete(0, tk.END)
            L_m.children["!application"].Img_url.insert(0, filename)
            L_m.children["!application"].imgurl = filename
            imgurl = filename
        except:
            return
        # 画像ファイルを設定する
        self.set_image(filename)

    def menu_Reopen_clicked(self, event=None):
        # ファイル→開く
        # 画像ファイルを設定する
        self.set_image(imgurl)

    def menu_quit_clicked(self):
        # ウィンドウを閉じる
        self.master.destroy()

    # create_menuメソッドを定義
    def create_menu(self):
        self.menu_bar = tk.Menu(self)  # Menuクラスからmenu_barインスタンスを生成

        self.file_menu = tk.Menu(self.menu_bar, tearoff=tk.OFF)
        self.menu_bar.add_cascade(label="開く", menu=self.file_menu)

        self.file_menu.add_command(
            label="Open", command=self.menu_open_clicked, accelerator="Ctrl+O"
        )
        self.file_menu.add_separator()  # セパレーターを追加
        self.file_menu.add_command(label="Exit", command=self.menu_quit_clicked)

        # self.menu_bar.bind_all(
        #     "<Control-o>", self.menu_open_clicked
        # )  # ファイルを開くのショートカット(Ctrol-Oボタン)
        self.menu_bar.add_separator()  # セパレーターを追加
        self.menu_bar.add_command(
            label="再表示", command=self.menu_Reopen_clicked, accelerator="Ctrl+k"
        )

        self.master.config(menu=self.menu_bar)  # メニューバーの配置

    def create_widget(self):
        """ウィジェットの作成"""

        # ステータスバー相当(親に追加)
        self.statusbar = tk.Frame(self.master)
        self.mouse_position = tk.Label(
            self.statusbar, relief=tk.SUNKEN, text="mouse position"
        )  # マウスの座標
        self.image_position = tk.Label(
            self.statusbar, relief=tk.SUNKEN, text="image position"
        )  # 画像の座標
        self.label_space = tk.Label(self.statusbar, relief=tk.SUNKEN)  # 隙間を埋めるだけ
        self.image_info = tk.Label(
            self.statusbar, relief=tk.SUNKEN, text="image info"
        )  # 画像情報
        # self.mouse_position.pack(side=tk.LEFT)
        # self.image_position.pack(side=tk.LEFT)
        # self.label_space.pack(side=tk.LEFT, expand=True, fill=tk.X)
        # self.image_info.pack(side=tk.RIGHT)
        self.statusbar.pack(side=tk.BOTTOM, fill=tk.X)

        # Canvas
        self.control.canvas = tk.Canvas(self.master, background=self.back_color)
        self.control.canvas.pack(expand=True, fill=tk.BOTH)  # この両方でDock.Fillと同じ

        # マウスイベント
        self.master.bind("<Motion>", self.mouse_move)  # MouseMove
        self.master.bind("<B1-Motion>", self.mouse_move_left)  # MouseMove（左ボタンを押しながら移動）
        # self.master.bind(
        #     "<Shift-B1-Motion>", self.Shift_mouse_move_left
        # )  # MouseMove（左ボタンを押しながら移動）
        self.master.bind("<Button-1>", self.mouse_down_left)  # MouseDown（左ボタン）
        self.master.bind(
            "<Double-Button-1>", self.mouse_double_click_left
        )  # MouseDoubleClick（左ボタン）
        self.master.bind("<MouseWheel>", self.mouse_wheel)  # MouseWheel

    def create_widget_forFrame(self):
        """ウィジェットの作成"""

        # # ステータスバー相当(親に追加)
        self.statusbar = tk.Frame(self.master)

        # self.mouse_position = tk.Label(
        #     self.statusbar, relief=tk.SUNKEN, text="mouse position"
        # )  # マウスの座標
        # self.image_position = tk.Label(
        #     self.statusbar, relief=tk.SUNKEN, text="image position"
        # )  # 画像の座標
        # # self.label_space = tk.Label(self.statusbar, relief=tk.SUNKEN)  # 隙間を埋めるだけ
        # self.image_info = tk.Label(
        #     self.statusbar, relief=tk.SUNKEN, text="image info"
        # )  # 画像情報
        # # self.mouse_position.pack(side=tk.LEFT)
        # # self.image_position.pack(side=tk.LEFT)
        # # self.label_space.pack(side=tk.LEFT)
        # # self.image_info.pack(side=tk.LEFT)
        # self.ImgSet_btn = tk.Button(
        #     self.statusbar, text="再表示", command=self.menu_Reopen_clicked
        # )
        # self.ImgSet_btn.pack(side=tk.LEFT, expand=True, fill=tk.X)
        # self.Open_btn = tk.Button(
        #     self.statusbar, text="画像選択", command=self.menu_open_clicked
        # )
        # self.Open_btn.pack(side=tk.RIGHT, expand=True, fill=tk.X)
        # self.statusbar.pack(side=tk.BOTTOM, fill=tk.X)

        # Canvas
        self.control.canvas = tk.Canvas(self.master, background=self.back_color)
        self.control.canvas.pack(
            side=tk.TOP, expand=True, fill=tk.BOTH
        )  # この両方でDock.Fillと同じ

        # マウスイベント
        # self.control.canvas.bind("<Motion>", self.mouse_move)  # MouseMove
        self.control.canvas.bind(
            "<B1-Motion>", self.mouse_move_left
        )  # MouseMove（左ボタンを押しながら移動）
        # self.master.bind(
        #     "<Shift-B1-Motion>", self.Shift_mouse_move_left
        # )  # MouseMove（左ボタンを押しながら移動）
        self.control.canvas.bind("<Button-1>", self.mouse_down_left)  # MouseDown（左ボタン）
        self.control.canvas.bind(
            "<Double-Button-1>", self.mouse_double_click_left
        )  # MouseDoubleClick（左ボタン）
        self.control.canvas.bind("<MouseWheel>", self.mouse_wheel)  # MouseWheel

    def set_image(self, filename):
        """画像ファイルを開く"""
        if not filename:
            return
        # PIL.Imageで開く
        self.pil_image = Image.open(filename)
        # 画像全体に表示するようにアフィン変換行列を設定
        self.zoom_fit(self.pil_image.width, self.pil_image.height)
        # 画像の表示
        self.draw_image(self.pil_image)

        # # ウィンドウタイトルのファイル名を設定
        # self.master.title(self.my_title + " - " + os.path.basename(filename))
        # # ステータスバーに画像情報を表示する
        # self.image_info[
        #     "text"
        # ] = f"{self.pil_image.format} : {self.pil_image.width} x {self.pil_image.height} {self.pil_image.mode}"
        # カレントディレクトリの設定
        os.chdir(os.path.dirname(filename))

    # -------------------------------------------------------------------------------
    # マウスイベント
    # -------------------------------------------------------------------------------

    def mouse_move(self, event):
        """マウスの移動時"""
        # マウス座標
        self.mouse_position["text"] = f"mouse(x, y) = ({event.x: 4d}, {event.y: 4d})"

        if self.pil_image is None:
            return

        # 画像座標
        mouse_posi = np.array([event.x, event.y, 1])  # マウス座標(numpyのベクトル)
        mat_inv = np.linalg.inv(self.mat_affine)  # 逆行列（画像→Cancasの変換からCanvas→画像の変換へ）
        image_posi = np.dot(mat_inv, mouse_posi)  # 座標のアフィン変換
        x = int(np.floor(image_posi[0]))
        y = int(np.floor(image_posi[1]))
        if x >= 0 and x < self.pil_image.width and y >= 0 and y < self.pil_image.height:
            # 輝度値の取得
            value = self.pil_image.getpixel((x, y))
            self.image_position["text"] = f"image({x: 4d}, {y: 4d}) = {value}"
        else:
            self.image_position["text"] = "-------------------------"

    def mouse_move_left(self, event):
        """マウスの左ボタンをドラッグ"""
        if self.pil_image is None:
            return
        self.translate(event.x - self.__old_event.x, event.y - self.__old_event.y)
        self.redraw_image()  # 再描画
        self.__old_event = event

    # def Shift_mouse_move_left(self, event):
    #     """Shift+マウス左ドラッグ"""
    #     self.translate(event.x - self.__old_event.x, event.y - self.__old_event.y)
    #     self.redraw_image()  # 再描画
    #     self.__old_event = event

    def DrawRectangle(self, canvas, clip_sy, clip_sx, clip_ey, clip_ex):
        """長方形描画"""
        if canvas.gettags("clip_rect"):
            canvas.delete("clip_rect")

        canvas.create_rectangle(
            clip_sx, clip_sy, clip_ex, clip_ey, outline="red", tag="clip_rect"
        )

    def mouse_down_left(self, event):
        """マウスの左ボタンを押した"""
        self.__old_event = event

    def mouse_double_click_left(self, event):
        """マウスの左ボタンをダブルクリック"""
        if self.pil_image is None:
            return
        self.zoom_fit(self.pil_image.width, self.pil_image.height)
        self.redraw_image()  # 再描画

    def mouse_wheel(self, event):
        """マウスホイールを回した"""
        if self.pil_image is None:
            return

        if event.delta < 0:
            # 上に回転の場合、縮小
            self.scale_at(0.8, event.x, event.y)
        else:
            # 下に回転の場合、拡大
            self.scale_at(1.25, event.x, event.y)

        self.redraw_image()  # 再描画

    # -------------------------------------------------------------------------------
    # 画像表示用アフィン変換
    # -------------------------------------------------------------------------------

    def reset_transform(self):
        """アフィン変換を初期化（スケール１、移動なし）に戻す"""
        self.mat_affine = np.eye(3)  # 3x3の単位行列

    def translate(self, offset_x, offset_y):
        """平行移動"""
        mat = np.eye(3)  # 3x3の単位行列
        mat[0, 2] = float(offset_x)
        mat[1, 2] = float(offset_y)

        self.mat_affine = np.dot(mat, self.mat_affine)

    def scale(self, scale: float):
        """拡大縮小"""
        mat = np.eye(3)  # 単位行列
        mat[0, 0] = scale
        mat[1, 1] = scale

        self.mat_affine = np.dot(mat, self.mat_affine)

    def scale_at(self, scale: float, cx: float, cy: float):
        """座標(cx, cy)を中心に拡大縮小"""

        # 原点へ移動
        self.translate(-cx, -cy)
        # 拡大縮小
        self.scale(scale)
        # 元に戻す
        self.translate(cx, cy)

    def zoom_fit(self, image_width, image_height):
        """画像をウィジェット全体に表示させる"""

        # キャンバスのサイズ
        canvas_width = self.control.canvas.winfo_width()
        canvas_height = self.control.canvas.winfo_height()

        if (image_width * image_height <= 0) or (canvas_width * canvas_height <= 0):
            return

        # アフィン変換の初期化
        self.reset_transform()

        scale = 1.0
        offsetx = 0.0
        offsety = 0.0

        if (canvas_width * image_height) > (image_width * canvas_height):
            # ウィジェットが横長（画像を縦に合わせる）
            scale = canvas_height / image_height
            # あまり部分の半分を中央に寄せる
            offsetx = (canvas_width - image_width * scale) / 2
        else:
            # ウィジェットが縦長（画像を横に合わせる）
            scale = canvas_width / image_width
            # あまり部分の半分を中央に寄せる
            offsety = (canvas_height - image_height * scale) / 2

        # 拡大縮小
        self.scale(scale)
        # あまり部分を中央に寄せる
        self.translate(offsetx, offsety)

    # -------------------------------------------------------------------------------
    # 描画
    # -------------------------------------------------------------------------------

    def draw_image(self, pil_image):

        if pil_image is None:
            return

        self.control.canvas.delete("all")

        # キャンバスのサイズ
        canvas_width = self.control.canvas.winfo_width()
        canvas_height = self.control.canvas.winfo_height()

        # キャンバスから画像データへのアフィン変換行列を求める
        # （表示用アフィン変換行列の逆行列を求める）
        mat_inv = np.linalg.inv(self.mat_affine)

        # PILの画像データをアフィン変換する
        dst = pil_image.transform(
            (canvas_width, canvas_height),  # 出力サイズ
            Image.AFFINE,  # アフィン変換
            tuple(mat_inv.flatten()),  # アフィン変換行列（出力→入力への変換行列）を一次元のタプルへ変換
            Image.NEAREST,  # 補間方法、ニアレストネイバー
            fillcolor=self.back_color,
        )

        # 表示用画像を保持
        self.image = ImageTk.PhotoImage(image=dst, master=self.master)

        # 画像の描画
        self.control.canvas.create_image(
            0,
            0,  # 画像表示位置(左上の座標)
            anchor="nw",  # アンカー、左上が原点
            image=self.image,  # 表示画像データ
        )
        # self.master.attributes("-topmost", True)
        # self.master.attributes("-topmost", False)

    def redraw_image(self):
        """画像の再描画"""
        if self.pil_image is None:
            return
        self.draw_image(self.pil_image)


def call(imgu, Frame):
    global imgurl
    imgurl = imgu
    app = Application(Frame, master=None)
    return app


def Alonecall(imgu):
    global imgurl
    root = tk.Tk()
    imgurl = imgu
    # root.attributes("-topmost", True)
    data = IconCode.icondata()
    root.tk.call("wm", "iconphoto", root._w, tk.PhotoImage(data=data, master=root))
    # imgurl = r"C:\Users\もちねこ\Desktop\PDFTEST\JA_1page.png"
    app = Application(master=root)
    app.mainloop()


if __name__ == "__main__":
    global imgurl

    root = tk.Tk()
    # root.attributes("-topmost", True)
    data = IconCode.icondata()
    root.tk.call("wm", "iconphoto", root._w, tk.PhotoImage(data=data, master=root))
    imgurl = r"C:\Users\もちねこ\Desktop\PDFTEST\JA_1page.png"
    app = Application(master=root)
    app.mainloop()
