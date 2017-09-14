import unittest

from d_manager.food import BaseFood
from d_manager.nutrient.basics import Energy, Protein, Lipid, Carbohydrate, SaltEquivalent
from d_manager.helper.unit_helper import Unit


class BaseFoodTest(unittest.TestCase):
    valid_food_name = 'food_name'
    values = (0, 1, 1.1)
    # 想定される文字フォーマット
    string_formats = ('{}{}', '{} {}')
    # 食品の量で認められている単位
    mass_units = (Unit.microgram, Unit.milligram, Unit.gram, Unit.kilogram)
    volume_units = (Unit.milliliter, Unit.liter)
    # 食品の量で認められていない単位
    invalid_units = (Unit.calorie, Unit.joule)

    def test_init(self):
        """コンストラクタの確認"""
        # 文字列の量から作成
        for str_format in self.string_formats:
            for value in self.values:
                # 認められる単位は重量か体積
                for valid_unit in self.mass_units + self.volume_units:
                    BaseFood(self.valid_food_name,
                             str_format.format(value, valid_unit))
                for invalid_unit in self.invalid_units:
                    with self.assertRaises(ValueError):
                        BaseFood(self.valid_food_name,
                                 str_format.format(value, invalid_unit))

        # 数値のみのよる、つまり無次元量による指定は認められていない
        for value in self.values:
            with self.assertRaises(ValueError):
                BaseFood(self.valid_food_name, value)

        # 既にある単位からの作成
        for value in self.values:
            # 認められる単位は重量か体積
            for valid_unit in self.mass_units + self.volume_units:
                _q = Unit.get_quantity(value, valid_unit)
                BaseFood(self.valid_food_name, _q)
            for invalid_unit in self.invalid_units:
                _q = Unit.get_quantity(value, invalid_unit)
                with self.assertRaises(ValueError):
                    BaseFood(self.valid_food_name, _q)

    def test_setting_nutrient(self):
        """栄養素の代入確認"""
        food = BaseFood(self.valid_food_name, '100g')
        energy = Energy(1)  # 数値のみの引数はデフォルトの単位が指定されたものとされる
        protein = Protein(2)
        lipid = Lipid(3)
        carbohydrate = Carbohydrate(4)
        salt = SaltEquivalent(5)
        # プロパティ側で自動で栄養素を分類する
        food.nutrient = energy
        food.nutrient = protein
        food.nutrient = lipid
        food.nutrient = carbohydrate
        food.nutrient = salt
        # 確認
        self.assertEqual(energy, food.energy)
        self.assertEqual(protein, food.protein)
        self.assertEqual(lipid, food.lipid)
        self.assertEqual(carbohydrate, food.carbohydrate)
        self.assertEqual(salt, food.salt)


if __name__ == '__main__':
    unittest.main()
