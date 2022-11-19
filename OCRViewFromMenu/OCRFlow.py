from GCloudVision import Bankrentxtver
import os
import toml
from pandas import DataFrame
from csv import reader, QUOTE_NONNUMERIC
from numpy import asarray

# ----------------------------------------------------------------------------
def getNearestValue(list, num):
    """
    概要: リストからある値に最も近い値を返却する関数
    @param list: データ配列
    @param num: 対象値
    @return 対象値に最も近い値
    """

    # リスト要素と対象値の差分を計算し最小値のインデックスを取得
    array = asarray(list)
    array = asarray(array[:, 0], dtype="float64")
    idx = (abs(array - num)).argmin()
    return list[idx]


# ----------------------------------------------------------------------------
def DiffCheck(GFTable, ColList):
    """
    概要: データフレームの列数にあわせて列名リスト要素数を変更
    @param list: データ配列
    @param num: 対象値
    @return 対象値に最も近い値
    """

    # データフレームの列数にあわせて列名リスト要素数を変更------------------------------
    try:
        GC_Diff = len(GFTable[0]) - len(ColList)
    except:
        GC_Diff = GFTable.shape[1] - len(ColList)
    if GC_Diff < 0:
        GC_Diff = GC_Diff * -1
        for GC_d in range(GC_Diff):
            ColList.pop(len(ColList) - 1)
    else:
        for GC_d in range(GC_Diff):
            ColList.append("未設定" + str(GC_d + 1))


# ----------------------------------------------------------------------------
def DiffListCreate(self):
    """
    概要: GoogleVisionApiを実行し、結果をCSV化
    @param FileURL : 画像URL(str)
    @param Yoko : 横軸リスト
    @param Tate : 縦軸リスト
    @param Banktoml : toml設定ファイルURL(str)
    @param ColList : 列名リスト(list)
    @param DaySet : 日付列番号リスト(list)
    @param MoneySet : 金額表示列番号リスト(list)
    @param ReplaceSet : 置換対象列番号のリスト(list)
    @param ReplaceStr : 置換対象文字列のリスト(list)
    @return : bool,CSVURL(str)
    """
    # ####################################################################################
    readcsv1 = self.control.YokoList
    readcsv2 = self.control.TateList
    COLArray = True, readcsv1, readcsv2
    # ####################################################################################
    if COLArray[0] is True:
        GF = Bankrentxtver(
            self.control.imgurl,
            COLArray[1],
            COLArray[2],
        )  # 画像URL,横軸閾値,縦軸閾値,ラベル配置間隔,etax横軸閾値,etax縦軸閾値,etaxラベル配置間隔,ラベル(str),同行として扱う縦間隔
        print(GF[0])

        if GF[0] is True:
            GFTable = GF[1]
            # --------------------------------------------------------------
            # DataFrame作成
            # 分割文字列リストを結合---------------------------------------------------------
            ColList = self.control.OutColumn
            df = DataFrame(GFTable, columns=ColList)
            DiffCheck(df, ColList)  # データフレームの列数にあわせて列名リスト要素数を変更
            # -----------------------------------------------------------------------------
            self.control.OCR_outcsv.set(
                os.path.dirname(self.control.imgurl)
                + r"/"
                + self.control.tomlTitle
                + ".csv"
            )

            try:
                df.to_csv(
                    self.control.OCR_outcsv.get(),
                    index=False,
                    encoding="cp932",
                    quoting=QUOTE_NONNUMERIC,
                )
            except:
                with open(
                    self.control.OCR_outcsv.get(),
                    mode="w",
                    encoding="cp932",
                    errors="ignore",
                    newline="",
                ) as f:
                    df.to_csv(f, index=False, quoting=QUOTE_NONNUMERIC)
            return True, self.control.OCR_outcsv.get()


# -------------------------------------------------------------------------------------
def Main(self):
    """
    概要: 呼出関数
    @param FileURL : 画像URL(str)
    @param Yoko : 横軸リスト
    @param Tate : 縦軸リスト
    @param Banktoml : toml設定ファイルURL(str)
    @param ColList : 日付列番号リスト(list)
    @param MoneySet : 金額表示列番号リスト(list)
    @param ReplaceSet : 置換対象列番号のリスト(list)
    @param ReplaceStr : 置換対象文字列のリスト(list)
    @return : bool,CSVURL(str)
    """
    # # toml読込------------------------------------------------------------------------------
    # with open(os.getcwd() + r"/TKInterGUI/BankSetting.toml", encoding="utf-8") as f:
    #     Banktoml = toml.load(f)
    #     print(Banktoml)
    # # -----------------------------------------------------------
    DLC = DiffListCreate(self)
    if DLC[0] is True:
        return DLC
    else:
        return False, ""


if __name__ == "__main__":
    # toml読込------------------------------------------------------------------------------
    with open(os.getcwd() + r"/BankSetting.toml", encoding="utf-8") as f:
        Banktoml = toml.load(f)
        print(Banktoml)
    # -----------------------------------------------------------
    URL = os.getcwd()
    readcsv1 = []
    with open(
        URL + r"\StraightListYoko.csv",
        "r",
        newline="",
    ) as inputfile:
        for row in reader(inputfile):
            for rowItem in row:
                rsp = (
                    rowItem.replace("[", "")
                    .replace("]", "")
                    .replace(" ", "")
                    .split(",")
                )
                readcsv1.append([int(rsp[0]), int(rsp[1]), int(rsp[2]), int(rsp[3])])
    readcsv2 = []
    with open(
        URL + r"\StraightListTate.csv",
        "r",
        newline="",
    ) as inputfile:
        for row in reader(inputfile):
            for rowItem in row:
                rsp = (
                    rowItem.replace("[", "")
                    .replace("]", "")
                    .replace(" ", "")
                    .split(",")
                )
                readcsv2.append([int(rsp[0]), int(rsp[1]), int(rsp[2]), int(rsp[3])])
    for fd_path, sb_folder, sb_file in os.walk(r"D:\Souzoku_JAPng"):
        si = 0
        for sb_fileItem in sb_file:
            if si >= 14:
                imgurl = fd_path + "\\" + sb_fileItem
                DiffListCreate(imgurl, readcsv1, readcsv2, Banktoml, "JASouzoku")
            si += 1
