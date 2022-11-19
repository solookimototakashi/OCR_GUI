# -*- coding: utf-8 -*-


# """Wareki (和暦) : Japanese style way of counting years
# Author: 古川貴之
# 和暦の表現方法
# >>> Wareki(Gengo('平成'), 32)
# Wareki(Gengo('平成'), 32)
# >>> S(39)
# Wareki(Gengo('昭和'), 39)
# >>> str(H(32))
# '平成32年'
# 西暦を和暦に変換する
# >>> Wareki.from_ad(2020)
# Wareki(Gengo('平成'), 32)
# 和暦を西暦に変換する
# >>> H(32).to_ad()
# 2020
# # 次のように、int()に渡すこともできます。
# >>> int(H(32))
# 2020
# """

import datetime as _datetime

_gengo_table = [
    {
        "name": "明治",
        "started": _datetime.date(1868, 1, 1),
        "ended": _datetime.date(1912, 7, 29),
    },
    {
        "name": "大正",
        "started": _datetime.date(1912, 7, 30),
        "ended": _datetime.date(1926, 12, 24),
    },
    {
        "name": "昭和",
        "started": _datetime.date(1926, 12, 25),
        "ended": _datetime.date(1989, 1, 7),
    },
    {
        "name": "平成",
        "started": _datetime.date(1989, 1, 8),
        "ended": _datetime.date(2019, 4, 30),
    },
    {"name": "令和", "started": _datetime.date(2019, 5, 1), "ended": None},
]


class Gengo:
    """元号
    >>> Gengo('平成')(32)
    Wareki(Gengo('平成'), 32)
    TODO: 明治より前の元号をサポート。
    """

    def __init__(self, name):
        self._name = name
        for i in _gengo_table:
            if i["name"] == name:
                self._started = i["started"]
                self._ended = i["ended"]
                break
        else:
            raise ValueError()

    @classmethod
    def from_date(cls, dt):
        for i in reversed(_gengo_table):
            started = i["started"]
            if dt > started:
                gengo = cls(i["name"])
                break
        else:
            raise ValueError()
        return gengo

    @property
    def name(self):
        return self._name

    @property
    def started(self):
        return self._started

    @property
    def ended(self):
        return self._ended

    @classmethod
    def get_current(cls):
        return cls(_gengo_table[-1]["name"])

    def __str__(self):
        return self.name

    def __repr__(self):
        s = __class__.__name__ + "('" + self.name + "')"
        return s

    def __eq__(self, other):
        return self.name == other.name

    def __contains__(self, date):
        left = self.started <= date
        if self == __class__.get_current():
            right = True
        else:
            right = date <= self.ended
        return left and right

    def __call__(self, year):
        """和暦を返す"""
        return Wareki(self, year)


# アルファベット
M = Gengo("明治")
T = Gengo("大正")
S = Gengo("昭和")
H = Gengo("平成")
R = Gengo("令和")


def _ad2gengo(year):
    return Gengo.from_date(_datetime.date(year, 12, 31))


class Wareki:
    """和暦を元号と年で表現するクラス"""

    def __init__(self, gengo, year):
        """Constructor."""
        self._gengo = gengo
        self._year = year

    @classmethod
    def from_ad(cls, year):
        gengo = _ad2gengo(year)
        obj = cls(gengo, year - gengo.started.year + 1)
        return obj

    @property
    def gengo(self):
        """元号"""
        return self._gengo

    @property
    def year(self):
        return self._year

    def __repr__(self):
        s = "{}({}, {})".format(__class__.__name__, repr(self.gengo), self.year)
        return s

    def __str__(self):
        gengo = str(self.gengo)
        # year = '元' if self.year == 1 else self.year
        year = self.year
        s = "{}{}年".format(gengo, year)
        return s

    def to_ad(self):
        return self.gengo.started.year + self.year - 1

    __int__ = to_ad


class WarekiDate(_datetime.date):
    """和暦を用いた日付表現"""

    @classmethod
    def from_ad(cls, date):
        obj = cls(Wareki.from_ad(date.year), date.month, date.day)
        return obj

    @property
    def wareki(self):
        return Wareki.from_ad(self.year)

    def __str__(self):
        return "{}{}月{}日".format(self.wareki, self.month, self.day)

    def __repr__(self):
        s = "{}({}, {}, {})".format(
            __class__.__name__, repr(self.wareki), self.month, self.day
        )
        return s

    def to_date(self):
        return _datetime.date(self.wareki, self.month, self.day)


def SeirekiDate(Nengou, Nen, Mon, Da):
    omikuji = {"M": 1868, "T": 1912, "S": 1926, "H": 1989, "R": 2019}

    if Nengou in omikuji:
        PlusYear = omikuji[Nengou]
        Dater = str(PlusYear + Nen - 1) + "/" + str(Mon) + "/" + str(Da)
        return Dater
    else:
        print("エラー")


def SeirekiSTRDate(d):
    """
    令和3年4月1日(引数)→2021/4/1(戻り値)
    """
    omikuji = {"明治": 1868, "大正": 1912, "昭和": 1926, "平成": 1989, "令和": 2019}
    if "明治" in d:
        Nengou = "明治"
        dsp = d.split("明治")
        dsp = dsp[1].split("年")
        Nen = int(dsp[0])
        dsp = dsp[1].split("月")
        Mon = int(dsp[0])
        dsp = dsp[1].split("日")
        Da = int(dsp[0])
    elif "大正" in d:
        Nengou = "大正"
        dsp = d.split("大正")
        dsp = dsp[1].split("年")
        Nen = int(dsp[0])
        dsp = dsp[1].split("月")
        Mon = int(dsp[0])
        dsp = dsp[1].split("日")
        Da = int(dsp[0])
    elif "昭和" in d:
        Nengou = "昭和"
        dsp = d.split("昭和")
        dsp = dsp[1].split("年")
        Nen = int(dsp[0])
        dsp = dsp[1].split("月")
        Mon = int(dsp[0])
        dsp = dsp[1].split("日")
        Da = int(dsp[0])
    elif "平成" in d:
        Nengou = "平成"
        dsp = d.split("平成")
        dsp = dsp[1].split("年")
        Nen = int(dsp[0])
        dsp = dsp[1].split("月")
        Mon = int(dsp[0])
        dsp = dsp[1].split("日")
        Da = int(dsp[0])
    elif "令和" in d:
        Nengou = "令和"
        dsp = d.split("令和")
        dsp = dsp[1].split("年")
        Nen = int(dsp[0])
        dsp = dsp[1].split("月")
        Mon = int(dsp[0])
        dsp = dsp[1].split("日")
        Da = int(dsp[0])
    if Nengou in omikuji:
        PlusYear = omikuji[Nengou]
        Dater = (
            str(PlusYear + Nen - 1) + "/" + str(Mon).zfill(2) + "/" + str(Da).zfill(2)
        )
        return Dater
    else:
        print("エラー")


if __name__ == "__main__":
    pass
