from d_manager.helper.unit_helper import Unit

# 食品表示基準（平成 27 年内閣府令第 10 号）で規定される成分の内で、
# 基本 5 項目を含む食品項目飲みを管理する。
# 基本 5 項目とは熱量、たんぱく質、脂質、炭水化物、食塩相当量を指す。

# 出力時のラベル
NAME_LABEL = 'name'
AMOUNT_LABEL = 'amount'
NUTRIENT_LABEL = 'nutrient'
ENERGY_LABEL = 'energy'
PROTEIN_LABEL = 'protein'
LIPID_LABEL = 'lipid'
CARBOHYDRATE_LABEL = 'carbohydrate'
SALT_LABEL = 'salt_equivalent'

# 格納時のキー
ENERGY_KEY = 'energy'
PROTEIN_KEY = 'protein'
LIPID_KEY = 'lipid'
CARBOHYDRATE_KEY = 'carbohydrate'
SALT_KEY = 'salt_equivalent'

# 選択可能な食品群
# 日本食品標準成分表 2015 に収載されている食品群を採用
FOOD_GROUPS = {
    1: '穀類',
    2: 'いも及びでん粉類',
    3: '砂糖及び甘味類',
    4: '豆類',
    5: '種実類',
    6: '野菜類',
    7: '果実類',
    8: 'きのこ類',
    9: '藻類',
    10: '魚介類',
    11: '肉類',
    12: '卵類',
    13: '乳類',
    14: '油脂類',
    15: '菓子類',
    16: 'し好飲料類',
    17: '調味料及び香辛料類',
    18: '調理加工食品類',
}


class BaseFood:
    """
    Food class

    食品表示基準（平成 27 年内閣府令第 10 号）で規定される成分の内で、
    基本 5 項目を含む食品項目を表すクラス。
    基本 5 項目は熱量、たんぱく質、脂質、炭水化物、食塩相当量を指す。
    """

    def __init__(self, name, amount):
        self.name = str(name)
        # 食事に含まれる栄養素がどれくらいの量の食品における含有量かを示す基準となる量（食品単位）
        # 例えば市販の食品だったら栄養成分表示には食品単位が重量として記録されている。
        # また、日本食品標準成分表2015年版では食品単位は全て 100g である。
        # 量で、認められる次元は質量と体積の二つ
        if Unit.is_volume(amount) or Unit.is_mass(amount):
            self.amount = Unit.parse_expression(amount)
        else:
            raise ValueError('量の次元が不正。 value:{}'.format(amount))

        self.nutrients = dict()

    def set_nutrients_list(self, l):
        self.energy = l[0]
        self.protein = l[1]
        self.lipid = l[2]
        self.carbohydrate = l[3]
        self.salt = l[4]

    @classmethod
    def from_list(cls, l):
        food = cls(l[0], l[1])
        food.energy = l[2]
        food.protein = l[3]
        food.lipid = l[4]
        food.carbohydrate = l[5]
        food.salt = l[6]
        return food

    def to_dict(self):
        return {NAME_LABEL: self.name,
                AMOUNT_LABEL: Unit.to_str(self.amount),
                NUTRIENT_LABEL: {ENERGY_LABEL: Unit.to_str(self.energy),
                                 PROTEIN_LABEL: Unit.to_str(self.protein),
                                 LIPID_LABEL: Unit.to_str(self.lipid),
                                 CARBOHYDRATE_LABEL: Unit.to_str(self.carbohydrate),
                                 SALT_LABEL: Unit.to_str(self.salt),
                                 }
                }

    def get_label_of_list(self):
        return [NAME_LABEL,
                AMOUNT_LABEL,
                ENERGY_LABEL,
                PROTEIN_LABEL,
                LIPID_LABEL,
                CARBOHYDRATE_LABEL,
                SALT_LABEL]

    def to_list(self):
        return [self.name,
                self.amount,
                self.energy,
                self.protein,
                self.lipid,
                self.carbohydrate,
                self.salt]

    # Energy
    @property
    def energy(self):
        return self.nutrients[ENERGY_KEY]

    @energy.setter
    def energy(self, amount):
        if Unit.is_energy(amount):
            self.nutrients[ENERGY_KEY] = Unit.parse_expression(amount)
        else:
            raise ValueError('量の次元が不正。 value:{}'.format(amount))

    # たんぱく質
    @property
    def protein(self):
        return self.nutrients[PROTEIN_KEY]

    @protein.setter
    def protein(self, amount):
        if Unit.is_mass(amount):
            self.nutrients[PROTEIN_KEY] = Unit.parse_expression(amount)
        else:
            raise ValueError('量の次元が不正。 value:{}'.format(amount))

    # 脂質
    @property
    def lipid(self):
        return self.nutrients[LIPID_KEY]

    @lipid.setter
    def lipid(self, amount):
        if Unit.is_mass(amount):
            self.nutrients[LIPID_KEY] = Unit.parse_expression(amount)
        else:
            raise ValueError('量の次元が不正。 value:{}'.format(amount))

    # 炭水化物
    @property
    def carbohydrate(self):
        return self.nutrients[CARBOHYDRATE_KEY]

    @carbohydrate.setter
    def carbohydrate(self, amount):
        if Unit.is_mass(amount):
            self.nutrients[CARBOHYDRATE_KEY] = Unit.parse_expression(amount)
        else:
            raise ValueError('量の次元が不正。 value:{}'.format(amount))

    # ナトリウム（食塩相当量で表示）
    @property
    def salt(self):
        return self.nutrients[SALT_KEY]

    @salt.setter
    def salt(self, amount):
        if Unit.is_mass(amount):
            self.nutrients[SALT_KEY] = Unit.parse_expression(amount)
        else:
            raise ValueError('量の型が不正。 value:{}'.format(amount))
