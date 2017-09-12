import datetime
from d_manager.book import BaseBook

from d_manager.meal import Meal


class MealBook(BaseBook):
    def __init__(self):
        super(MealBook, self).__init__()
        # 日付ごとに食事の記録を持つ
        self.meals_by_date = dict()

    def append(self, new_meal):
        """食事を登録"""
        if not isinstance(new_meal, Meal):
            raise ValueError

        # 日付をキーとする
        date = new_meal.datetime.date()
        if date not in self.meals_by_date:
            self.meals_by_date[date] = list([new_meal, ])
        else:
            # 時刻昇順で格納する
            self.meals_by_date[date].append(new_meal)
            self.meals_by_date[date] = sorted(self.meals_by_date[date],
                                              key=lambda meal: meal.datetime)

    def get_meal_by_date(self, date):
        if isinstance(date, datetime.date):
            return self.meals_by_date[date]
        elif isinstance(date, datetime.datetime):
            return self.meals_by_date[date.date()]
        else:
            raise ValueError
