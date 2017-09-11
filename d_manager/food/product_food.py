import yaml

from d_manager.food import BaseFood

# 出力時のキー
ID_KEY = 'id'
GROUP_ID_KEY = 'group_id'
ID_IN_GROUP_KEY = 'id_in_group'
PRODUCT_KEY = 'product'
PRODUCT_NAME_KEY = 'product_name'
MAKER_KEY = 'maker'
FOOD_KEY = 'food'


class ProductFood(BaseFood):
    """食品表示法に準拠した表示事項を備える市販の食品"""
    def __init__(self, maker_name, product_name, food_name, amount):
        self.group_id = None
        self.id_in_group = None
        self.id = None
        self.product_name = product_name
        self.maker_name = maker_name
        super(ProductFood, self).__init__(food_name, amount)

    def classify(self, group_id, id_in_group):
        self.group_id = group_id
        self.id_in_group = id_in_group
        self.id = group_id * 10000 + id_in_group

    def set_nutrients_list(self, l):
        """栄養素の情報をリスト形式でセットする。"""
        super(ProductFood, self).set_nutrients_list(l)

    def to_dict(self):
        return {PRODUCT_KEY: {PRODUCT_NAME_KEY: self.product_name,
                              MAKER_KEY: self.maker_name},
                FOOD_KEY: super().to_dict()}

    def get_label_of_list(self):
        _label = [GROUP_ID_KEY,
                  ID_IN_GROUP_KEY,
                  ID_KEY,
                  PRODUCT_NAME_KEY,
                  MAKER_KEY]
        return _label + super().get_label_of_list()

    def to_list(self):
        _list = [self.group_id,
                 self.id_in_group,
                 self.id,
                 self.product_name,
                 self.maker_name]
        return _list + super().to_list()
