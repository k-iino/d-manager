from d_manager.quantity import _ureg
from d_manager.quantity.unit import Unit


class _Quantity:
    """
    物理量のクラス

    pint の物理量クラスの簡易的なラッパ。
    """
    def __init__(self, magnitude, unit):
        self.q = _ureg.Quantity(magnitude, unit)

    def to(self, unit):
        """単位を変換する"""
        self.q = self.q.to(unit)
        return self

    def round(self, ndigit):
        """物理量の値を小数点以下第 N 位に丸め込む"""
        m = round(self.q.m, ndigit)
        self.q = _ureg.Quantity(m, self.q.u)
        return self

    def __str__(self):
        return '{:~P}'.format(self.q)

    def __add__(self, other):
        # pint を利用して生成した Quantity や Unit は同一の UnitRegister インスタンスから
        # 生成したもの同士でないと比較や各種演算が出来ない。
        # そのため、Pickle 形式などでシリアライズした Quantity や Unit をデシリアライズして
        # 再利用しようとするとエラーが発生する。
        # そのため、シリアライズをする場合は物理量の演算か、入出力の実装を変更する必要がある。
        self.q += other.q
        return self

    def __mul__(self, other):
        self.q *= other
        return self

    @classmethod
    def from_str(cls, input_str):
        _pq = _ureg.parse_expression(input_str)
        return cls(_pq.magnitude, _pq.units)

    @property
    def magnitude(self):
        """Quantity's magnitude. Long form for `m`
        """
        return self.q.magnitude

    @property
    def m(self):
        """Quantity's magnitude. Short form for `m`
        """
        return self.q.magnitude

    @property
    def unit(self):
        """Quantity's units. Long form for `u`
        """
        return self.q.units

    @property
    def u(self):
        """Quantity's units. Short form for `units`
        """
        return self.q.units

    # fixme or deleteme. 不必要か
    # @classmethod
    # def __numeric_value_to_quantity(cls, num, units=None):
    #     if units is None:
    #         # 単位の指定がなければ無次元だと解釈する
    #         _units = Dimension.dimensionless
    #         return _Quantity(num, _units)
    #     else:
    #         # 指定があった次元の大きさだと解釈する
    #         _units = Unit.get(units)
    #         return _Quantity(num, _units)
    #
    # @classmethod
    # def from_str(cls, input_string, units=None):
    #     """文字列を単位に変換する。"""
    #     _pq = _ureg.parse_expression(input_string)
    #
    #     # parse_expression の仕様で '1' や '1.0' が、渡された場合は
    #     # 無次元の量が返るのではなく、単に int や float の値が返るのでよろしくない
    #     if isinstance(_pq, (int, float)):
    #         # 指定された単位があれば、その単位の量を求められていると解釈している
    #         return cls.__numeric_value_to_quantity(_pq, units)
    #     elif isinstance(_pq, _ureg.Quantity):
    #         # 単位に指定があったら単位に置き換える
    #         if units is not None:
    #             _units = Unit.get(units)
    #             _pq = _pq.to(_units)
    #             return _Quantity(_pq.m, _pq.u)
    #         else:
    #             return _Quantity(_pq.m, _pq.u)
    #     else:
    #         raise ValueError("{} は物理量に変換できません。".format(input_string))


class NutrientQuantity(_Quantity):
    """栄養素の物理量"""
    # 許容される単位
    energy_units = (Unit.calorie, Unit.kilocalorie,
                    Unit.joule, Unit.kilojoule)
    mass_units = (Unit.gram,
                  Unit.kilogram,
                  Unit.nanogram, Unit.microgram, Unit.milligram)

    def __init__(self, magnitude, unit):
        if unit not in self.energy_units + self.mass_units:
            raise ValueError('{} は不適切な単位です。'.format(unit))

        super(NutrientQuantity, self).__init__(magnitude, unit)


class FoodQuantity(_Quantity):
    """食品の物理量"""
    # 日本食品標準成分表2015年版では食品単位は全て 100g である。
    # また、「食品表示基準」によると一般加工食品の食品単位で認められる単位は質量か体積の二つ。
    mass_units = (Unit.gram,
                  Unit.kilogram,
                  Unit.nanogram, Unit.microgram, Unit.milligram)
    volume_units = (Unit.liter,
                    Unit.milliliter)

    def __init__(self, magnitude, unit):
        if unit not in self.mass_units + self.volume_units:
            raise ValueError('{} は不適切な単位です。'.format(unit))

        super(FoodQuantity, self).__init__(magnitude, unit)
