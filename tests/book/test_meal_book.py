# import unittest
# import random
# import datetime
# import math
#
# from d_manager.book.meal_book import MealBook
# from d_manager.meal import MealItem, Meal
# from d_manager.food.product_food import ProductFood
#
#
# class MealBookTestCase(unittest.TestCase):
#     def test_init(self):
#         # 食事を大量に作成し、ランダムに MealBook に登録する。
#         # ランダムに登録しても内部的には同じ日付内で時刻昇順に登録されているかを確認する。
#         meals = list()
#         meals_by_time = list()
#         challenge_time = 50
#         for i in range(challenge_time):
#             product_food = ProductFood(maker_name='maker',
#                                        product_name='product {}'.format(i),
#                                        food_name='food',
#                                        amount='100g')
#             scale = 2.0
#             meal = Meal([MealItem(product_food, scale)], memo='{}'.format(i))
#             meals.append(meal)
#             meals_by_time.append(meal)
#
#         # 登録はシャッフルしてから登録する
#         meal_book = MealBook()
#         random.seed()
#         random.shuffle(meals)
#         for meal in meals:
#             meal_book.append(meal)
#
#         # 確認する
#         date = datetime.date.today()
#         i = 0
#         for meal in meal_book.get_meal_by_date(date):
#             self.assertEqual(meals_by_time[i], meal)
#             i += 1
#
#     def test_append(self):
#         # 日付を指定した場合に登録が出来るか
#         product_food = ProductFood(maker_name='maker',
#                                    product_name='product',
#                                    food_name='food',
#                                    amount='100g')
#         scale = 2.0
#         # 時刻、日付両方のオブジェクトで登録が出来るか
#         meal_1 = Meal([MealItem(product_food, scale)], datetime.datetime.now())
#         meal_2 = Meal([MealItem(product_food, scale)], datetime.date.today())
#         pass
#
#     def test_rows(self):
#         # 食事を大量に作成し、ランダムな日付に MealBook に登録する。
#         meal_book = MealBook()
#         challenge_time = 50
#         num_of_food = 20
#         for i in range(challenge_time):
#             meal_items = list()
#             for j in range(num_of_food):
#                 product_food = ProductFood(maker_name='maker',
#                                            product_name='product {}'.format(j),
#                                            food_name='food {}'.format(j),
#                                            amount='100g')
#                 product_food.nutrients = ['1kcal', '1g', '2g', '3g', '4g']
#                 scale = round(random.random()*10, 2)
#                 meal_items.append(MealItem(product_food, scale))
#
#             year = random.randrange(2000, 2017)
#             month = random.randrange(1, 13)
#             day = random.randrange(1, 29)
#             date = datetime.date(year, month, day)
#             meal = Meal(meal_items, date, memo='{}'.format(i))
#             meal_book.append(meal)
#
#         for row in meal_book.get_rows():
#             print(row)
#
# if __name__ == '__main__':
#     unittest.main()
