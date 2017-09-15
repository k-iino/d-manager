import yaml

from d_manager.io.book_loader.pickle_book_loader import STOFC2015FoodBookPickleLoader
from d_manager.io.book_loader.pickle_book_loader import ProductFoodBookPickleLoader

# 食品 Book の Type
STOFC2015_FOOD_BOOK_TYPE = 'stofc2015'
PRODUCT_FOOD_BOOK_TYPE = 'product'


class MealYAMLConfig:
    """食事に関する設定"""
    def __init__(self, yf):
        # 食品 Book
        # 種類から、 Book を呼び出せるようにしたもの
        self.__type_to_book = dict()

        with open(yf, mode='r') as f:
            config = yaml.load(f)

        # 食事ログのデータベース
        if 'meal_book' in config:
            self.meal_book = config['meal_book']

        # 食品データベース
        for food_book in config['food_book']:
            if food_book['type'] == PRODUCT_FOOD_BOOK_TYPE:
                _book = ProductFoodBookPickleLoader(food_book['file']).load()
                self.__type_to_book[PRODUCT_FOOD_BOOK_TYPE] = _book
            elif food_book['type'] == STOFC2015_FOOD_BOOK_TYPE:
                _book = STOFC2015FoodBookPickleLoader(food_book['file']).load()
                self.__type_to_book[STOFC2015_FOOD_BOOK_TYPE] = _book
            else:
                raise NotImplementedError('{} というタイプの food_book には未対応'.format(food_book['type']))

        # 最低一つの食品データベースが必要
        if len(self.__type_to_book) < 0:
            raise ValueError('最低一つの食品データベースの登録が必要です。')

    def get_book_from_type(self, t):
        return self.__type_to_book[t]
