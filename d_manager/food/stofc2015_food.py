"""
STOFC2015: STANDARD TABLES OF FOOD COMPOSITION IN JAPAN - 2015
日本食品標準成分表2015年版（七訂）の食品群
"""
from d_manager.food import BaseFood


class STOFC2015Food(BaseFood):
    """日本食品標準成分表2015年版の食品"""
    def __init__(self, groups, tags, amount):
        self.groups = groups
        self.tags = tags
        # 名前は CSV 出力のことを考えてカンマでは区切らない
        name = ' '.join(tags)
        super(STOFC2015Food, self).__init__(name, amount)
