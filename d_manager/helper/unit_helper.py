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
