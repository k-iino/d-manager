from datetime import datetime

from pint import UnitRegistry


class Unit:
    """単位を操作するクラス"""
    # 実際の物理量の操作は別のパッケージに委任している。

    # 異なる UnitRegistry 間だと量同士の演算が出来ないので
    # 全体でひとつの UnitRegistry を利用する。
    __reg = UnitRegistry()

    # 次元を示す文字列
    DIM_MASS = '[mass]'
    DIM_VOLUME = '[volume]'
    DIM_ENERGY = '[energy]'

    @classmethod
    def get_amount(cls, a):
        if isinstance(a, int) or isinstance(a, float):
            return cls.__reg.Quantity(a)
        elif isinstance(a, str):
            return cls.parse_expression(a)
        elif isinstance(a, cls.__reg.Quantity):
            return a
        else:
            raise ValueError('不適切な値。 type={}, value={}'.format(type(a), a))

    @classmethod
    def parse_expression(cls, e):
        return cls.__reg.parse_expression(e)

    @staticmethod
    def to_str(amount):
        return '{:~P}'.format(amount)

    @classmethod
    def check_dimensionality(cls, dim, amount):
        """単位の次元を確認する。"""
        amount = cls.get_amount(amount)
        a = cls.__reg.get_dimensionality(amount)
        m = cls.__reg.get_dimensionality(dim)
        return a == m

    @classmethod
    def is_mass(cls, amount):
        """量の次元は質量か"""
        return cls.check_dimensionality(cls.DIM_MASS, amount)

    @classmethod
    def is_volume(cls, amount):
        """量の次元は体積か"""
        return cls.check_dimensionality(cls.DIM_VOLUME, amount)

    @classmethod
    def is_energy(cls, amount):
        """量の次元はエネルギーか"""
        return cls.check_dimensionality(cls.DIM_ENERGY, amount)


class FoodHelper:
    @staticmethod
    def sum_nutrients(food1, scale_of_food1, food2, scale_of_food2):
        """二つの食品の栄養素を加算して求める"""
        # 加算した栄養素は辞書から削除するため複製しておく
        nutrients_of_food1 = dict(food1.nutrients)
        nutrients_of_food2 = dict(food2.nutrients)

        result = dict()
        for k1, v1 in nutrients_of_food1.items():
            if k1 in nutrients_of_food2.keys():
                # Food1 と Food2 と両方に含まれている栄養素
                result[k1] = v1 * scale_of_food1 + nutrients_of_food2[k1] * scale_of_food2
                del nutrients_of_food2[k1]
            else:
                # Food1 に含まれているが Food2 には含まれていない栄養素
                result[k1] = v1 * scale_of_food1

        # Food1 には無く Food2 には含まれている栄養素
        for k2, v2 in nutrients_of_food2.items():
            result[k2] = v2 * scale_of_food2

        return result


class DateTimeHelper:

    # 全て0埋めした10進数
    DATE_FORMAT = '%Y-%m-%d'
    TIME_FORMAT = '%H:%M:%S'
    DATETIME_FORMAT = '{} {}'.format(DATE_FORMAT, TIME_FORMAT)

    @classmethod
    def get_datetime(s):
        datetime.strptime(s)
