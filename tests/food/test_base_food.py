import unittest

from d_manager.food import BaseFood


class BaseFoodTest(unittest.TestCase):
    def test_init(self):
        """コンストラクタの確認"""
        # Good
        valid_name = 'food_name'
        valid_mass_amounts = ['123' + x for x in ('ug', 'mg', 'g', 'kg')]
        valid_volume_amounts = ['123' + x for x in ('ml', 'l')]
        for valid_amount in valid_mass_amounts + valid_volume_amounts:
            BaseFood(valid_name, valid_amount)

        invalid_amounts = ['123' + x for x in ('s', 'm', 'J', 'kcal')]
        for invalid_amount in invalid_amounts:
            with self.assertRaises(ValueError):
                BaseFood(valid_name, invalid_amount)

        # リストをセットする
        food = BaseFood(valid_name, '100g')
        food.set_nutrients_list(['1kcal', '1g', '2g', '3g', '4g'])
        # リストから取得する
        values = [valid_name, '100g', '1kcal', '1g', '2g', '3g', '4g']
        food = BaseFood.from_list(values)

    def test_nutrient(self):
        """栄養素の代入確認"""
        valid_name = 'food_name'
        valid_food_amount = '100g'
        food = BaseFood(valid_name, valid_food_amount)

        energy_amounts = ['123' + x for x in ('J', 'kcal')]
        mass_amounts = ['123' + x for x in ('ug', 'mg', 'g', 'kg')]
        non_energy_amounts = ['123' + x for x in ('s', 'm', 'A', 'ml', 'l', 'g', 'mg', 'kg')]
        non_mass_amounts = ['123' + x for x in ('s', 'm', 'A', 'ml', 'l', 'J', 'kcal')]

        # Good
        for energy_amount in energy_amounts:
            food.energy = energy_amount

        for mass_amount in mass_amounts:
            food.protein = mass_amount
            food.lipid = mass_amount
            food.carbohydrate = mass_amount
            food.salt = mass_amount

        # Bad
        for amt in non_energy_amounts:
            with self.assertRaises(ValueError):
                food.energy = amt

        for amt in non_mass_amounts:
            with self.assertRaises(ValueError):
                food.protein = amt
            with self.assertRaises(ValueError):
                food.lipid = amt
            with self.assertRaises(ValueError):
                food.carbohydrate = amt
            with self.assertRaises(ValueError):
                food.salt = amt

if __name__ == '__main__':
    unittest.main()
