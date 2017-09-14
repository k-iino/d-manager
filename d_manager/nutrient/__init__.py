from d_manager.helper.unit_helper import Unit


class BaseNutrient:
    """栄養素のベースクラス"""

    _ureg = Unit.unit_registry()

    def __init__(self, name, quantity, units=None, ndigits=0):
        self.name = name
        # 表示用の小数部の有効桁（小数第N位）
        self.__significant_figure = ndigits
        # 保存、計算時は、精度が落ちることを防ぐために表示時の有効桁より1桁多い桁を用いる
        self.__significant_figure_for_calc = ndigits + 1
        # 物理量
        if isinstance(quantity, int) or isinstance(quantity, float):
            if units is None:
                # 単位の指定がなければ無次元だと解釈する
                self.__units = Unit.dimensionless
                self.__quantity = self._ureg.Quantity(quantity, self.__units)
            else:
                # 指定があった次元の大きさだと解釈する
                self.__units = units
                self.__quantity = self._ureg.Quantity(quantity, self.__units)
        elif isinstance(quantity, str):
            if units is None:
                # 生成した物理量の次元を採用
                self.__quantity = self._ureg.parse_expression(quantity)
                self.__units = self.__quantity.units
            else:
                # 生成した物理量の次元を指定があったものに置き換える
                self.__units = units
                self.__quantity = self._ureg.parse_expression(quantity).to(self.__units)
        # BaseNutrient が個別に呼ばれることはなく、また、子クラスである各栄養素のクラスは
        # このコンストラクタに Quantity のオブジェクトを渡すことはないので、この判定は不要である。
        # elif isinstance(quantity, self._ureg.Quantity):
        #     self.__quantity = quantity
        #     if units is not None:
        #         # 指定された次元に変換する
        #         self.__units = units
        #         self.__quantity = self._ureg.parse_expression(quantity).to(self.__units)
        #     pass
        else:
            raise ValueError

        # 物理量の大きさを計算用の精度に丸め込む
        rounded_magnitude = round(self.__quantity.magnitude, self.__significant_figure_for_calc)
        self.__quantity = self._ureg.Quantity(rounded_magnitude, self.__units)

    def __add__(self, other):
        if isinstance(other, BaseNutrient):
            _q = self.__quantity + other.__quantity
            _q.to(self.__units)
            return BaseNutrient(self.name, _q.magnitude, self.__units, self.__significant_figure)
        else:
            raise NotImplementedError

    def __mul__(self, other):
        if isinstance(other, int) or isinstance(other, float):
            _q = self.__quantity * other
            _q.to(self.__units)
            return BaseNutrient(self.name, _q.magnitude, self.__units, self.__significant_figure)
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
        _rounded = '{} {}'.format(round(self.__quantity.magnitude, self.__significant_figure),
                                  self.__quantity.units)
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
