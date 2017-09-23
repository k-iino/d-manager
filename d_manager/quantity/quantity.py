from d_manager.quantity import _Quantity
from d_manager.quantity.unit import Unit


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
