from d_manager.data import EntryBase
from d_manager.data import Food


class FoodEntry(EntryBase):
    def __init__(self, _id, food):
        if isinstance(food, Food):
            self.food = food
        else:
            raise ValueError

        super(FoodEntry, self).__init__(_id)

    def to_dict(self):
        return {'id': self.id,
                'food': self.food.to_dict()}


class ProductFoodEntry(FoodEntry):
    def __init__(self, _id, product_name, maker_name, food):
        self.product_name = product_name
        self.maker_name = maker_name
        super(ProductFoodEntry, self).__init__(_id, food)

    def to_dict(self):
        return {'id': self.id,
                'product': {'name': self.product_name,
                            'maker': self.maker_name},
                'food': self.food.to_dict()}


class STOFC2015r7FoodEntry(FoodEntry):
    """
    日本食品標準成分表2015年版（七訂）の食品情報を持つエントリ
    """
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

    def __init__(self, _id, group, tag_name, food):
        self.group = group
        self.tag_name = tag_name
        super(STOFC2015r7FoodEntry, self).__init__(_id, food)

    def to_dict(self):
        return {'id': self.id,
                'classification': {'group': self.group,
                                   'tag_name': self.tag_name},
                'food': self.food.to_dict()}
