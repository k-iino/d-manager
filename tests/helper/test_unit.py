import unittest
import pint

from d_manager.helper.unit_helper import Unit


class UnitTestCase(unittest.TestCase):
    """単位"""
    def test_call(self):
        """呼び出せるか"""
        # registry
        self.assertIsInstance(Unit.unit_registry(), pint.UnitRegistry)
        # energy
        calorie = Unit.calorie
        kilocalorie = Unit.kilocalorie
        joule = Unit.joule
        kilojoule = Unit.kilojoule
        energy_units = (calorie, kilocalorie, joule, kilocalorie)
        for energy_unit in energy_units:
            self.assertTrue(Unit.is_energy(energy_unit))
        # mass
        gram = Unit.gram
        kilogram = Unit.kilogram
        milligram = Unit.milligram
        microgram = Unit.microgram
        nanogram = Unit.nanogram
        mass_units = (gram, kilogram, milligram, microgram, nanogram)
        for unit in mass_units:
            self.assertTrue(Unit.is_mass(unit))
        # volume
        liter = Unit.liter
        milliliter = Unit.milliliter
        volume_units = (liter, milliliter)
        for unit in volume_units:
            self.assertTrue(Unit.is_volume(unit))


if __name__ == '__main__':
    unittest.main()
