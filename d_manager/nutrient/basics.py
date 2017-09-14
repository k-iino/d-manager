from d_manager.helper.unit_helper import Unit
from d_manager.nutrient import BaseNutrient

"""
基本となる栄養素

栄養素に関しては、食品表示基準（平成 27 年内閣府令第 10 号）において「一般加工食品」に対する義務表示の基本 5 項目の栄養素のクラスを定義した。
ここでの基本 5 項目は熱量、たんぱく質、脂質、炭水化物、食塩相当量を指す。

表示の際に用いる各栄養素の単位と小数部の有効桁（小数第N位）は
「食品表示基準」と「日本食品標準成分表2015年版」での有効桁を見比べ、精度の低いものを採用した。
"""


class Energy(BaseNutrient):
    """熱量"""
    # 表示に用いる単位
    __units = Unit.kilocalorie
    # 小数部の有効桁（小数第N位）
    __significant_figure = 0

    def __init__(self, i):
        super(Energy, self).__init__('熱量', i, self.__units)


class Protein(BaseNutrient):
    """たんぱく質"""
    # 単位
    __units = Unit.gram
    # 小数部の有効桁（小数第N位）
    __significant_figure = 0

    def __init__(self, i):
        super(Protein, self).__init__('たんぱく質', i, self.__units)


class Lipid(BaseNutrient):
    """脂質"""
    # 単位
    __units = Unit.gram
    # 小数部の有効桁（小数第N位）
    __significant_figure = 0

    def __init__(self, i):
        super(Lipid, self).__init__('脂質', i, self.__units)


class Carbohydrate(BaseNutrient):
    """炭水化物"""
    # 単位
    __units = Unit.gram
    # 小数部の有効桁（小数第N位）
    __significant_figure = 0

    def __init__(self, i):
        super(Carbohydrate, self).__init__('炭水化物', i, self.__units)


class SaltEquivalent(BaseNutrient):
    """食塩相当量"""
    # 単位
    __units = Unit.gram
    # 小数部の有効桁（小数第N位）
    __significant_figure = 0

    def __init__(self, i):
        super(SaltEquivalent, self).__init__('食塩相当量', i, self.__units)
