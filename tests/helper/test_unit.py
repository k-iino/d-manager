import unittest

from pint.errors import UndefinedUnitError
from pint.errors import DimensionalityError

from d_manager.helper.unit_helper import Unit


class TestUnit(unittest.TestCase):
    def test_parse_expression(self):
        """文字列を物理量に正しく変換できるかどうか"""
        valid_magnitudes = (1, 1.0)
        valid_units = ('', 'dimensionless',
                       'g', 'kg',
                       'l', 'ml')
        valids = [str(m) + u
                  for m in valid_magnitudes
                  for u in valid_units]
        for v in valids:
            Unit.parse_expression(v)

        valid_quantity = Unit.parse_expression('1g')
        Unit.get_amount(valid_quantity)

        invalid_units = ('invalid unit',)
        invalids = [str(m) + u
                    for m in valid_magnitudes
                    for u in invalid_units]
        for i in invalids:
            with self.assertRaises(UndefinedUnitError):
                Unit.parse_expression(i)

    def test_to_str(self):
        """物理量が期待通りの形式の文字列になるか"""
        test_sets = (('1g', '1 g'),
                     ('1kg', '1 kg'),
                     ('1 gram', '1 g'),
                     ('1 kilogram', '1 kg'),
                     ('1l', '1 l'),
                     ('1kl', '1 kl'),
                     ('1 liter', '1 l'),
                     ('1 milliliter', '1 ml'),
                     )
        for s in test_sets:
            pq = Unit.parse_expression(s[0])
            self.assertEqual(Unit.to_str(pq), s[1])

    def test_calculation(self):
        """加算が可能か確認"""
        # operand, operand , excepted
        test_sets = (('1g', '2g', '3g'),
                     ('1.0g', '2.0g', '3g'),
                     ('1kg', '2g', '1002g'),
                     ('1g', '2kg', '2001g'),
                     ('1mg', '0.2g', '201mg'),
                     ('1l', '0.2l', '1200ml'),
                     ('100ml', '2l', '2100ml'),
                     )
        for s in test_sets:
            op1 = Unit.parse_expression(s[0])
            op2 = Unit.parse_expression(s[1])
            excepted = Unit.parse_expression(s[2])
            self.assertEqual(op1 + op2, excepted)

        invalids = (('1g', '2ml'),
                    ('1.0g', '2.0l'))
        for s in invalids:
            op1 = Unit.parse_expression(s[0])
            op2 = Unit.parse_expression(s[1])
            with self.assertRaises(DimensionalityError):
                op1 + op2

    def test_check_dimensionality(self):
        """次元の確認ヘルパーメソッドの確認"""
        # 考えられる次元は質量、体積、エネルギーとその単位の組み合わせ。
        # ここでは、食品表示法と食品表示基準で定められている組み合わせで確認する。
        mass_units = ('ug', 'mg', 'g', 'kg')
        volume_units = ('ml', 'l')
        energy_units = ('kcal', 'J')
        # 特定の次元の確認用メソッド群
        mass_checker = Unit.is_mass
        volume_checker = Unit.is_volume
        energy_checker = Unit.is_energy

        # 正常系
        # 正常な次元と単位の組み合わせ
        valid_unit_pattern = {Unit.DIM_MASS: mass_units,
                              Unit.DIM_VOLUME: volume_units,
                              Unit.DIM_ENERGY: energy_units}
        # 正常な次元と確認用関数の組み合わせ
        valid_checker_pattern = {Unit.DIM_MASS: mass_checker,
                                 Unit.DIM_VOLUME: volume_checker,
                                 Unit.DIM_ENERGY: energy_checker}
        # 正常な組み合わせでテスト
        # Test for Unit.check_dimensionality
        for dim, units in valid_unit_pattern.items():
            for unit in units:
                self.assertTrue(Unit.check_dimensionality(dim, unit))
        # Test for Unit checkers
        for dim, checker in valid_checker_pattern.items():
            for valid_unit in valid_unit_pattern[dim]:
                self.assertTrue(checker(valid_unit))

        # 異常系
        # 正しくない次元と単位の組み合わせ
        invalid_unit_pattern = {Unit.DIM_MASS: volume_units + energy_units,
                                Unit.DIM_VOLUME: mass_units + energy_units,
                                Unit.DIM_ENERGY: mass_units + volume_units}
        # 正しくない次元と確認用関数の組み合わせ
        invalid_checker_pattern = {Unit.DIM_MASS: (volume_checker, energy_checker),
                                   Unit.DIM_VOLUME: (mass_checker, energy_checker),
                                   Unit.DIM_ENERGY: (mass_checker, volume_checker)}

        # Test for Unit.check_dimensionality
        for dim, invalid_units in invalid_unit_pattern.items():
            for unit in invalid_units:
                self.assertFalse(Unit.check_dimensionality(dim, unit))
        # Test for Unit checkers
        for dim, invalid_checkers in invalid_checker_pattern.items():
            # 正常な単位を、間違ったチェック関数に入れる
            for valid_unit in valid_unit_pattern[dim]:
                for invalid_checker in invalid_checkers:
                    self.assertFalse(invalid_checker(valid_unit))

if __name__ == '__main__':
    unittest.main()
