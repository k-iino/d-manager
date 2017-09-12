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
    @staticmethod
    def get_other_ids_from_total_id(total_id):
        """総合 ID から他の ID を取得する"""
        total_id = str(total_id)
        if len(total_id) == 5:
            id_in_group = total_id[1:]
            group_id = total_id[:1]
        elif len(total_id) == 6:
            id_in_group = total_id[2:]
            group_id = total_id[:2]
        else:
            raise ValueError('不正な ID。{}'.format(total_id))

        return int(group_id), int(id_in_group)

    @staticmethod
    def get_total_id(group_id, id_in_group):
        """他の ID から総合 ID を作成する"""
        return int(group_id) * 10000 + int(id_in_group)

    def __init__(self, maker_name, product_name, food_name, amount):
        self.group_id = None
        self.id_in_group = None
        self.total_id = None
        self.product_name = product_name
        self.maker_name = maker_name
        super(ProductFood, self).__init__(food_name, amount)

    def classify(self, group_id, id_in_group):
        self.group_id = group_id
        self.id_in_group = id_in_group
        self.total_id = self.get_total_id(group_id, id_in_group)

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
                 self.total_id,
                 self.product_name,
                 self.maker_name]
        return _list + super().to_list()
