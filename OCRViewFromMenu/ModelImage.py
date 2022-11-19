import os
import numpy as np

# from datetime import datetime
from PIL import Image, ImageTk, ImageOps, ImageDraw
import cv2

# import math
from pathlib import Path
from pdf2image import convert_from_path


class ModelImage:
    def __init__(self, ImageType="Photo"):

        self.ImageType = ImageType
        self.edit_img = None
        self.original_img = None
        self.canvas_w = 0
        self.canvas_h = 0

    def set_image_layout(self, canvas, image):
        """
        キャンバスサイズにあわせた画像サイズ変換関数
        """
        self.canvas_w = canvas.winfo_width()
        self.canvas_h = canvas.winfo_height()

        h, w = image.height, image.width

        if h > w:
            self.resize_h = self.canvas_h
            self.resize_w = int(w * (self.canvas_h / h))
            self.pad_x = (self.canvas_w - self.resize_w) // 2
            self.pad_y = 0

        else:
            self.resize_w = self.canvas_w
            self.resize_h = int(h * (self.canvas_w / w))
            self.pad_y = (self.canvas_h - self.resize_h) // 2
            self.pad_x = 0

        print(h, w, self.resize_h, self.resize_w, self.pad_y, self.pad_x)

    def get_correct_values(self, rate, sy, sx, ey, ex):

        mod_sx = int(np.min((sx, ex)) * rate)
        mod_sy = int(np.min((sy, ey)) * rate)
        mod_ex = int(np.max((sx, ex)) * rate)
        mod_ey = int(np.max((sy, ey)) * rate)
        ch, cw = mod_ey - mod_sy, mod_ex - mod_sx

        return mod_sy, mod_sx, ch, cw

    def get_original_coords(self, h, w, args):

        print(args, h, w)
        sy, sx, ey, ex = args["sy"], args["sx"], args["ey"], args["ex"]

        if h > w:
            rate = h / self.canvas_h
            # x_spc = self.pad_x * rate
            sy, sx, ch, cw = self.get_correct_values(rate, sy, sx, ey, ex)
            # sx = sx - x_spc
            # sx = int(np.max((sx, 0)))
            # sx = int(np.min((sx, w)))

        else:
            rate = w / self.canvas_w
            # y_spc = self.pad_y * rate
            sy, sx, ch, cw = self.get_correct_values(rate, sy, sx, ey, ex)
            # sy = sy - y_spc
            # sy = int(np.max((sy, 0)))
            # sy = int(np.min((sy, h)))

        return sy, sx, ch, cw

    def edit_image_command(self, orginal_image, edit_image, command, args={}):

        if edit_image is not None:
            img = edit_image
        else:
            img = orginal_image.copy()

        np_img = np.array(img)

        if "flip-1" in command:  # U/L
            np_img = np.flip(np_img, axis=0)

        elif "flip-2" in command:  # L/R
            np_img = np.flip(np_img, axis=1)

        elif "rotate-" in command:  # 1:rot90 2:rot180 3:rot270
            cmd = int(command.replace("rotate-", ""))
            np_img = np.rot90(np_img, cmd)

        elif "rotateFree-" in command:
            cmd = int(command.replace("rotateFree-", ""))
            rotimg = img.rotate(cmd, expand=True)
            np_img = np.array(rotimg)
            # return img.rotate(cmd, expand=True)

        elif "clip_done" in command:
            C_url = self.original_img.filename.split(".")
            C_url = C_url[0] + "edit." + C_url[1]
            h, w = np_img[:, :, 0].shape
            sy, sx, ch, cw = self.get_original_coords(h, w, args)
            np_img = np_img[sy : sy + ch, sx : sx + cw, :]
            imwrite(C_url, np_img)
            self.stock_url = C_url

        elif "clip_Erace" in command:
            C_url = self.original_img.filename.split(".")
            C_url = C_url[0] + "edit." + C_url[1]
            img = imread(self.original_img.filename)
            img = cv2.rectangle(
                img,
                (args["sx"], args["sy"]),
                (args["ex"], args["ey"]),
                (255, 255, 255),
                thickness=-1,
            )
            imwrite(C_url, img)
            self.stock_url = C_url
            np_img = np.array(img)

        return Image.fromarray(np_img)

    # Public

    def GetValidPos(self, pos_y, pos_x):
        """
        トリミング範囲計算
        """
        if self.resize_h > self.resize_w:
            valid_pos_y = pos_y
            valid_pos_x = np.max((pos_x, self.pad_x))
            valid_pos_x = np.min((valid_pos_x, self.canvas_w - self.pad_x))

        else:
            valid_pos_x = pos_x
            valid_pos_y = np.max((pos_y, self.pad_y))
            valid_pos_y = np.min((valid_pos_y, self.canvas_h - self.pad_y))

        return valid_pos_y, valid_pos_x

    def DrawImage(self, fpath, canvas, command, args={}):

        if canvas.gettags("Photo"):
            canvas.delete("Photo")

        if self.edit_img is not None and command != "None":
            img = self.edit_img

        else:
            img = Image.open(fpath)
            self.original_img = img
            self.edit_img = None
            self.set_image_layout(canvas, self.original_img)
            self.original_width = img.size[0]
            self.original_height = img.size[1]
        if command == "clip_Erace":
            img = self.edit_image_command(
                self.original_img, self.edit_img, command, args=args
            )
            self.edit_img = img
            self.set_image_layout(canvas, self.edit_img)
        elif command != "None" and not command == "Map":
            if not len(args) == 0:
                args["sx"] = int(args["sx"] * (self.resize_w / self.original_width))
                args["sy"] = int(args["sy"] * (self.resize_h / self.original_height))
                args["ex"] = int(args["ex"] * (self.resize_w / self.original_width))
                args["ey"] = int(args["ey"] * (self.resize_h / self.original_height))
            img = self.edit_image_command(
                self.original_img, self.edit_img, command, args=args
            )
            self.edit_img = img
            self.set_image_layout(canvas, self.edit_img)
        elif command == "Map":
            if not len(args) == 0:
                args["sx"] = int(args["sx"] * (self.resize_w / self.original_width))
                args["sy"] = int(args["sy"] * (self.resize_h / self.original_height))
                args["ex"] = int(args["ex"] * (self.resize_w / self.original_width))
                args["ey"] = int(args["ey"] * (self.resize_h / self.original_height))
            img = self.edit_image_command(
                self.original_img, self.edit_img, command, args=args
            )
            self.edit_img = img
            self.set_image_layout(canvas, self.edit_img)

        pil_img = ImageOps.pad(img, (self.canvas_w, self.canvas_h))
        self.tk_img = ImageTk.PhotoImage(image=pil_img)
        canvas.create_image(
            self.canvas_w / 2, self.canvas_h / 2, image=self.tk_img, tag="Photo"
        )

    def DrawRectangle(self, canvas, clip_sy, clip_sx, clip_ey, clip_ex):

        if canvas.gettags("clip_rect"):
            canvas.delete("clip_rect")

        canvas.create_rectangle(
            clip_sx, clip_sy, clip_ex, clip_ey, outline="red", tag="clip_rect"
        )

    def SaveImage(self, fname):

        fpath = fname
        self.edit_img.save(fpath)
        print("Saved: {}".format(fpath))

    def OverSaveImage(self, fname):

        if self.edit_img is not None:
            name, ext = os.path.splitext(fname)
            name = name.replace("\\", "/")
            fpath = name.replace("/", r"\\") + ext

            self.edit_img.save(fpath)
            print("Saved: {}".format(fpath))

    # def ImageLotate(self, URL, imgurl, disth, canth1, canth2, casize, do):
    #     """
    #     概要: 画像から直線を検出し、画像の傾きを調べ回転して上書き保存
    #     @param URL: 画像フォルダ(str)
    #     @param imgurl: 画像URL(str)
    #     @param disth: マージする線分の距離(float)
    #     @param canth1: Canny Edge Detectorの引数1(float)
    #     @param canth2: Canny Edge Detectorの引数2(float)
    #     @param casize: Canny Edge Detectorに使うSobelのサイズ(0ならCannyは適用しない)(int)
    #     @param dom: Trueなら線分をマージして出力する(boolean)
    #     @return 傾き値リスト(np配列)
    #     """
    #     try:
    #         img = imread(imgurl)
    #         # 回転-----------------------------------------------------------------------
    #         # StraightLineDetectionで最後の一つになるまで絞りだしたピクセル連続線から
    #         # 角度をmathアークタンジェントで計算し、degreesでラジアン→℃変換後画像を回転
    #         Kakuavg = self.StraightLineDetection(
    #             URL, imgurl, disth, canth1, canth2, casize, do
    #         )
    #         if Kakuavg[0] is True:
    #             x1 = Kakuavg[1][:, 1]
    #             y1 = Kakuavg[1][:, 0]
    #             x2 = Kakuavg[1][:, 3]
    #             y2 = Kakuavg[1][:, 2]
    #             # numpyとmathではy,x軸が反対なので入替--------------------------------------
    #             x = np.average(y1) - np.average(y2)
    #             y = np.average(x1) - np.average(x2)
    #             # ------------------------------------------------------------------------
    #             tan = math.degrees(math.atan2(y, x))
    #             img = Image.open(imgurl)
    #             img = img.rotate(tan)
    #         # ---------------------------------------------------------------------------
    #         else:
    #             return False
    #         return img
    #     except:
    #         return False

    def TotalNoise(self, imgurl, ksize):
        S_imgurl = imgurl.split(".")
        S_imgurl = S_imgurl[0] + "edit." + S_imgurl[1]
        Inv_img = self.ColorInverter(imgurl)  # 白黒反転(PIL)
        Inv_img.save(S_imgurl)  # 白黒反転保存(PIL)
        img = imread(S_imgurl)  # 白黒反転画像(cv2)
        CleanUp_img = self.NoiseRemoval(img, ksize)  # ノイズ除去(cv2)
        imwrite(S_imgurl, CleanUp_img)  # ノイズ除去保存(cv2)
        Inv_img = self.ColorInverter(S_imgurl)  # 白黒反転(PIL)
        Inv_img.save(S_imgurl)  # 白黒反転保存(PIL)
        Inv_img = Image.open(S_imgurl)
        return Inv_img

    def StraightLineDetection(self, URL, imgurl, disth, canth1, canth2, casize, do):
        """
        概要: 画像から直線を検出し、画像の傾きを調べる
        @param URL: 画像フォルダ(str)
        @param imgurl: 画像URL(str)
        @param disth: マージする線分の距離(float)
        @param canth1: Canny Edge Detectorの引数1(float)
        @param canth2: Canny Edge Detectorの引数2(float)
        @param casize: Canny Edge Detectorに使うSobelのサイズ(0ならCannyは適用しない)(int)
        @param dom: Trueなら線分をマージして出力する(boolean)
        @return 傾き値リスト(np配列)
        """
        try:
            img = imread(imgurl)
            size = img.shape  # 画像のサイズ x,y
            Pix = int(size[0] / 100)  # 検出ピクセル数
            LCheck = False  # ライン検出フラグ
            while LCheck is False:  # ライン検出フラグTrueまでループ
                FLStock = []
                if Pix <= 0:
                    Pix = 1
                # FLDインスタンス生成
                FLDs = self.FastLineDetector(
                    imgurl,
                    Pix,
                    disth,
                    canth1,
                    canth2,
                    casize,
                    do,
                )  # boolean,yx値
                if FLDs[0] is True:  # 連続ピクセルを検知したら
                    FLDItem = len(FLDs[1])  # 配列要素数
                    if FLDItem <= 3:  # 配列要素数0なら
                        print(str(FLDItem) + "要素なので終了")
                        FLStock = FLDs[1]
                        LCheck = True
                    else:
                        print(str(FLDItem) + "要素取得")
                        FLStock = FLDs[1]
                PlPix = size[0] / 1000
                if PlPix < 1:
                    Pix += 1
                else:
                    Pix += int(PlPix)
            XLFlag = False
            for x in range(len(FLStock)):
                UpY = FLStock[x][0][0]
                UpX = FLStock[x][0][1]
                LoY = FLStock[x][0][2]
                LoX = FLStock[x][0][3]
                if XLFlag is False:
                    XList = np.array([[UpY, UpX, LoY, LoX]])
                    XLFlag = True
                else:
                    XList = np.append(XList, [[UpY, UpX, LoY, LoX]], axis=0)
            return True, XList
        except:
            return False, ""

    def FastLineDetector(self, fileImage, lenth, disth, canth1, canth2, casize, dom):
        """
        概要: 画像の線形を検出
        @param fileImage: 画像URL(str)
        @param lenth: 検出する最小の線分のピクセル数(int)
        @param disth: マージする線分の距離(float)
        @param canth1: Canny Edge Detectorの引数1(float)
        @param canth2: Canny Edge Detectorの引数2(float)
        @param casize: Canny Edge Detectorに使うSobelのサイズ(0ならCannyは適用しない)(int)
        @param dom: Trueなら線分をマージして出力する(boolean)
        @return boolean,検出ラインピクセル値配列,ライン描画後画像のcvインスタンス
        """
        colorimg = imread(fileImage, cv2.IMREAD_COLOR)  # 元画像
        if colorimg is None:
            return False, "", ""
        image = cv2.cvtColor(colorimg.copy(), cv2.COLOR_BGR2GRAY)

        # FLDパラメーター設定--------------------------------------------
        length_threshold = lenth
        distance_threshold = disth
        canny_th1 = canth1
        canny_th2 = canth2
        canny_aperture_size = casize
        do_merge = dom
        # -------------------------------------------------------------
        # FLDインスタンス化
        fld = cv2.ximgproc.createFastLineDetector(
            length_threshold,
            distance_threshold,
            canny_th1,
            canny_th2,
            canny_aperture_size,
            do_merge,
        )

        # ライン取得
        lines = fld.detect(image)
        # # ライン描画後画像のインスタンス作成
        out = fld.drawSegments(colorimg, lines)
        return True, lines, out

    def ColorInverter(self, imgurl):
        """
        概要: 画像白黒反転
        @param img: 画像URL(str)
        @return 白黒反転した画像(cv2)
        """
        img = Image.open(imgurl).convert("RGB")
        Inv_img = ImageOps.invert(img)
        return Inv_img

    def NoiseRemoval(self, img, ksize):
        """
        概要: 画像ノイズ除去（収縮⇒膨張）
        @param img: cv2で開いた画像
        @return 画像ノイズ除去した画像(cv2)
        """
        kernel = np.ones((2, 2))
        Open_img = cv2.morphologyEx(img, cv2.MORPH_OPEN, kernel)
        # 中央値フィルタ
        Open_img = cv2.medianBlur(Open_img, ksize)
        return Open_img

    def pdf_image(self, pdf_file, fmtt, dpi, PBAR):
        """
        概要: popplerでPDFを指定した画像形式に変換
        @param pdf_file : PDFURL(str)
        @param img_path : 画像フォルダURL(str)
        @param fmtt : 変換後の画像形式(str)
        @param dpi : 変換する際の解像度(int)
        @param PDFPage : 変換するPDFのページ番号(str)
        @return : bool
        @return : 変換後画像URLのリスト(list)
        """
        try:
            Mydir = os.getcwd()
            pppath = Mydir + r"\poppler-22.01.0\Library\bin"
            # pdf_file、img_pathをPathにする
            pdf_path = Path(pdf_file)
            image_dir = os.path.dirname(pdf_file)
            os.environ["PATH"] += os.pathsep + str(pppath)
            FileKey = os.path.basename(pdf_file)
            FileKey = FileKey.replace(".pdf", "").replace(".PDF", "")
            # 線形検出パラメータ設定########################################
            disth = 1.41421356
            canth1 = 50.0
            canth2 = 50.0
            casize = 3
            do = True
            # ############################################################
            PBAR._target.step(10)
            # PDFをImage に変換(pdf2imageの関数)
            pages = convert_from_path(pdf_path, dpi, poppler_path=pppath)
            PS = 40
            PS_x = 50 / len(pages)
            PBAR._target.step(PS)

            # 画像ファイルを１ページずつ保存
            for i, page in enumerate(pages):
                file_name = FileKey + "_" + str(i + 1) + "page." + fmtt
                image_path = image_dir + r"/" + file_name
                page.save(image_path, fmtt)
                self.PDFChange(image_dir, image_path, disth, canth1, canth2, casize, do)
                PBAR._target.step(PS_x)
            PBAR._target.master.destroy()
            return True
        except:
            PBAR._target.master.destroy()
            return False

    def PDFChange(self, URL, imgurl, disth, canth1, canth2, casize, do):
        """
        概要: OCR読込用に画像を自動編集
        @param URL: 画像フォルダ(str)
        @param imgurl: 画像URL(str)
        @param disth: マージする線分の距離(float)
        @param canth1: Canny Edge Detectorの引数1(float)
        @param canth2: Canny Edge Detectorの引数2(float)
        @param casize: Canny Edge Detectorに使うSobelのサイズ(0ならCannyは適用しない)(int)
        @param dom: Trueなら線分をマージして出力する(boolean)
        @return OCR読込用に画像を自動編集した画像URL(str)
        """
        Inv_img = self.ColorInverter(imgurl)  # 白黒反転(PIL)
        Inv_img.save(imgurl)  # 白黒反転保存(PIL)
        img = imread(imgurl)  # 白黒反転画像(cv2)
        CleanUp_img = self.NoiseRemoval(img, 3)  # ノイズ除去(cv2)
        imwrite(imgurl, CleanUp_img)  # ノイズ除去保存(cv2)
        Inv_img = self.ColorInverter(imgurl)  # 白黒反転(PIL)
        Inv_img.save(imgurl)  # 白黒反転保存(PIL)
        # # 画像から直線を検出し、画像の傾きを調べ回転して上書き保存
        # ILT = self.ImageLotate(URL, imgurl, disth, canth1, canth2, casize, do)
        # if ILT is True:
        img = imread(imgurl)
        # 画像リサイズ-----------------------------------------------
        IMGsize = [3840, 3840]
        h, w = img.shape[:2]
        ash = IMGsize[1] / h
        asw = IMGsize[0] / w
        if asw < ash:
            sizeas = (int(w * asw), int(h * asw))
        else:
            sizeas = (int(w * ash), int(h * ash))
        img = cv2.resize(img, dsize=sizeas)
        imwrite(imgurl, img)
        # ----------------------------------------------------------
        # self.TesseOCRLotate(URL, imgurl)  # 無料OCRで回転
        # img = imread(imgurl)
        # TC = self.toneCurveUpContrast(img)  # トーンカーブ処理
        # imwrite(imgurl, TC)
        # 直線を削除------------------------------------------------------
        # self.StraightLineErase(URL, imgurl, disth, canth1, canth2, casize, do)
        # ---------------------------------------------------------------
        # ImageColorChange(URL, img)
        return imgurl
        # else:
        #     return imgurl

    def StraightLineErase(self, imgurl, disth, canth1, canth2, casize, do):
        """
        概要: 画像から直線を検出し、白で塗り潰す
        @param URL: 画像フォルダ(str)
        @param imgurl: 画像URL(str)
        @param disth: マージする線分の距離(float)
        @param canth1: Canny Edge Detectorの引数1(float)
        @param canth2: Canny Edge Detectorの引数2(float)
        @param casize: Canny Edge Detectorに使うSobelのサイズ(0ならCannyは適用しない)(int)
        @param dom: Trueなら線分をマージして出力する(boolean)
        @return 傾き値リスト(np配列)
        """
        try:
            img = imread(imgurl)
            S_imgurl = imgurl.split(".")
            S_imgurl = S_imgurl[0] + "edit." + S_imgurl[1]
            size = img.shape  # 画像のサイズ 横,縦
            Pix = int(size[0] / 50)  # 検出ピクセル数
            LineWidth = int((size[0] / 2000))
            LCheck = False  # ライン検出フラグ
            while LCheck is False:  # ライン検出フラグTrueまでループ
                FLStock = []
                if Pix <= 0:
                    Pix = 1
                # FLDインスタンス生成
                FLDs = self.FastLineDetector(
                    imgurl,
                    Pix,
                    disth,
                    canth1,
                    canth2,
                    casize,
                    do,
                )  # boolean,yx値
                if FLDs[0] is True:  # 連続ピクセルを検知したら
                    # FLDItem = len(FLDs[1])  # 配列要素数
                    FLStock = FLDs[1]
                    LCheck = True
            ######################################################
            img = Image.open(imgurl)
            draw = ImageDraw.Draw(img)
            ######################################################
            for x in range(len(FLStock)):
                # UpY = int(FLStock[x][0][0])  # 縦
                # UpX = int(FLStock[x][0][1])  # 横
                # LoY = int(FLStock[x][0][2])  # 縦
                # LoX = int(FLStock[x][0][3])  # 横

                UpY = FLStock[x][0][0]  # 縦
                UpX = FLStock[x][0][1]  # 横
                LoY = FLStock[x][0][2]  # 縦
                LoX = FLStock[x][0][3]  # 横

                YDif = UpY - LoY
                if YDif < 0:
                    YDif = YDif * -1
                XDif = UpX - LoX
                if XDif < 0:
                    XDif = XDif * -1
                # 線を消す(白で線を引く)
                if YDif > XDif:
                    # no_lines_img = cv2.line(
                    #     img, (0, UpX), (size[1], LoX), (255, 255, 255), LineWidth
                    # )
                    draw.line([(0, UpX), (size[1], LoX)], fill="White", width=LineWidth)
                elif YDif < XDif:
                    # no_lines_img = cv2.line(
                    #     img, (UpY, 0), (LoY, size[0]), (255, 255, 255), LineWidth
                    # )
                    draw.line([(UpY, 0), (LoY, size[0])], fill="White", width=LineWidth)
                else:
                    # no_lines_img = cv2.line(
                    #     img, (UpY, UpX), (LoY, LoX), (255, 255, 255), LineWidth
                    # )
                    draw.line([(UpY, UpX), (LoY, LoX)], fill="White", width=LineWidth)
            # imwrite(URL + r"\NoLine.png", no_lines_img)
            # 画像の表示
            img.save(imgurl)
            # img.show()
            return img
        except:
            return False


def imread(filename, flags=cv2.IMREAD_COLOR, dtype=np.uint8):
    try:
        n = np.fromfile(filename, dtype)
        img = cv2.imdecode(n, flags)
        return img
    except Exception as e:
        print(e)
        return None


def imwrite(filename, img, params=None):
    try:
        ext = os.path.splitext(filename)[1]
        result, n = cv2.imencode(ext, img, params)

        if result:
            with open(filename, mode="w+b") as f:
                n.tofile(f)
            return True
        else:
            return False
    except Exception as e:
        print(e)
        return False
