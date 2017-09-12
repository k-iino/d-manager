import unittest
import random
import datetime

from d_manager.book.meal_book import MealBook
from d_manager.meal import MealItem, Meal
from d_manager.food.product_food import ProductFood


class MealBookTestCase(unittest.TestCase):
    def test_init(self):

        # 食事を大量に作成し、ランダムに MealBook に登録する。
        # ランダムに登録しても内部的には同じ日付内で時刻昇順に登録されているかを確認する。
        meals = list()
        meals_by_time = list()
        challenge_time = 50
        for i in range(challenge_time):
            product_food = ProductFood(maker_name='maker',
                                       product_name='product {}'.format(i),
                                       food_name='food',
                                       amount='100g')
            scale = 2.0
            meal = Meal([MealItem(product_food, scale)], memo='{}'.format(i))
            meals.append(meal)
            meals_by_time.append(meal)

        # 登録はシャッフルしてから登録する
        meal_book = MealBook()
        random.seed()
        random.shuffle(meals)
        for meal in meals:
            meal_book.append(meal)

        # 確認する
        date = datetime.date.today()
        i = 0
        for meal in meal_book.get_meal_by_date(date):
            self.assertEqual(meals_by_time[i], meal)
            #print('{}: {}'.format(meal.datetime, meal.memo))
            i += 1


if __name__ == '__main__':
    unittest.main()
