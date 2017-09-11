import unittest

from d_manager.food.product_food import ProductFood


class ProductFoodTest(unittest.TestCase):
    def test_init(self):
        product_food = ProductFood(maker_name='maker',
                                   product_name='product',
                                   food_name='food',
                                   amount='100g')
        product_food.set_nutrients_list(['1kcal', '1g', '2g', '3g', '4g'])

if __name__ == '__main__':
    unittest.main()
