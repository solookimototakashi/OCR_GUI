from tkinter import filedialog, messagebox
import pandas as pd
import os
import numpy as np
from chardet.universaldetector import UniversalDetector
import tomli_w
import sqlite3 as sql
from pandas import read_csv, concat

# -----------------------------------------------------------------------------------
class CreateDB:
    """
    dbを作成する
    """

    def __init__(self, dbname, tbname=None):
        # すでに存在していれば、それにアスセスする。
        self.dbname = dbname
        conn = sql.connect(self.dbname)

        # データベースへのコネクションを閉じる。(必須)
        conn.close()

    def TableUpdate(self, tbname):
        try:
            conn = sql.connect(self.dbname)
            cur = conn.cursor()
            # データの投入
            self.df.to_sql(tbname, conn, if_exists="replace", index=False)
        finally:
            cur.close()
            conn.close()

    def readsql_to_df(self, tbname):
        try:
            conn = sql.connect(self.dbname)
            cur = conn.cursor()

            # terminalで実行したSQL文と同じようにexecute()に書く
            self.df = pd.read_sql_query("SELECT * FROM " + tbname, conn)
        except:
            print("sqlReadErr")
            raise
        finally:
            cur.close()
            conn.close()

    def df_replace_to_sql(self, tbname, df):
        try:
            conn = sql.connect(self.dbname)
            cur = conn.cursor()
            # データの投入
            # df = df.reset_index()
            df.to_sql(tbname, conn, if_exists="replace", index=True)
            self.df = df
        except:
            print("sqlimportErr")
            raise
        finally:
            cur.close()
            conn.close()

    def list_to_df_replace_to_sql(self, tbname, in_list):
        """
        listを成型してDF保存
        """
        try:
            ind = [x for x in range(len(in_list))]
            column_list = ["x1", "y1", "x2", "y2", "LineName"]
            df = pd.DataFrame(
                data=in_list,
                columns=column_list,
                index=ind,
            )
            df[["x1", "y1", "x2", "y2"]].astype(int)
            self.df_replace_to_sql(tbname, df)
        except:
            print("Err")

    def replaceText_to_sql(self, tbname, in_list):
        """
        listを成型してDF保存
        """
        try:
            ind = [x for x in range(len(in_list))]
            column_list = ["変更前", "変更後"]
            df = pd.DataFrame(
                data=in_list,
                columns=column_list,
                index=ind,
            )
            df[["変更前", "変更後"]].astype(str)
            self.df_replace_to_sql(tbname, df)
        except:
            print("Err")


# -----------------------------------------------------------------------------------
def getFileEncoding(file_path):  # .format( getFileEncoding( "sjis.csv" ) )
    if os.path.isfile(file_path) is True:
        detector = UniversalDetector()
        with open(file_path, mode="rb") as f:
            for binary in f:
                detector.feed(binary)
                if detector.done:
                    break
        detector.close()
        return detector.result["encoding"]
    else:
        messagebox.showinfo("確認", file_path + "\nが存在しません。")
        return ""


# -----------------------------------------------------------------------------------
def blankno(List):
    if len() != 0:
        TN_List = [int(str(t[0][0]).replace("Line", "")) for t in List]
        TN_List.sort()
        N_TN_r = 0
        for TN_r in TN_List:
            if N_TN_r == 0:
                N_TN_r = TN_r + 1
            else:
                if N_TN_r == TN_r:
                    N_TN_r = TN_r + 1
                else:
                    return N_TN_r
        N_TN_r = TN_r + 1
        return N_TN_r
    else:
        return 1


# -------------------------------------------------------------------------------------
def Pandas_mem_usage(df):
    """
    Pandasデータフレームのメモリ最適化
    """
    start_mem = df.memory_usage().sum() / 1024**2
    print("Memory usage of dataframe is {:.2f} MB".format(start_mem))

    for col in df.columns:
        col_type = df[col].dtype

        if col_type != object:
            c_min = df[col].min()
            c_max = df[col].max()
            if str(col_type)[:3] == "int":
                if c_min > np.iinfo(np.int8).min and c_max < np.iinfo(np.int8).max:
                    df[col] = df[col].astype(np.int8)
                elif c_min > np.iinfo(np.int16).min and c_max < np.iinfo(np.int16).max:
                    df[col] = df[col].astype(np.int16)
                elif c_min > np.iinfo(np.int32).min and c_max < np.iinfo(np.int32).max:
                    df[col] = df[col].astype(np.int32)
                elif c_min > np.iinfo(np.int64).min and c_max < np.iinfo(np.int64).max:
                    df[col] = df[col].astype(np.int64)
            else:
                if (
                    c_min > np.finfo(np.float16).min
                    and c_max < np.finfo(np.float16).max
                ):
                    df[col] = df[col].astype("object")
                    # df[col] = df[col].astype(np.float16)
                    # df[col] = df[col].astype(np.int16)
                elif (
                    c_min > np.finfo(np.float32).min
                    and c_max < np.finfo(np.float32).max
                ):
                    df[col] = df[col].astype("object")
                    # df[col] = df[col].astype(np.float32)
                    # df[col] = df[col].astype(np.int32)
                else:
                    df[col] = df[col].astype("object")
                    # df[col] = df[col].astype(np.float64)
                    # df[col] = df[col].astype(np.int64)
        else:
            df[col] = df[col].astype("object")
            # df[col] = df[col].astype("category")

    end_mem = df.memory_usage().sum() / 1024**2
    print("Memory usage after optimization is: {:.2f} MB".format(end_mem))
    print("Decreased by {:.1f}%".format(100 * (start_mem - end_mem) / start_mem))

    return df


# -------------------------------------------------------------------------------------
def JoinCSV(CSVList):
    """
    概要: 引数リストのURLから連結CSVを作成
    @param CSVList: CSVURLリスト
    @return 連結CSVURL
    """
    try:
        r = 0
        for CSVListItem in CSVList:
            if r == 0:
                enc = getFileEncoding(CSVListItem)
                m_csv = read_csv(CSVListItem, encoding=enc)
            else:
                enc = getFileEncoding(CSVListItem)
                r_csv = read_csv(CSVListItem, encoding=enc)
                m_csv = concat([m_csv, r_csv])
            r += 1
        return True, m_csv
    except:
        return False, ""


# -------------------------------------------------------------------------------------
def dump_toml(toml_dict, path):
    """
    tomlで読み込んだ辞書をtomlファイルに出力する
    """
    try:
        with open(path, "wb") as configfile:
            tomli_w.dump(toml_dict, configfile)
    except:
        print("Err")


if __name__ == "__main__":

    db = CreateDB("LineSettingData.db", tbname=None)
    l = np.array(
        [
            [0, 0, 0, 0, "Tate"],
            [0, 0, 0, 0, "Yoko"],
            [1, 1, 1, 1, "Tate"],
            [1, 1, 1, 1, "Yoko"],
        ]
    )
    ind = [x for x in range(l.shape[0])]
    df = pd.DataFrame(
        data=l,
        columns=["x1", "y1", "x2", "y2", "LineName"],
        index=ind,
    )
    df[["x1", "y1", "x2", "y2"]].astype(int)
    db.df_replace_to_sql("OCR", df)
    print(db.df)
