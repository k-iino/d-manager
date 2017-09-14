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

    # 単位の取得
    def test_get_quantity(self):
        """単位を作成出来るか"""
        values = (0, 0.0, 1, 1.0)
        string_formats = ('{}{}', '{} {}')
        # 使われることが予測される単位
        mass_units = (Unit.kilogram,
                      Unit.gram,
                      Unit.nanogram, Unit.microgram, Unit.milligram)
        volume_units = (Unit.liter,
                        Unit.milliliter)
        energy_units = (Unit.kilocalorie,
                        Unit.calorie,
                        Unit.kilojoule,
                        Unit.joule)
        # 文字列から作成
        for string_format in string_formats:
            for value in values:
                # 数値のみの文字列
                _input = string_format.format(value, '')
                _pq = Unit.get_quantity(_input)
                self.assertEqual(_pq.magnitude, value)
                self.assertEqual(_pq.units, Unit.dimensionless)
                # 数値のみの文字列に、単位指定あり
                # 無次元ではなく指定の単位の量だと判断する
                for unit in mass_units + volume_units + energy_units:
                    _pq = Unit.get_quantity(_input, units=unit)
                    self.assertEqual(_pq.magnitude, value)
                    self.assertEqual(_pq.units, unit)

                # 単位付きの文字列。 e.g. '1g', '1.0g'
                for unit in mass_units + volume_units + energy_units:
                    _input = string_format.format(value, unit)
                    _pq = Unit.get_quantity(_input)
                    self.assertEqual(_pq.magnitude, value)
                    self.assertEqual(_pq.units, unit)
                    # 単位変換あり
                    if Unit.is_mass(unit):
                        for _new_unit in mass_units:
                            _a = Unit.get_quantity(_input)
                            _b = Unit.get_quantity(_input, units=_new_unit)  # 変換あり
                            # 大きさは変わったが、量としては等しい
                            self.assertEqual(_a, _b)
                    elif Unit.is_volume(unit):
                        for _new_unit in volume_units:
                            _a = Unit.get_quantity(_input)
                            _b = Unit.get_quantity(_input, units=_new_unit)  # 変換あり
                            self.assertEqual(_a, _b)
                    elif Unit.is_energy(unit):
                        for _new_unit in energy_units:
                            _a = Unit.get_quantity(_input)
                            _b = Unit.get_quantity(_input, units=_new_unit)  # 変換あり
                            self.assertEqual(_a, _b)
                    else:
                        raise NotImplementedError

        # 数から作成
        for value in values:
            # 数値のみは無次元量
            _pq = Unit.get_quantity(value)
            self.assertEqual(_pq.magnitude, value)
            self.assertEqual(_pq.units, Unit.dimensionless)

            # 数値と単位から
            for unit in mass_units + volume_units + energy_units:
                # 数値と単位の指定あり
                # 無次元ではなく指定の単位の量だと判断する
                _pq = Unit.get_quantity(value, unit)
                self.assertEqual(_pq.magnitude, value)
                self.assertEqual(_pq.units, unit)

                # 数値から作成される場合は、第２引数で単位を指定したらその単位の量となるので
                # 単位から単位の変換はない

        # 既にある単位から作成
        for value in values:
            # 無次元の量から作成
            _src = Unit.get_quantity(value)
            _dst = Unit.get_quantity(_src)
            self.assertEqual(_src, _dst)
            self.assertEqual(_src.magnitude, _dst.magnitude)
            self.assertEqual(_src.units, _dst.units)

            for unit in mass_units + volume_units + energy_units:
                #  単位ありの量から新しい量を作成
                _src = Unit.get_quantity(value, unit)
                _dst = Unit.get_quantity(_src)
                self.assertEqual(_src, _dst)
                self.assertEqual(_src.magnitude, _dst.magnitude)
                self.assertEqual(_src.units, _dst.units)
                # 単位変換あり
                if Unit.is_mass(unit):
                    for _new_unit in mass_units:
                        _new = Unit.get_quantity(_src, units=_new_unit)  # 変換あり
                        # 大きさは変わったが、量としては等しい
                        self.assertEqual(_src, _new)
                elif Unit.is_volume(unit):
                    for _new_unit in volume_units:
                        _new = Unit.get_quantity(_src, units=_new_unit)  # 変換あり
                        self.assertEqual(_src, _new)
                elif Unit.is_energy(unit):
                    for _new_unit in energy_units:
                        _new = Unit.get_quantity(_src, units=_new_unit)  # 変換あり
                        self.assertEqual(_src, _new)
                else:
                    raise NotImplementedError


if __name__ == '__main__':
    unittest.main()
