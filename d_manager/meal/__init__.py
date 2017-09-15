import datetime
from d_manager.food import BaseFood


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


class AdjustMealItem:
    """調整用アイテム"""
    def __init__(self):
        # 単に栄養素のコンテナとして食品情報を持つ
        self.__food = BaseFood('adjust', '1g')

    @property
    def nutrient(self):
        return self.__food.nutrient

    @nutrient.setter
    def nutrient(self, nutrient):
        self.__food.nutrient = nutrient

    @property
    def nutrients(self):
        return self.__food.nutrients

    @nutrients.setter
    def nutrients(self, nutrients):
        self.__food.nutrients = nutrients


class Meal:
    """一回の食事を表すクラス"""
    def __init__(self, taking_time=None, memo=None):
        self.items = list()

        if taking_time is None:
            # 時刻が登録されていなかった場合は現在の時刻で作成
            self.datetime = datetime.datetime.now()
        elif isinstance(taking_time, datetime.datetime):
            self.datetime = taking_time
        elif isinstance(taking_time, datetime.date):
            # date オブジェクトなら、時刻情報はないが日付のみでよいとする
            self.datetime = datetime.datetime(year=taking_time.year,
                                              month=taking_time.month,
                                              day=taking_time.day)
        else:
            raise ValueError('時刻のデータが不正. {}'.format(taking_time))

        if memo is None:
            self.memo = ''
        elif isinstance(memo, str):
            self.memo = memo
        else:
            raise ValueError

    def append(self, item, memo=None):
        """食事を追加する"""
        if isinstance(item, MealItem) or isinstance(item, AdjustMealItem):
            self.items.append(item)
        else:
            raise ValueError('Item の型が不正。{}'.format(type(item)))

        if isinstance(memo, str):
            self.memo = memo
        else:
            raise ValueError
