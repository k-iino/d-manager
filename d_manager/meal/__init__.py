from d_manager.food import BaseFood
from d_manager.helper.datetime_helper import DateTimeHelper


class MealItem:
    def __init__(self, food, scale):
        """
        1回の食事に含まれるアイテム
        :param food:
        :param scale: 摂取した食事の標準的な量に対する倍率（物理量ではないので注意）
        """
        if isinstance(food, BaseFood):
            self.food = food
        else:
            raise ValueError('不正なエントリの型です。{}'.format(food))

        # 食品単位
        # 食事のエントリには記録されている栄養素がどれくらいの量の食品における含有量かを示す
        # 基準となる量（食品単位）が記録されている。
        # 例えば市販の食品だったら栄養成分表示には食品単位が重量として記録されている。
        # また、日本食品標準成分表2015年版では食品単位は全て 100g である。
        # ここでの scale とはこの食品単位に対して、摂取した量がどれくらいの倍率になるかを表している。
        self.scale = float(scale)

    # スケールの反映は、利用側でする。
    # def get_scaled_food_amount(self):
    #     """scale を反映した食品の量を返す"""
    #     return self.food.amount * self.scale
    #
    # def set_nutrient(self, nutrient):
    #     self.food.nutrient = nutrient
    #
    # def get_scaled_nutrients(self):
    #     """scale を反映した量の栄養素の辞書を返す"""
    #     scaled_nutrients = dict()
    #     for _class, _nutrient in self.food.nutrients:
    #         scaled_nutrients[_class] = _nutrient * self.scale
    #
    #     return scaled_nutrients

    def set_nutrients(self, nutrients):
        self.food.nutrients = nutrients


class AdjustMealItem(MealItem):
    """調整用アイテム"""
    def __init__(self):
        # 単に栄養素のコンテナとして食品情報を持つ
        food = BaseFood('adjust', '100g')
        super(AdjustMealItem, self).__init__(food, 1.0)


class Meal:
    """一回の食事を表すクラス"""
    def __init__(self, taking_time=None, memo=None):
        self.items = list()
        self.datetime = DateTimeHelper.get_datetime(taking_time)

        if memo is None:
            self.memo = ''
        elif isinstance(memo, str):
            self.memo = memo
        else:
            raise ValueError

    def append(self, item, memo=None):
        """食事を追加する"""
        if isinstance(item, MealItem):
            self.items.append(item)
        else:
            raise ValueError('Item の型が不正。{}'.format(type(item)))

        if isinstance(memo, str):
            self.memo = memo
