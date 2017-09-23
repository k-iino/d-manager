from d_manager.nutrient.builder import NutrientBuilder
from d_manager.quantity.unit import Unit
from d_manager.quantity.unit import Dimension


class BasicNutrientsProvider:
    """
    基本的な栄養素を生産するプロバイダ

    栄養素に関しては、食品表示基準（平成 27 年内閣府令第 10 号）において「一般加工食品」に対する義務表示の基本 5 項目の栄養素のクラスを定義した。
    ここでの基本 5 項目は熱量、たんぱく質、脂質、炭水化物、食塩相当量を指す。

    表示の際に用いる各栄養素の単位と小数部の有効桁（小数第N位）は
    「食品表示基準」と「日本食品標準成分表2015年版」での有効桁を参考にした。
    「食品表示基準」では、最低限表示すべき桁数が定められているが、より下の位を表示することを妨げていない。
    実際の市販食品では小数第1位までを表示するものが多いようだ。
    """

    def __init__(self):
        self.builders = dict()
        # 基本 5 項目の栄養素
        self._set_builder(name='energy',
                          dimension=Dimension.energy,
                          unit=Unit.kilocalorie,
                          ndigits=1)
        self._set_builder(name='protein',
                          dimension=Dimension.mass,
                          unit=Unit.gram,
                          ndigits=1)
        self._set_builder(name='lipid',
                          dimension=Dimension.mass,
                          unit=Unit.gram,
                          ndigits=1)
        self._set_builder(name='carbohydrate',
                          dimension=Dimension.mass,
                          unit=Unit.gram,
                          ndigits=1)
        self._set_builder(name='salt',
                          dimension=Dimension.mass,
                          unit=Unit.gram,
                          ndigits=3)  # 手元に小数第3位まで表示しているものがあったので

    def _set_builder(self, name, dimension, unit, ndigits):
        self.builders[name] = NutrientBuilder(name, dimension, unit, ndigits)

    def provide_from_str(self, name, amount_str):
        """指定した名前の栄養素を文字列から生成する"""
        # todo パース不可能な栄養素が合った場合は、独自例外を投げて呼び出し元に通知する
        return self.builders[name].build_from_str(amount_str)
