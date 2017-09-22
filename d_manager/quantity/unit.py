from d_manager.quantity import _ureg


class Dimension:
    """次元に関するクラス"""
    # 単位の次元
    dimensionless = _ureg.dimensionless
    energy = _ureg.get_dimensionality('[energy]')
    mass = _ureg.get_dimensionality('[mass]')
    volume = _ureg.get_dimensionality('[volume]')

    @staticmethod
    def get(i):
        """次元を得る"""
        _q = Unit.get(i)
        return _ureg.get_dimensionality(_q)

    @classmethod
    def is_mass(cls, i):
        """量の次元は質量か"""
        return cls.get(i) == cls.mass

    @classmethod
    def is_volume(cls, i):
        """量の次元は体積か"""
        return cls.get(i) == cls.volume

    @classmethod
    def is_energy(cls, i):
        """量の次元はエネルギーか"""
        return cls.get(i) == cls.energy


class Unit:    
    """単位を表現するクラス"""
    # energy
    calorie = _ureg.calorie
    kilocalorie = _ureg.kilocalorie
    joule = _ureg.joule
    kilojoule = _ureg.kilojoule
    # mass
    kilogram = _ureg.kilogram
    gram = _ureg.gram
    milligram = _ureg.milligram
    microgram = _ureg.microgram
    nanogram = _ureg.nanogram
    # volume
    liter = _ureg.liter
    milliliter = _ureg.milliliter

    @staticmethod
    def get(i):
        """与えられた入力値から単位を作成して返す"""
        if isinstance(i, _ureg.Unit):
            return i
        elif isinstance(i, _ureg.Quantity):
            return i.units
        elif isinstance(i, str):
            return _ureg.parse_expression(i).units
        # None を無理やり無次元量に置き換えると、呼び出し元で予想しない単位変換が起きる。
        # elif units is None:
        #     return Dimension.dimensionless
        else:
            raise NotImplementedError(i)

    # fixme 要らないかも
    # @classmethod
    # def unit_registry(cls):
    #     return _ureg
