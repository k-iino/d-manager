import unittest
from pint.errors import DimensionalityError

from d_manager.nutrient import BaseNutrient
from d_manager.helper.unit_helper import Unit


class MyTestCase(unittest.TestCase):
    values = (0, 0.0, 1, 1.0, 1.23, 1.234)
    ndigits = (0, 1)  # 表示時の精度の桁（小数点n桁まで有効かを表す）ただし、表示以外では n+1 桁で扱われる
    mass_units = (Unit.kilogram,
                  Unit.gram,
                  Unit.nanogram, Unit.microgram, Unit.milligram)
    volume_units = (Unit.liter,
                    Unit.milliliter)
    energy_units = (Unit.kilocalorie,
                    Unit.calorie,
                    Unit.kilojoule,
                    Unit.joule)

    @staticmethod
    def ratio_of_units(src_unit, dst_unit):
        """同次元の単位同士の比率を得る"""
        _src_pq = Unit.unit_registry().Quantity(1, src_unit)
        return _src_pq.to(dst_unit).magnitude

    def test_init(self):
        """各種コンストラクタのテスト"""
        # 生成した BaseNutrient と予想値の比較用関数
        def _assert_base_nutrient(_base_nutrient, _units, _magnitude, _ndigits):
            self.assertEqual(_units, _base_nutrient.units)
            # 表示時以外では n+1 桁に丸め込まれる
            _excepted = round(_magnitude, _ndigits + 1)
            self.assertEqual(_excepted, _base_nutrient.magnitude)

        # 量を数値として渡す
        for v in self.values:
            for n in self.ndigits:
                # 単位の指定がない場合、無次元量になっているか
                bn = BaseNutrient(v, units=None, ndigits=n)
                _assert_base_nutrient(bn, Unit.dimensionless, v, n)

                # 単位の指定がある
                for unit in self.mass_units + self.volume_units + self.energy_units:
                    bn = BaseNutrient(v, units=unit, ndigits=n)
                    _assert_base_nutrient(bn, unit, v, n)

        # 文字列として量を渡す場合
        str_formats = ('{} {}', '{}{}')
        # 複数の文字列形式で、全ての値で、全ての精度で
        for str_format in str_formats:
            for v in self.values:
                for n in self.ndigits:
                    # 単位の指定がない場合、無次元量になっているか
                    input_str = str_format.format(v, Unit.dimensionless)
                    bn = BaseNutrient(input_str, ndigits=n)
                    _assert_base_nutrient(bn, Unit.dimensionless, v, n)
                    # 単位の指定がある場合、ただし同じ無次元
                    bn = BaseNutrient(input_str, units=Unit.dimensionless, ndigits=n)
                    _assert_base_nutrient(bn, Unit.dimensionless, v, n)
                    # 無次元を他の次元には変換出来ない
                    with self.assertRaises(DimensionalityError):
                        BaseNutrient(input_str, units=Unit.joule, ndigits=n)

                    # 単位の指定がある場合
                    # 入力文字列に含まれる単位と、指定の単位が異なる場合、単位変換がされているかも確認する
                    for unit in self.mass_units + self.volume_units + self.energy_units:
                        input_str = str_format.format(v, unit)
                        # 単位の指定がない場合、文字列内から正しく単位を取得できているか
                        bn = BaseNutrient(input_str, units=None, ndigits=n)
                        _assert_base_nutrient(bn, unit, v, n)
                        # 単位の指定がある場合、正しく単位を変換できているか
                        if unit in self.mass_units:
                            # mass -> mass
                            for dst_unit in self.mass_units:
                                bn = BaseNutrient(input_str, units=dst_unit, ndigits=n)
                                # 単位変換が行われたので、magnitude も変化している
                                scaled_magnitude = self.ratio_of_units(unit, dst_unit) * v
                                _assert_base_nutrient(bn, dst_unit, scaled_magnitude, n)
                            # mass -> other
                            for other_unit in self.energy_units + self.volume_units:
                                with self.assertRaises(DimensionalityError):
                                    BaseNutrient(input_str, units=other_unit, ndigits=n)
                        elif unit in self.volume_units:
                            # volume -> volume
                            for dst_unit in self.volume_units:
                                bn = BaseNutrient(input_str, units=dst_unit, ndigits=n)
                                # 単位変換が行われたので、magnitude も変化している
                                scaled_magnitude = self.ratio_of_units(unit, dst_unit) * v
                                _assert_base_nutrient(bn, dst_unit, scaled_magnitude, n)
                            # volume -> other
                            for other_unit in self.energy_units + self.mass_units:
                                with self.assertRaises(DimensionalityError):
                                    BaseNutrient(input_str, units=other_unit, ndigits=n)
                        elif unit in self.energy_units:
                            # energy -> energy
                            for dst_unit in self.energy_units:
                                bn = BaseNutrient(input_str, units=dst_unit, ndigits=n)
                                # 単位変換が行われたので、magnitude も変化している
                                scaled_magnitude = self.ratio_of_units(unit, dst_unit) * v
                                _assert_base_nutrient(bn, dst_unit, scaled_magnitude, n)
                            # energy -> other
                            for other_unit in self.volume_units + self.mass_units:
                                with self.assertRaises(DimensionalityError):
                                    BaseNutrient(input_str, units=other_unit, ndigits=n)

    def test_add(self):
        """加算が正しく出来るか"""
        def _check_sum(left_operands, right_operands, invalid_operands):
            """確認用"""
            for left_operand in left_operands:
                for right_operand in right_operands:
                    for n in self.ndigits:
                        # print('{} + {}'.format(left_operand, right_operand))
                        left_bn = BaseNutrient(left_operand, ndigits=n)
                        right_bn = BaseNutrient(right_operand, ndigits=n)
                        actual_sum = left_bn + right_bn
                        # 計算後は左側の被演算子の単位になっているか
                        self.assertEqual(actual_sum.units, left_bn.units)
                        # 計算後の値
                        excepted_sum_magnitude = left_bn.magnitude + (right_bn.magnitude
                                                                      / self.ratio_of_units(left_bn.units,
                                                                                            right_bn.units))
                        # 計算結果は、誤差を減らすために表示用の精度より +1 桁多めで計算しておく
                        excepted_sum_magnitude = round(excepted_sum_magnitude, n + 1)
                        self.assertEqual(excepted_sum_magnitude, actual_sum.magnitude)
                # 異なる単位間での加算はエラー
                for invalid_operand in invalid_operands:
                    left_bn = BaseNutrient(left_operand)
                    right_bn = BaseNutrient(invalid_operand)
                    with self.assertRaises(DimensionalityError):
                        left_bn + right_bn
                # 直接数値を加算するのはエラー
                for value in self.values:
                    left_bn = BaseNutrient(left_operand)
                    with self.assertRaises(NotImplementedError):
                        left_bn + value

        # 各単位での被演算子の作成
        energy_operands = tuple(('{} {}'.format(_v, _u) for _v in self.values
                                 for _u in self.energy_units))
        volume_operands = tuple(('{} {}'.format(_v, _u) for _v in self.values
                                 for _u in self.volume_units))
        mass_operands = tuple(('{} {}'.format(_v, _u) for _v in self.values
                               for _u in self.mass_units))

        _check_sum(energy_operands, energy_operands, volume_operands + mass_operands)
        _check_sum(mass_operands, mass_operands, energy_operands + volume_operands)
        _check_sum(volume_operands, volume_operands, energy_operands + mass_operands)

    def test_mul(self):
        """乗算が正しく出来るか"""
        def _check_mul(left_operands, right_operands, invalid_operands):
            """乗算確認用"""
            # 栄養素同士の乗算は栄養素と数値との掛け算しか認めていない
            for left_operand in left_operands:
                for right_operand in right_operands:
                    left_bn = BaseNutrient(left_operand)
                    right_bn = BaseNutrient(right_operand)
                    # 同じ次元の量を持つ栄養素同士の乗算はエラー
                    with self.assertRaises(NotImplementedError):
                        left_bn * right_bn
                # 異なる単位での乗算はエラー
                for invalid_operand in invalid_operands:
                    left_bn = BaseNutrient(left_operand)
                    right_bn = BaseNutrient(invalid_operand)
                    with self.assertRaises(NotImplementedError):
                        left_bn * right_bn
                # 直接数値を乗算することのみが認められている
                for value in self.values:
                    for n in self.ndigits:
                        left_bn = BaseNutrient(left_operand, ndigits=n)
                        answer = left_bn * value
                        if not isinstance(answer, BaseNutrient):
                            raise ValueError

                        # 計算後は左側の被演算子の単位になっているか
                        self.assertEqual(answer.units, left_bn.units)
                        # 計算結果は、誤差を減らすために表示用の精度より +1 桁多めで計算しておく
                        excepted = left_bn.magnitude * value
                        excepted = round(excepted, n + 1)
                        self.assertEqual(answer.magnitude, excepted)

        # 各単位での被演算子の作成
        energy_operands = tuple(('{} {}'.format(_v, _u) for _v in self.values
                                 for _u in self.energy_units))
        volume_operands = tuple(('{} {}'.format(_v, _u) for _v in self.values
                                 for _u in self.volume_units))
        mass_operands = tuple(('{} {}'.format(_v, _u) for _v in self.values
                               for _u in self.mass_units))

        _check_mul(energy_operands, energy_operands, volume_operands + mass_operands)
        _check_mul(mass_operands, mass_operands, energy_operands + volume_operands)
        _check_mul(volume_operands, volume_operands, energy_operands + mass_operands)


if __name__ == '__main__':
    unittest.main()
