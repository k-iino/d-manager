from d_manager.quantity.quantity import NutrientQuantity
from d_manager.quantity.unit import Dimension
from d_manager.nutrient import Nutrient


class NutrientBuilder:
    """
    特定の栄養素を生成するためのビルダークラス

    栄養素毎に Nutrient クラスを継承するのではなく、ビルダーで栄養素を生成する。
    栄養素毎にその物理量の次元や単位、表示有効桁を設定する。
    ただし、物理量の値を計算した際の誤差処理は利用側の責任とする。
    """

    def __init__(self, name, dimension, unit, ndigits=0):
        # 栄養素の名前
        self.name = name
        # 単位
        self.dimension = dimension
        self.unit = unit
        # 表示有効桁（小数点N桁）
        self.ndigits = ndigits

    def build(self, magnitude, unit):
        """栄養素をビルドして返す"""
        dim = Dimension.get(unit)
        if dim != self.dimension:
            raise ValueError('{} は栄養素 {} の次元として不適切です。'.format(unit, self.name))
        q = NutrientQuantity(magnitude, unit).to(self.unit)
        n = Nutrient(self.name, q)
        n.ndigits = self.ndigits
        return n

    def build_from_str(self, input_str):
        q = NutrientQuantity.from_str(input_str)
        return self.build(q.m, q.u)
