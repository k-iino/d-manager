import unittest

from d_manager.food.product_food import ProductFood
from d_manager.food.stofc2015_food import STOFC2015Food
from d_manager.meal import MealItem
from d_manager.meal import Meal


class MealTestCase(unittest.TestCase):
    def test_meal_item(self):

        item = MealItem()



if __name__ == '__main__':
    unittest.main()
