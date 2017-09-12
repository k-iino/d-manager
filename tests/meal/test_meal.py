import unittest
import datetime

from d_manager.food.product_food import ProductFood
from d_manager.food.stofc2015_food import STOFC2015Food
from d_manager.meal import MealItem
from d_manager.meal import Meal


class MealTestCase(unittest.TestCase):
    def test_meal_item(self):
        # 予想される食品を登録出来るか
        stofc2015_food = STOFC2015Food(group_id=1,
                                       food_id_in_group=1,
                                       food_id=1001,
                                       group_list=['group1', 'group2'],
                                       tag_list=['tag1', 'tag2', 'tag3'],
                                       amount='100g')
        scale = 0.5
        item = MealItem(stofc2015_food, scale)
        self.assertEqual(item.food, stofc2015_food)
        self.assertEqual(item.scale, scale)

        product_food = ProductFood(maker_name='maker',
                                   product_name='product',
                                   food_name='food',
                                   amount='100g')
        scale = 2.0
        item = MealItem(product_food, scale)
        item = MealItem(product_food, scale)
        self.assertEqual(item.scale, scale)

        scale_str = '0.5'
        item = MealItem(stofc2015_food, scale)
        self.assertEqual(item.scale, scale)

        # 食品ではないものは登録できない
        with self.assertRaises(ValueError):
            item = MealItem('hoge', scale)

    def test_meal(self):
        """食事エントリのテスト"""
        items = list()
        product_food = ProductFood(maker_name='maker',
                                   product_name='product',
                                   food_name='food',
                                   amount='100g')
        scale = 2.0
        items.append(MealItem(product_food, scale))

        stofc2015_food = STOFC2015Food(group_id=1,
                                       food_id_in_group=1,
                                       food_id=1001,
                                       group_list=['group1', 'group2'],
                                       tag_list=['tag1', 'tag2', 'tag3'],
                                       amount='100g')
        items.append(MealItem(stofc2015_food, scale))
        meal = Meal(items, _datetime=None, memo=None)
        i = 0
        for item in meal.items:
            self.assertEqual(item, items[i])
            i += 1

        # 時刻を指定しなかった場合、現在時刻が自動で登録されるかを確認
        now_dt = datetime.datetime.now()
        meal = Meal(items, _datetime=None, memo=None)
        # 日付
        self.assertEqual(now_dt.date(), meal.datetime.date())
        # 時間は分までの精度で確認
        self.assertEqual(datetime.time(now_dt.hour, now_dt.minute),
                         datetime.time(meal.datetime.hour, meal.datetime.minute))

        meal = Meal(items, now_dt)
        self.assertEqual(now_dt, meal.datetime)

        memo = '我々の夢はガラクタだらけ。いわば紙の帽子と仮装服のようなもの'
        meal = Meal(items, now_dt, memo)
        self.assertEqual(meal.memo, memo)

if __name__ == '__main__':
    unittest.main()
