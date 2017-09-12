from pint import UnitRegistry


class Unit:
    """単位を操作するクラス"""
    # 実際の物理量の操作は別のパッケージに委任している。

    # 異なる UnitRegistry 間だと量同士の演算が出来ないので
    # 全体でひとつの UnitRegistry を利用する。
    __reg = UnitRegistry()

    # 次元を示す文字列
    DIM_MASS = '[mass]'
    DIM_VOLUME = '[volume]'
    DIM_ENERGY = '[energy]'

    @classmethod
    def get_amount(cls, a):
        if isinstance(a, int) or isinstance(a, float):
            return cls.__reg.Quantity(a)
        elif isinstance(a, str):
            return cls.parse_expression(a)
        elif isinstance(a, cls.__reg.Quantity):
            return a
        else:
            raise ValueError('不適切な値。 type={}, value={}'.format(type(a), a))

    @classmethod
    def parse_expression(cls, e):
        return cls.__reg.parse_expression(e)

    @staticmethod
    def to_str(amount):
        return '{:~P}'.format(amount)

    @classmethod
    def check_dimensionality(cls, dim, amount):
        """単位の次元を確認する。"""
        amount = cls.get_amount(amount)
        a = cls.__reg.get_dimensionality(amount)
        m = cls.__reg.get_dimensionality(dim)
        return a == m

    @classmethod
    def is_mass(cls, amount):
        """量の次元は質量か"""
        return cls.check_dimensionality(cls.DIM_MASS, amount)

    @classmethod
    def is_volume(cls, amount):
        """量の次元は体積か"""
        return cls.check_dimensionality(cls.DIM_VOLUME, amount)

    @classmethod
    def is_energy(cls, amount):
        """量の次元はエネルギーか"""
        return cls.check_dimensionality(cls.DIM_ENERGY, amount)
