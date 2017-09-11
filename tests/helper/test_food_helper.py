import unittest

from d_manager.food import ENERGY_KEY, PROTEIN_KEY, LIPID_KEY, CARBOHYDRATE_KEY, SALT_KEY
from d_manager.food import BaseFood
from d_manager.helper import Unit
from d_manager.helper import FoodHelper


class FoodHelperTest(unittest.TestCase):
    def test_sum(self):
        food1 = BaseFood('food one', '100g')
        food2 = BaseFood('food two', '100g')

        nutrients_food1 = ('123kcal', '1g', '2g', '3g', '4g')
        nutrients_food2 = ('456kcal', '5g', '6g', '7g', '8g')
        excepted_scale1 = ('579kcal', '6g', '8g', '10g', '12g')
        excepted_scale2 = ('1158kcal', '12g', '16g', '20g', '24g')

        food1.energy = nutrients_food1[0]
        food2.energy = nutrients_food2[0]
        food1.protein = nutrients_food1[1]
        food2.protein = nutrients_food2[1]
        food1.lipid = nutrients_food1[2]
        food2.lipid = nutrients_food2[2]
        food1.carbohydrate = nutrients_food1[3]
        food2.carbohydrate = nutrients_food2[3]
        food1.salt = nutrients_food1[4]
        food2.salt = nutrients_food2[4]

        result = FoodHelper.sum_nutrients(food1, 1, food2, 1)
        self.assertEqual(result[ENERGY_KEY], Unit.get_amount(excepted_scale1[0]))
        self.assertEqual(result[PROTEIN_KEY], Unit.get_amount(excepted_scale1[1]))
        self.assertEqual(result[LIPID_KEY], Unit.get_amount(excepted_scale1[2]))
        self.assertEqual(result[CARBOHYDRATE_KEY], Unit.get_amount(excepted_scale1[3]))
        self.assertEqual(result[SALT_KEY], Unit.get_amount(excepted_scale1[4]))

        result = FoodHelper.sum_nutrients(food1, 2, food2, 2)
        self.assertEqual(result[ENERGY_KEY], Unit.get_amount(excepted_scale2[0]))
        self.assertEqual(result[PROTEIN_KEY], Unit.get_amount(excepted_scale2[1]))
        self.assertEqual(result[LIPID_KEY], Unit.get_amount(excepted_scale2[2]))
        self.assertEqual(result[CARBOHYDRATE_KEY], Unit.get_amount(excepted_scale2[3]))
        self.assertEqual(result[SALT_KEY], Unit.get_amount(excepted_scale2[4]))


if __name__ == '__main__':
    unittest.main()
