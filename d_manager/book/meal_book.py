import datetime

from d_manager.book import BaseBook
from d_manager.meal import Meal
# from d_manager.helper.food_helper import FoodHelper
# from d_manager.food import ENERGY_KEY, PROTEIN_KEY, LIPID_KEY, CARBOHYDRATE_KEY, SALT_KEY
# from d_manager.food.product_food import ProductFood
# from d_manager.food.stofc2015_food import STOFC2015Food


class MealBook(BaseBook):
    """食事のログを収載するクラス"""
    def __init__(self):
        super(MealBook, self).__init__()
        # 日付ごとに食事の記録を持つ
        self.__meals = dict()

    def append(self, new_meal):
        """食事を登録"""
        if not isinstance(new_meal, Meal):
            raise ValueError

        # 食事内の日付をキーにして整理する
        date = new_meal.datetime.date()
        if date not in self.__meals.keys():
            # その日付最初の食事
            self.__meals[date] = list([new_meal, ])
        else:
            self.__meals[date].append(new_meal)
            # その日付の中の食事を時刻昇順でソートした上で格納しなす
            self.__meals[date] = sorted(self.__meals[date],
                                        key=lambda meal: meal.datetime)

    def get_meals_by_date(self, date):
        """指定した日付の食事群を取得する"""
        if isinstance(date, datetime.date):
            return self.__meals[date]
        elif isinstance(date, datetime.datetime):
            return self.__meals[date.date()]
        else:
            raise ValueError

    def generator(self):
        for date, meals in self.__meals.items():
            for meal in meals:
                yield date, meal

    # def get_rows(self, is_label=True):
    #     """行の集合として出力する"""
    #     # 日付昇順で表示する
    #     rows = list()
    #     labels = ['date',
    #               'time',
    #               'food_name',
    #               'amount',
    #               'energy',
    #               'protein',
    #               'lipid',
    #               'carbohydrate',
    #               'salt',
    #               ]
    #
    #     if is_label:
    #         rows.append(labels)
    #
    #     for date in sorted(self.__meals):
    #         for meal in self.__meals[date]:
    #             for item in meal.items:
    #                 food = item.food
    #                 # 食品名
    #                 if isinstance(food, ProductFood):
    #                     food_name = '{} {}'.format(food.maker_name, food.product_name)
    #                 else:
    #                     food_name = food.name
    #
    #                 # 摂取量
    #                 amount = food.amount * item.scale
    #                 # 摂取した栄養素
    #                 nutrients = FoodHelper.get_actual_nutrients(food, item.scale)
    #
    #                 row = [meal.datetime.date(),
    #                        meal.datetime.time(),
    #                        food.name,
    #                        amount,
    #                        nutrients[ENERGY_KEY],
    #                        nutrients[PROTEIN_KEY],
    #                        nutrients[LIPID_KEY],
    #                        nutrients[CARBOHYDRATE_KEY],
    #                        nutrients[SALT_KEY],
    #                        ]
    #                 # row_list = list(map(lambda x: str(x), row_list))
    #                 rows.append(row)
    #
    #     return rows
