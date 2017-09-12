import datetime
from d_manager.food import BaseFood


class MealItem:
    def __init__(self, food, scale):
        """
        食事に登録するアイテム
        :param food:
        :param scale: 摂取した食事の標準的な量に対する倍率（物理量ではないので注意）
        """
        if isinstance(food, BaseFood):
            self.food = food
        else:
            raise ValueError('不正なエントリの型です。{}'.format(food))

        # 食事のエントリには記録されている栄養素がどれくらいの量の食品における含有量かを示す
        # 基準となる量（食品単位）が記録されている。
        # 例えば市販の食品だったら栄養成分表示には食品単位が重量として記録されている。
        # また、日本食品標準成分表2015年版では食品単位は全て 100g である。
        # ここでの scale とはこの食品単位に対して、摂取した量がどれくらいの倍率になるかを表している。
        self.scale = float(scale)


class Meal:
    def __init__(self, items, _datetime=None, memo=None):
        # 記録すべき事項
        #   - 時間
        #     - 日付
        #     - 時刻
        #   - 食事
        #     - 食品を特定する情報
        #     - 食べた量
        # オプション
        #     - メモ

        if isinstance(_datetime, datetime.datetime):
            self.datetime = _datetime
        elif not _datetime:
            # 時刻が登録されていなかった場合は現在の時刻で作成
            self.datetime = datetime.datetime.now()
        else:
            raise ValueError('時刻のデータが不正. {}'.format(_datetime))

        self.items = list()
        for item in items:
            if isinstance(item, MealItem):
                self.items = items
            else:
                raise ValueError('Item の型が不正。{}'.format(type(item)))

        if memo:
            self.memo = str(memo)
        else:
            self.memo = ''
