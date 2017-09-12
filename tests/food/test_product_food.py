import unittest

from d_manager.food.product_food import ProductFood


class ProductFoodTest(unittest.TestCase):
    def test_init(self):
        product_food = ProductFood(maker_name='maker',
                                   product_name='product',
                                   food_name='food',
                                   amount='100g')
        product_food.set_nutrients_list(['1kcal', '1g', '2g', '3g', '4g'])

    def test_id(self):
        """ID 生成関係のメソッドテスト"""
        # グループの ID とグループ内の ID から総合 ID 総合
        self.assertEqual(ProductFood.get_total_id('1', '1'), 10001)
        self.assertEqual(ProductFood.get_total_id('1', '2345'), 12345)
        self.assertEqual(ProductFood.get_total_id('10', '1'), 100001)
        self.assertEqual(ProductFood.get_total_id('10', '2345'), 102345)
        # 総合 ID からグループの ID など
        self.assertEqual(ProductFood.get_other_ids_from_total_id('10001'), (1, 1))
        self.assertEqual(ProductFood.get_other_ids_from_total_id('12345'), (1, 2345))
        self.assertEqual(ProductFood.get_other_ids_from_total_id('100001'), (10, 1))
        self.assertEqual(ProductFood.get_other_ids_from_total_id('123456'), (12, 3456))

if __name__ == '__main__':
    unittest.main()
