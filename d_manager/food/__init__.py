from d_manager.nutrient import BaseNutrient
#from d_manager.nutrient.basics import Energy, Protein, Lipid, Carbohydrate, SaltEquivalent
from d_manager.quantity.unit import Unit
from d_manager.quantity.quantity import FoodQuantity


class Food:
    def __init__(self, name, amount):
        self.name = str(name)
        self.nutrients = dict()
        # 食品単位
        # 食事に含まれる栄養素がどれくらいの量の食品における含有量かを示す基準となる量。
        # 例えば一般の加工食品だったら「栄養成分表示」に食品単位が重量か体積で示されている
        self.amount = FoodQuantity.from_str(amount)

    def set_nutrient(self, name, nutrient):
        self.nutrients[name] = nutrient


class BaseFood:
    """基本となる食品クラス"""
    # NAME_KEY = 'name'
    # AMOUNT_KEY = 'amount'
    # NUTRIENT_KEY = 'helper'
    # # 栄養素のキー
    # ENERGY_KEY = 'energy'
    # PROTEIN_KEY = 'protein'
    # LIPID_KEY = 'lipid'
    # CARBOHYDRATE_KEY = 'carbohydrate'
    # SALT_KEY = 'salt_equivalent'
    # SODIUM_KEY = 'sodium'

    def __init__(self, name, amount, ):
        self.name = str(name)

        # 食品単位
        # 食事に含まれる栄養素がどれくらいの量の食品における含有量かを示す基準となる量。
        # 例えば一般の加工食品だったら「栄養成分表示」に食品単位が重量か体積で示されている
        _q = Unit.get_quantity(amount)

        # 日本食品標準成分表2015年版では食品単位は全て 100g である。
        # また、「食品表示基準」によると一般加工食品の食品単位で認められる単位は質量か体積の二つ
        if Unit.is_volume(_q) or Unit.is_mass(_q):
            self.amount = _q
        else:
            raise ValueError('{} の量の次元が不正。 value:{}'.format(name, _q.units))

        self.__nutrients = dict()

    @staticmethod
    def from_json(j):
        food = BaseFood(j['name'], j['amount'])
        return food
        
    # 栄養素に関するその他事項
    # 有効数字については、各栄養素のクラスで決定している。

    @property
    def nutrient(self):
        raise NotImplementedError

    @nutrient.setter
    def nutrient(self, nutrient):
        if isinstance(nutrient, BaseNutrient):
            self.__nutrients[nutrient.__class__] = nutrient
        else:
            ValueError('栄養素ではありません。')

    def __check_and_set_nutrient(self, nutrient, class_):
        """栄養素の型を確認してから栄養素をセットする"""
        if isinstance(nutrient, BaseNutrient) and isinstance(nutrient, class_):
            self.nutrient = nutrient
        else:
            raise ValueError('栄養素ではありません。')
    
    @property
    def nutrients(self):
        return self.__nutrients

    @nutrients.setter
    def nutrients(self, nutrients):
        """シーケンス形式で表された栄養素をセットする"""
        if isinstance(nutrients, list) or isinstance(nutrients, tuple):
            for n in nutrients:
                self.nutrient = n
        else:
            raise NotImplementedError

    # 基本 5 項目
    # 熱量、たんぱく質、脂質、炭水化物、食塩相当量

    # 熱量
    @property
    def energy(self):
        return self.__nutrients[Energy]

    @energy.setter
    def energy(self, n):
        self.__check_and_set_nutrient(n, Energy)

    # たんぱく質
    @property
    def protein(self):
        return self.__nutrients[Protein]

    @protein.setter
    def protein(self, n):
        self.__check_and_set_nutrient(n, Protein)

    # 脂質
    @property
    def lipid(self):
        return self.__nutrients[Lipid]

    @lipid.setter
    def lipid(self, n):
        self.__check_and_set_nutrient(n, Lipid)

    # 炭水化物
    @property
    def carbohydrate(self):
        return self.__nutrients[Carbohydrate]

    @carbohydrate.setter
    def carbohydrate(self, n):
        self.__check_and_set_nutrient(n, Carbohydrate)

    # 食塩相当量
    # 「食品表示基準」では「栄養成分表示」にナトリウム量を示した場合も、食塩相当量を示す義務を設けている。
    # そのため、実際は食塩相当量で事足りる。
    @property
    def salt(self):
        return self.__nutrients[SaltEquivalent]

    @salt.setter
    def salt(self, n):
        self.__check_and_set_nutrient(n, SaltEquivalent)

    # # ナトリウム（ソディウム）
    # # 内部的には食塩相当量として保持する。
    # @property
    # def sodium(self):
    #     return self.salt / 2.54
    # 
    # @sodium.setter
    # def sodium(self, amount):
    #     if Unit.is_mass(amount):
    #         self.salt = Unit.UnitRegistry(amount) * 2.54
    #     else:
    #         raise ValueError('量の型が不正。 value:{}'.format(amount))

    # fixme
    # @staticmethod
    # def get_from_list(l):
    #     """リストからインスタンスを作成する"""
    #     food = BaseFood(l[0], l[1])
    #     food.energy = l[2]
    #     food.protein = l[3]
    #     food.lipid = l[4]
    #     food.carbohydrate = l[5]
    #     food.salt = l[6]
    #     return food
    #
    # def to_list(self):
    #     """リストを作成する"""
    #     return [self.name,
    #             self.amount,
    #             self.energy,
    #             self.protein,
    #             self.lipid,
    #             self.carbohydrate,
    #             self.salt]
    #
    # @property
    # def labels(self):
    #     """ラベルのリストを作成する"""
    #     return [self.NAME_KEY,
    #             self.AMOUNT_KEY,
    #             self.ENERGY_KEY,
    #             self.PROTEIN_KEY,
    #             self.LIPID_KEY,
    #             self.CARBOHYDRATE_KEY,
    #             self.SALT_KEY]
    #
    # @classmethod
    # def from_dict(cls, d):
    #     """辞書形式からインスタンスを作成"""
    #     food = BaseFood(d[cls.NAME_KEY], d[cls.AMOUNT_KEY])
    #     _nutrients = d[cls.NUTRIENT_KEY]
    #     food.energy = _nutrients[cls.ENERGY_KEY]
    #     food.protein = _nutrients[cls.PROTEIN_KEY]
    #     food.lipid = _nutrients[cls.LIPID_KEY]
    #     food.carbohydrate = _nutrients[cls.CARBOHYDRATE_KEY]
    #     food.salt = _nutrients[cls.SALT_KEY]
    #     return food
    #
    # def to_dict(self):
    #     """辞書形式に変換"""
    #     return {self.NAME_KEY: self.name,
    #             self.AMOUNT_KEY: self.amount,
    #             self.NUTRIENT_KEY: {self.ENERGY_KEY: self.energy,
    #                                 self.PROTEIN_KEY: self.protein,
    #                                 self.LIPID_KEY: self.lipid,
    #                                 self.CARBOHYDRATE_KEY: self.carbohydrate,
    #                                 self.SALT_KEY: self.salt,
    #                                 }
    #             }
