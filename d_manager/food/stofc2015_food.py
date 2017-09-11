"""
STOFC2015: STANDARD TABLES OF FOOD COMPOSITION IN JAPAN - 2015
"""

from d_manager.food import BaseFood


class STOFC2015BaseFood(BaseFood):
    """日本食品標準成分表2015年版の食品"""
    def __init__(self, _id, group, tag_name, amount):
        self.id = _id
        self.group = group
        self.tag_name = tag_name
        # 名前は CSV 出力のことを考えてカンマでは区切らない
        name = ' '.join(tag_name)
        super(STOFC2015BaseFood, self).__init__(name, amount)

    def to_dict(self):
        return {'id': self.id,
                'classification': {'group': self.group,
                                   'tag_name': self.tag_name},
                'food': super().to_dict()}
