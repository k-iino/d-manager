from _collections import OrderedDict

from d_manager.book.meal_book import MealBook
from d_manager.meal import Meal
from d_manager.meal import MealItem
from d_manager.nutrient.basics import Energy, Protein, Lipid, Carbohydrate, SaltEquivalent


class CSVMealLogWriter:
    @staticmethod
    def __get_scaled_nutrients(nutrients, scale):
        """スケールを考慮した栄養素の取得"""
        _ntrs = dict()
        for nutrient in nutrients:
            if isinstance(nutrient, Energy):
                _ntrs[Energy] = nutrient * scale
            elif isinstance(nutrient, Protein):
                _ntrs[Protein] = nutrient * scale
            elif isinstance(nutrient, Lipid):
                _ntrs[Lipid] = nutrient * scale
            elif isinstance(nutrient, Carbohydrate):
                _ntrs[Carbohydrate] = nutrient * scale
            elif isinstance(nutrient, SaltEquivalent):
                _ntrs[SaltEquivalent] = nutrient * scale

        # 順序を維持して返したい
        return ((Energy, _ntrs[Energy]), (Protein, _ntrs[Protein]), (Lipid, _ntrs[Lipid]),
                (Carbohydrate, _ntrs[Carbohydrate]), (SaltEquivalent, _ntrs[SaltEquivalent]))

    @staticmethod
    def __sum_nutrients(nutrients):
        """渡された栄養素を全て合計して返す"""
        e, p, l, c, s = Energy(0), Protein(0), Carbohydrate(0), Carbohydrate(0), SaltEquivalent(0)
        for nutrient in nutrients:
            # 栄養素のクラスに１項代入演算子 '+=' を定義していない
            if isinstance(nutrient, Energy):
                e = e + nutrient
            elif isinstance(nutrient, Protein):
                p = p + nutrient
            elif isinstance(nutrient, Lipid):
                l = l + nutrient
            elif isinstance(nutrient, Carbohydrate):
                c = c + nutrient
            elif isinstance(nutrient, SaltEquivalent):
                s = s + nutrient
        else:
            return
    
    def daily_summary(self, book):
        if not isinstance(book, MealBook):
            raise ValueError()

        rows = list()
        # LABEL
        rows.append(['date',
        #              'food_id',
        #              'groups',
        #              'tags',
                     'energy [{:~P}]'.format(Energy.default_units()),
                     'protein [{:~P}]'.format(Protein.default_units()),
                     'lipid [{:~P}]'.format(Lipid.default_units()),
                     'carbohydrate [{:~P}]'.format(Carbohydrate.default_units()),
                     'salt_equivalent [{:~P}]'.format(SaltEquivalent.default_units()),
                     ])
        # Meal
        days = set()
        # 記録がある日付を先に集める
        for meal in book.generator():
            if not isinstance(meal, Meal):
                raise ValueError()
            days.add(meal.datetime.date())
        for day in days:
            # 1 日の栄養素
            daily_nutrients = dict()
            daily_nutrients[Energy] = Energy(0)
            daily_nutrients[Protein] = Protein(0)
            daily_nutrients[Lipid] = Lipid(0)
            daily_nutrients[Carbohydrate] = Carbohydrate(0)
            daily_nutrients[SaltEquivalent] = SaltEquivalent(0)
            # その日の栄養素をまとめる
            for meal in book.get_meals_by_date(day):
                for item in meal.items:
                    # スケールを考慮する
                    scaled_nutrient = self.__get_scaled_nutrients(item.food.nutrients.values(),
                                                                  item.scale)
                    # 栄養素毎に足し合わせる
                    for _cls, _ntr in scaled_nutrient:
                        daily_nutrients[_cls] = daily_nutrients[_cls] + _ntr
            # 有効数字を合わせる
            rows.append(list(map(lambda x: str(x), [day,
                                                    round(daily_nutrients[Energy].m,
                                                          Energy.default_significant_figure()),
                                                    round(daily_nutrients[Protein].m,
                                                          Protein.default_significant_figure()),
                                                    round(daily_nutrients[Lipid].m,
                                                          Lipid.default_significant_figure()),
                                                    round(daily_nutrients[Carbohydrate].m,
                                                          Carbohydrate.default_significant_figure()),
                                                    round(daily_nutrients[SaltEquivalent].m,
                                                          SaltEquivalent.default_significant_figure())])))
        for row in rows:
            print(','.join(row))
    
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
                # 栄養素（基本5項目）
                _nutrients = self.__get_scaled_nutrients(item.food.nutrients.values(),
                                                         scale=item.scale)
                for _cls, _n in _nutrients:
                    # 表示用の最小表示桁に丸める
                    _row.append(round(_n.m, _cls.default_significant_figure()))

                rows.append(list(map(lambda x: str(x), _row)))

        for row in rows:
            print(','.join(row))
