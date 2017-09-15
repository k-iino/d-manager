import csv
import sys

from d_manager.book.meal_book import MealBook
from d_manager.meal import Meal
from d_manager.meal import MealItem
from d_manager.nutrient.basics import Energy, Protein, Lipid, Carbohydrate, SaltEquivalent


class CSVMealLogWriter:
    def write(self, book):
        if not isinstance(book, MealBook):
            raise ValueError()

        rows = list()

        # LABEL
        rows.append(['date',
                     'time',
                     'food_name',
                     'amount',
        #              'food_id',
        #              'groups',
        #              'tags',
                     'energy [{:~P}]'.format(Energy.default_units()),
                     'protein [{:~P}]'.format(Protein.default_units()),
                     'lipid [{:~P}]'.format(Lipid.default_units()),
                     'carbohydrate [{:~P}]'.format(Carbohydrate.default_units()),
                     'salt_equivalent [{:~P}]'.format(SaltEquivalent.default_units()),
                     ])

        for meal in book.generator():
            if not isinstance(meal, Meal):
                raise ValueError()

            for item in meal.items:
                if not isinstance(item, MealItem):
                    raise ValueError()

                _row = list()
                # 時刻
                _row.extend([meal.datetime.date(),
                            meal.datetime.time().strftime('%H:%M'),  # 秒以下はいらない
                            ])
                # 食品情報
                _row.extend([item.food.name,
                             item.food.amount * item.scale,
                             ])
                # 栄養素
                _nutrients = [None, None, None, None, None]
                for _, nutrient in item.food.nutrients.items():
                    if isinstance(nutrient, Energy):
                        _nutrients[0] = round((nutrient * item.scale).m, Energy.default_significant_figure())
                    elif isinstance(nutrient, Protein):
                        _nutrients[1] = round((nutrient * item.scale).m, Protein.default_significant_figure())
                    elif isinstance(nutrient, Lipid):
                        _nutrients[2] = round((nutrient * item.scale).m, Lipid.default_significant_figure())
                    elif isinstance(nutrient, Carbohydrate):
                        _nutrients[3] = round((nutrient * item.scale).m, Carbohydrate.default_significant_figure())
                    elif isinstance(nutrient, SaltEquivalent):
                        _nutrients[4] = round((nutrient * item.scale).m, SaltEquivalent.default_significant_figure())
                else:
                    _row.extend(_nutrients)

                rows.append(list(map(lambda x: str(x), _row)))

        for row in rows:
            print(','.join(row))
