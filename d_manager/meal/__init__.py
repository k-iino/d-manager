class MealItem:

    ndigits_of_amount = 1

    """食事記録の項目を表すクラス"""
    def __init__(self, name, amount, nutrients):
        self.name = name
        self.amount = amount
        self.nutrients = nutrients


class Meal:
    """食事記録を表すクラス"""
    def __init__(self):
        self.items = list()

    def append(self, item):
        if isinstance(item, MealItem):
            self.items.append(item)
        else:
            msg = '{} 以外の項目を食事に追加出来ません。'.format(MealItem.__name__)
            raise ValueError(msg)
