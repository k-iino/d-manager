from d_manager.helper.unit_helper import Unit
from d_manager.nutrient import BaseNutrient
from d_manager.nutrient import HasDefaultSignificantFigure
from d_manager.nutrient import HasDefaultUnit

"""
基本となる栄養素

栄養素に関しては、食品表示基準（平成 27 年内閣府令第 10 号）において「一般加工食品」に対する義務表示の基本 5 項目の栄養素のクラスを定義した。
ここでの基本 5 項目は熱量、たんぱく質、脂質、炭水化物、食塩相当量を指す。

表示の際に用いる各栄養素の単位と小数部の有効桁（小数第N位）は
「食品表示基準」と「日本食品標準成分表2015年版」での有効桁を参考にした。
「食品表示基準」では、最低限表示すべき桁数が定められているが、より下の位を表示することを妨げていない。
実際の市販食品では小数第1位までを表示するものが多いようだ。
"""


class Energy(BaseNutrient, HasDefaultSignificantFigure, HasDefaultUnit):
    """熱量"""
    name = '熱量'
    # 表示に用いる単位
    _default_units = Unit.kilocalorie
    # 小数部の有効桁（小数第N位）
    _default_significant_figure = 1

    def __init__(self, i):
        super(Energy, self).__init__(i, self._default_units,
                                     self._default_significant_figure)


class Protein(BaseNutrient, HasDefaultSignificantFigure, HasDefaultUnit):
    """たんぱく質"""
    name = 'たんぱく質'
    # 単位
    _default_units = Unit.gram
    # 小数部の有効桁（小数第N位）
    _default_significant_figure = 1

    def __init__(self, i):
        super(Protein, self).__init__(i, self._default_units,
                                      self._default_significant_figure)


class Lipid(BaseNutrient, HasDefaultSignificantFigure, HasDefaultUnit):
    """脂質"""
    name = '脂質'
    # 単位
    _default_units = Unit.gram
    # 小数部の有効桁（小数第N位）
    _default_significant_figure = 1

    def __init__(self, i):
        super(Lipid, self).__init__(i, self._default_units,
                                    self._default_significant_figure)


class Carbohydrate(BaseNutrient, HasDefaultSignificantFigure, HasDefaultUnit):
    """炭水化物"""
    name = '炭水化物'
    # 単位
    _default_units = Unit.gram
    # 小数部の有効桁（小数第N位）
    _default_significant_figure = 1

    def __init__(self, i):
        super(Carbohydrate, self).__init__(i, self._default_units,
                                           self._default_significant_figure)


class SaltEquivalent(BaseNutrient, HasDefaultSignificantFigure, HasDefaultUnit):
    """食塩相当量"""
    name = '食塩相当量'
    # 単位
    _default_units = Unit.gram
    # 小数部の有効桁（小数第N位）
    _default_significant_figure = 3

    def __init__(self, i):
        super(SaltEquivalent, self).__init__(i, self._default_units,
                                             self._default_significant_figure)
