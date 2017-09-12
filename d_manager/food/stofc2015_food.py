"""
STOFC2015: STANDARD TABLES OF FOOD COMPOSITION IN JAPAN - 2015
"""

from d_manager.food import BaseFood
from d_manager.food import FOOD_GROUPS


ID_KEY = 'id'
CLASSIFICATION_KEY = 'classification'
GROUP_ID_KEY = 'group_id'
ID_IN_GROUP_KEY = 'id_in_group'
GROUP_NAME_KEY = 'group'
TAG_NAME_KEY = 'tag'
FOOD_KEY = 'food'


class STOFC2015Food(BaseFood):
    """日本食品標準成分表2015年版の食品"""
    def __init__(self, group_id, food_id_in_group, food_id, group_list, tag_list, amount):
        if group_id not in FOOD_GROUPS.keys():
            raise ValueError

        self.group_id = group_id
        self.id_in_group = food_id_in_group
        self.id = food_id
        self.group_list = group_list
        self.tag_list = tag_list
        # 名前は CSV 出力のことを考えてカンマでは区切らない
        name = ' '.join(tag_list)
        super(STOFC2015Food, self).__init__(name, amount)

    def set_nutrients_list(self, l):
        """栄養素の情報をリスト形式でセットする。"""
        super(STOFC2015Food, self).set_nutrients_list(l)

    def to_dict(self):
        return {ID_KEY: self.id,
                CLASSIFICATION_KEY: {GROUP_ID_KEY: self.group_id,
                                     GROUP_NAME_KEY: self.group_list,
                                     TAG_NAME_KEY: self.tag_list},
                FOOD_KEY: super().to_dict()}
    
    def get_label_of_list(self):
        _label = [GROUP_ID_KEY,
                  ID_IN_GROUP_KEY,
                  ID_KEY,
                  GROUP_NAME_KEY,
                  TAG_NAME_KEY]
        # BaseFood の名前はタグと重複しているので除く
        return _label + super().get_label_of_list()[1:]

    def to_list(self):
        _list = [self.group_id,
                 self.id_in_group,
                 self.id,
                 ' '.join(self.group_list),
                 ' '.join(self.tag_list)]
        # BaseFood の名前はタグと重複しているので除く
        return _list + super().to_list()[1:]
