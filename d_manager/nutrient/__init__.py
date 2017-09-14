from d_manager.helper.unit_helper import Unit


class BaseNutrient:
    """栄養素のベースクラス"""

    _ureg = Unit.unit_registry()

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
        self.__quantity = self._ureg.Quantity(rounded_magnitude, self.__units)

    def __add__(self, other):
        if isinstance(other, BaseNutrient):
            _q = self.__quantity + other.__quantity
            _q.to(self.__units)
            return BaseNutrient(_q.magnitude, self.__units, self.__significant_figure)
        else:
            raise NotImplementedError

    def __mul__(self, other):
        if isinstance(other, int) or isinstance(other, float):
            _m = self.__quantity.magnitude * other
            return BaseNutrient(_m, self.__units, self.__significant_figure)
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
