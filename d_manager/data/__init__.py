from pint import UnitRegistry


class Food:
    """
    Food class

    食品表示基準（平成 27 年内閣府令第 10 号）で規定される成分の内で、
    基本 5 項目を含む食品項目を表すクラス。
    基本 5 項目は熱量、たんぱく質、脂質、炭水化物、食塩相当量を指す。
    """
    # 異なる UnitRegistry 間だと量同士の演算が出来ないので
    # 全体でひとつの UnitRegistry を利用する。
    __ureg = UnitRegistry()

    __NAME_KEY = 'name'
    __AMOUNT_KEY = 'amount'
    __NUTRIENT_KEY = 'nutrient'
    __ENERGY_KEY = 'energy'
    __PROTEIN_KEY = 'protein'
    __LIPID_KEY = 'lipid'
    __CARBOHYDRATE_KEY = 'carbohydrate'
    __SALT_KEY = 'salt_equivalent'

    def __init__(self, name, amount):
        self.name = name
        self.amount = Food.__ureg.parse_expression(amount)
        self.__ntr = dict()

    def to_dict(self):
        def print_amount(_a):
            return '{:~P}'.format(_a)

        c_ = Food
        return {c_.__NAME_KEY: self.name,
                c_.__AMOUNT_KEY: print_amount(self.amount),
                c_.__NUTRIENT_KEY: {c_.__ENERGY_KEY: print_amount(self.__ntr[c_.__ENERGY_KEY]),
                                    c_.__PROTEIN_KEY: print_amount(self.__ntr[c_.__PROTEIN_KEY]),
                                    c_.__LIPID_KEY: print_amount(self.__ntr[c_.__LIPID_KEY]),
                                    c_.__CARBOHYDRATE_KEY: print_amount(self.__ntr[c_.__CARBOHYDRATE_KEY]),
                                    c_.__SALT_KEY: print_amount(self.__ntr[c_.__SALT_KEY]),
                                    }
                }

    # Energy
    @property
    def energy(self):
        return self.__ntr[Food.__ENERGY_KEY]

    @energy.setter
    def energy(self, amount):
        self.__ntr[Food.__ENERGY_KEY] = Food.__ureg.parse_expression(amount)

    # たんぱく質
    @property
    def protein(self):
        return self.__ntr[Food.__PROTEIN_KEY]

    @protein.setter
    def protein(self, amount):
        self.__ntr[Food.__PROTEIN_KEY] = Food.__ureg.parse_expression(amount)

    # 脂質
    @property
    def lipid(self):
        return self.__ntr[Food.__LIPID_KEY]

    @lipid.setter
    def lipid(self, amount):
        self.__ntr[Food.__LIPID_KEY] = Food.__ureg.parse_expression(amount)

    # 炭水化物
    @property
    def carbohydrate(self):
        return self.__ntr[Food.__CARBOHYDRATE_KEY]

    @carbohydrate.setter
    def carbohydrate(self, amount):
        self.__ntr[Food.__CARBOHYDRATE_KEY] = Food.__ureg.parse_expression(amount)

    # ナトリウム（食塩相当量で表示）
    @property
    def salt(self):
        return self.__ntr[Food.__SALT_KEY]

    @salt.setter
    def salt(self, amount):
        self.__ntr[Food.__SALT_KEY] = Food.__ureg.parse_expression(amount)


class EntryBase:
    def __init__(self, _id):
        self.id = _id

    def to_dict(self):
        raise NotImplementedError

    def to_list(self):
        raise NotImplementedError
