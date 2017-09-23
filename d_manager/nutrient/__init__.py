class Nutrient:
    """栄養素を表すクラス"""
    def __init__(self, name, quantity):
        self.name = name
        self.quantity = quantity

    def __add__(self, other):
        if isinstance(other, Nutrient):
            self.quantity += other.quantity
            return self
        else:
            msg = '栄養素同士以外の加算は出来ません。'
            raise ValueError(msg)

    def __mul__(self, other):
        if isinstance(other, (int, float)):
            self.quantity *= other
            return self
        else:
            msg = 'この型を栄養素に乗算することは出来ません。 {}'.format(other)
            raise ValueError(msg)
