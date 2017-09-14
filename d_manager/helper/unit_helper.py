from pint import UnitRegistry


class Unit:    
    """単位を表現するクラス"""
    
    # 実際の物理量の操作は別のパッケージに委任している。
    # 異なる UnitRegistry 間だと量同士の演算が出来ないので
    # 各種演算がされる量を持つクラスは一つの UnitRegistry を利用する必要がある。
    __ureg = UnitRegistry()

    # 単位の次元
    __energy_dim = __ureg.get_dimensionality('[energy]')
    __mass_dim = __ureg.get_dimensionality('[mass]')
    __volume_dim = __ureg.get_dimensionality('[volume]')

    # unitless, dimensionless
    dimensionless = __ureg.dimensionless
    # energy
    calorie = __ureg.calorie
    kilocalorie = __ureg.kilocalorie
    joule = __ureg.joule
    kilojoule = __ureg.kilojoule
    # mass
    kilogram = __ureg.kilogram
    gram = __ureg.gram
    milligram = __ureg.milligram
    microgram = __ureg.microgram
    nanogram = __ureg.nanogram
    # volume
    liter = __ureg.liter
    milliliter = __ureg.milliliter

    @classmethod
    def __get_unit(cls, units):
        if isinstance(units, cls.__ureg.Unit):
            return units
        elif isinstance(units, str):
            cls.__ureg.parse_expression(units)
        # None を無理やり無次元量に置き換えると、呼び出し元で予想しない単位変換が起きる。
        # elif units is None:
        #     return cls.dimensionless
        else:
            raise NotImplementedError(units)

    @classmethod
    def __numeric_value_to_quantity(cls, num, units=None):
        if units is None:
            # 単位の指定がなければ無次元だと解釈する
            _units = Unit.dimensionless
            return cls.__ureg.Quantity(num, _units)
        else:
            # 指定があった次元の大きさだと解釈する
            _units = cls.__get_unit(units)
            return cls.__ureg.Quantity(num, _units)

    @classmethod
    def __str_to_quantity(cls, input_string, units=None):
        """文字列を単位に変換する。"""
        _pq = cls.__ureg.parse_expression(input_string)

        # parse_expression の仕様で '1' や '1.0' が、渡された場合は
        # 無次元の量が返るのではなく、単に int や float の値が返るのでよろしくない
        if isinstance(_pq, int) or isinstance(_pq, float):
            # 指定された単位があれば、その単位の量を求められていると解釈している
            return cls.__numeric_value_to_quantity(_pq, units)
        elif isinstance(_pq, cls.__ureg.Quantity):
            # 単位に指定があったら単位に置き換える
            if units is not None:
                _units = cls.__get_unit(units)
                return _pq.to(_units)
            else:
                return _pq
        else:
            raise ValueError

    @classmethod
    def get_quantity(cls, input_, units=None):
        if isinstance(input_, cls.__ureg.Quantity):
            # 指定があった単位に置き換える
            if units is not None:
                _units = cls.__get_unit(units)
                return input_.to(_units)
            else:
                # そのまま返す？新しい量を作成する？
                return input_
        elif isinstance(input_, str):
            return cls.__str_to_quantity(input_, units)
        elif isinstance(input_, int) or isinstance(input_, float):
            # 指定があった単位で量を作成する。
            # None は無次元とする。
            return cls.__numeric_value_to_quantity(input_, units)
        else:
            raise ValueError

    @classmethod
    def unit_registry(cls):
        return cls.__ureg

    @classmethod
    def is_mass(cls, q):
        """量の次元は質量か"""
        return cls.__ureg.get_dimensionality(q) == cls.__mass_dim

    @classmethod
    def is_volume(cls, q):
        """量の次元は体積か"""
        return cls.__ureg.get_dimensionality(q) == cls.__volume_dim

    @classmethod
    def is_energy(cls, q):
        """量の次元はエネルギーか"""
        return cls.__ureg.get_dimensionality(q) == cls.__energy_dim
