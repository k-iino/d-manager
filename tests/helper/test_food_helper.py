import unittest
import random

from d_manager.food import ENERGY_KEY, PROTEIN_KEY, LIPID_KEY, CARBOHYDRATE_KEY, SALT_KEY
from d_manager.food import BaseFood
from d_manager.helper.unit_helper import Unit
from d_manager.helper.food_helper import FoodHelper


class FoodHelperTest(unittest.TestCase):
    def test_get_actual_nutrients(self):
        """食品に摂取比率をかけた時に正しい栄養素の量が得られるか"""
        energy_unit = 'kcal'
        mass_unit = 'g'
        nutrient_keys = (ENERGY_KEY, PROTEIN_KEY, LIPID_KEY, CARBOHYDRATE_KEY, SALT_KEY)

        # ランダムに栄養素（数値列）を作成して、計算を行う
        random.seed()
        # 試行回数分、ランダムな栄養素と摂取比率を持つ食品を作成して計算して確認する
        num_of_challenge = 10
        for num in range(num_of_challenge):
            food = BaseFood('food one', '100g')
            scale = round(random.random() * 10, 1)
            nutrients = dict()
            scaled_numbers = dict()

            for key in nutrient_keys:
                # 0 < n < 1000
                _n = round(random.random() * 1000, 1)
                # 数字列を作成して、予め scale を計算したものを格納していおく
                scaled_numbers[key] = _n * scale

                # 栄養素
                if key == ENERGY_KEY:
                    pq = '{}{}'.format(_n, energy_unit)
                else:
                    pq = '{}{}'.format(_n, mass_unit)

                nutrients[key] = pq
            else:
                food.nutrients = nutrients
                actual_nutrients = FoodHelper.get_actual_nutrients(food, scale)
                # 栄養素毎に比較
                for key in nutrient_keys:
                    self.assertEqual(scaled_numbers[key], actual_nutrients[key].magnitude)

    # def test_sum(self):
    #     food1 = BaseFood('food one', '100g')
    #     food2 = BaseFood('food two', '100g')
    #
    #     nutrients_food1 = ('123kcal', '1g', '2g', '3g', '4g')
    #     nutrients_food2 = ('456kcal', '5g', '6g', '7g', '8g')
    #     excepted_scale1 = ('579kcal', '6g', '8g', '10g', '12g')
    #     excepted_scale2 = ('1158kcal', '12g', '16g', '20g', '24g')
    #
    #     food1.energy = nutrients_food1[0]
    #     food2.energy = nutrients_food2[0]
    #     food1.protein = nutrients_food1[1]
    #     food2.protein = nutrients_food2[1]
    #     food1.lipid = nutrients_food1[2]
    #     food2.lipid = nutrients_food2[2]
    #     food1.carbohydrate = nutrients_food1[3]
    #     food2.carbohydrate = nutrients_food2[3]
    #     food1.salt = nutrients_food1[4]
    #     food2.salt = nutrients_food2[4]
    #
    #     result = FoodHelper.sum_nutrients(food1, 1, food2, 1)
    #     self.assertEqual(result[ENERGY_KEY], Unit.get_amount(excepted_scale1[0]))
    #     self.assertEqual(result[PROTEIN_KEY], Unit.get_amount(excepted_scale1[1]))
    #     self.assertEqual(result[LIPID_KEY], Unit.get_amount(excepted_scale1[2]))
    #     self.assertEqual(result[CARBOHYDRATE_KEY], Unit.get_amount(excepted_scale1[3]))
    #     self.assertEqual(result[SALT_KEY], Unit.get_amount(excepted_scale1[4]))
    #
    #     result = FoodHelper.sum_nutrients(food1, 2, food2, 2)
    #     self.assertEqual(result[ENERGY_KEY], Unit.get_amount(excepted_scale2[0]))
    #     self.assertEqual(result[PROTEIN_KEY], Unit.get_amount(excepted_scale2[1]))
    #     self.assertEqual(result[LIPID_KEY], Unit.get_amount(excepted_scale2[2]))
    #     self.assertEqual(result[CARBOHYDRATE_KEY], Unit.get_amount(excepted_scale2[3]))
    #     self.assertEqual(result[SALT_KEY], Unit.get_amount(excepted_scale2[4]))


if __name__ == '__main__':
    unittest.main()
