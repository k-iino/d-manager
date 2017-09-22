import json

from d_manager.food import Food


class Meal:
    """食事を表すクラス"""

    class Item:
        """
        食事記録の項目

        食事情報に食品単位に対する摂取した比率を反映させた情報持つ。
        """
        NAME_KEY = 'name'
        AMOUNT_KEY = 'amount'
        NUTRIENTS_KEY = 'nutrients'

        def __init__(self, food, scale):
            self.name = food.name
            self.amount = food.amount * scale
            self.nutrients = dict()
            for n_name, n_quantity in food.nutrients.items():
                self.nutrients[n_name] = n_quantity * scale

        def to_dict(self):
            """
            Item 内容を辞書で返す.

            ただし、食品の量や、栄養素は文字列でなく相当型のインスタンスなので注意。
            """
            d = dict()
            d[self.NAME_KEY] = self.name
            d[self.AMOUNT_KEY] = self.amount
            d[self.NUTRIENTS_KEY] = dict()
            for name, nutrient in self.nutrients.items():
                d[self.NUTRIENTS_KEY][name] = nutrient
            return d

        def to_json(self):
            """JSON 形式の文字列にして返す"""
            d = self.to_dict()
            # 文字列になっていないものを文字列にして返す
            d[self.AMOUNT_KEY] = str(d[self.AMOUNT_KEY].round(0))  # todo 食事量の表示有効桁の扱い
            for name, nutrient in d[self.NUTRIENTS_KEY].items():
                q = d[self.NUTRIENTS_KEY][name].quantity
                d[self.NUTRIENTS_KEY][name] = str(q.round(nutrient.ndigits))
            return json.dumps(d)

    def __init__(self):
        self.items = list()

    def append_item(self, item):
        if isinstance(item, self.Item):
            self.items.append(item)
        else:
            msg = '{} 以外の項目を食事に追加出来ません。'.format(self.Item.__name__)
            raise ValueError(msg)

    def append_food(self, food, scale):
        """食品情報を加える"""
        i = self.Item(food, scale)
        self.append_item(i)

    def to_json(self):
        """食事内容をリストにして返す"""
        l = list()
        for item in self.items:
            # todo
            # 一度 JSON 文字列にしてから、それを辞書形式にしている
            # 何か良い方法がないか
            _d = json.loads(item.to_json())
            l.append(_d)

        return json.dumps(l)

    def get_total_nutrients(self):
        """食事の栄養素毎の合計量を取得する"""
        total = dict()
        for item in self.items:
            for name, nutrient in item.nutrients.items():
                if name not in total:
                    total[name] = nutrient
                else:
                    total[name] += nutrient
        return total

    def to_summary_json(self):
        """食事の要約を JSON 形式で得る"""
        summary = dict()
        total_nutrients = self.get_total_nutrients()
        for name, nutrient in total_nutrients.items():
            summary[name] = str(nutrient.quantity.round(nutrient.ndigits))

        return json.dumps(summary)
