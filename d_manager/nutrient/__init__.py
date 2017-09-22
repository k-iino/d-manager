from d_manager.quantity.unit import Unit
from d_manager.quantity.unit import Dimension


class Nutrient:
    def __init__(self, name, quantity):
        self.name = name
        self.quantity = quantity

    def __add__(self, other):
        if isinstance(other, Nutrient):
            self.quantity += other.quantity
            return self
        else:
            msg = '栄養素同士以外の加算は出来ません。'
            raise ValueError(msg)

    def __mul__(self, other):
        if isinstance(other, (int, float)):
            self.quantity *= other
            return self
        else:
            msg = 'この型を栄養素に乗算することは出来ません。 {}'.format(other)
            raise ValueError(msg)

# class EnergyBuilder(NutrientBuilder):
#     name_of_nutrient = 'energy'
#     # デフォルト値
#     default_unit = Unit.kilocalorie
#     default_ndigits = 1
#
#     def __init__(self, unit=default_unit, ndigits=default_ndigits):
#         super(EnergyBuilder, self).__init__(self.name_of_nutrient, Dimension.energy,
#                                             unit, ndigits)

class BaseNutrient:
    """栄養素のベースクラス"""
    def __init__(self, input_, units=None, ndigits=0):
        # 表示用の小数部の有効桁（小数第N位）
        self.__significant_figure = ndigits
        # 保存、計算時は、精度が落ちることを防ぐために表示時の有効桁より1桁多い桁を用いる
        self.__significant_figure_for_calc = ndigits + 1
        # 物理量
        self.__quantity = Unit.get_quantity(input_, units)
        self.__units = self.__quantity.units

        # 物理量の大きさを計算用の精度に丸め込む
        rounded_magnitude = round(self.__quantity.magnitude, self.__significant_figure_for_calc)
        self.__quantity = Unit.unit_registry().Quantity(rounded_magnitude, self.__units)

    def __add__(self, other):
        if isinstance(other, BaseNutrient):
            _q = self.__quantity + other.__quantity
            _q.to(self.__units)
            # Pickle から元に戻した、栄養素は自身が参照している pint.UnitRegister が異なるため
            # 単位の各種変換や比較が正しく出来ない、そのため文字列に変換してから現在の UnitRegister で Unit を作成しなおしている。
            return BaseNutrient(_q.magnitude, str(self.__units), self.__significant_figure)
        else:
            raise NotImplementedError

    def __mul__(self, other):
        if isinstance(other, int) or isinstance(other, float):
            _m = self.__quantity.magnitude * other
            # Pickle から元に戻した、栄養素は自身が参照している pint.UnitRegister が異なるため
            # 単位の各種変換や比較が正しく出来ない、そのため文字列に変換してから現在の UnitRegister で Unit を作成しなおしている。
            return BaseNutrient(_m, str(self.__units), self.__significant_figure)
        # 次元のある量同士の計算だと次元が変わってしまうので
        # 栄養素同士の掛け算はここでは意義のない行為である。
        # elif isinstance(other, BaseNutrient):
        #     _q = self.__quantity * other.__quantity
        #     _q.to(self.__units)
        #     return BaseNutrient(self.name, _q.magnitude, self.__units, self.__significant_figure)
        else:
            raise NotImplementedError

    def __str__(self):
        """str 化"""
        # 表示用の精度に丸め込んでから表示する。
        _rounded = round(self.__quantity.magnitude, self.__significant_figure)
        if self.__significant_figure == 0:
            _rounded = int(_rounded)

        return '{} {:~P}'.format(_rounded, self.__quantity.units)

    @property
    def magnitude(self):
        """Quantity's magnitude. Long form for `m`
        """
        # コンストラクタ内、計算時に計算用の精度に丸め込んでいるのでそのまま返してよい
        return self.__quantity.magnitude

    @property
    def m(self):
        """Quantity's magnitude. Long form for `m`
        """
        return self.__quantity.magnitude

    @property
    def units(self):
        """Quantity's units. Long form for `u`
        """
        return self.__quantity.units

    @property
    def u(self):
        """Quantity's units. Short form for `units`
        """
        return self.__quantity.units

    @property
    def significant_figure(self):
        """significant_figure"""
        return self.__significant_figure


class HasDefaultSignificantFigure:
    """デフォルトの有効桁を所持することを表す"""
    # 小数部の有効桁（小数第N位）
    _default_significant_figure = 0

    @classmethod
    def default_significant_figure(cls):
        return cls._default_significant_figure


class HasDefaultUnit:
    """デフォルトの単位を所持することを表す"""
    _default_units = Dimension.dimensionless

    @classmethod
    def default_units(cls):
        return cls._default_units
