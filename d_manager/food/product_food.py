import yaml

from d_manager.food import BaseFood

# 出力時のキー
ID_KEY = 'id'
PRODUCT_KEY = 'product'
PRODUCT_NAME_KEY = 'product_name'
MAKER_KEY = 'maker'
FOOD_KEY = 'food'


class ProductFood(BaseFood):
    """食品表示法に準拠した表示事項を備える市販の食品"""
    def __init__(self, maker_name, product_name, food_name, amount):
        self.product_name = product_name
        self.maker_name = maker_name
        super(ProductFood, self).__init__(food_name, amount)

    def set_nutrients_list(self, l):
        """栄養素の情報をリスト形式でセットする。"""
        super(ProductFood, self).set_nutrients_list(l)

    def to_dict(self):
        return {PRODUCT_KEY: {PRODUCT_NAME_KEY: self.product_name,
                              MAKER_KEY: self.maker_name},
                FOOD_KEY: super().to_dict()}

    def to_yaml(self):
        return yaml.dump(self.to_dict())
