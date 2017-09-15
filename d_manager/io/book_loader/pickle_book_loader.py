import pickle

from d_manager.book.product_food_book import ProductFoodBook
from d_manager.book.stofc2015_food_book import STOFC2015FoodBook
from d_manager.book.meal_book import MealBook


class BookPickleLoader:
    def __init__(self, pickle_file):
        self._pickle_file = pickle_file
        pass

    def load(self):
        raise NotImplementedError


class ProductFoodBookPickleLoader(BookPickleLoader):
    def load(self):
        with open(self._pickle_file, mode='rb') as f:
            old_book = pickle.load(f)
            if not isinstance(old_book, ProductFoodBook):
                raise ValueError('不正な値です。 Pickle ファイルに予想とは異なる型のデータが含まれています。')
            else:
                return old_book

            # 以下のように、新しく Book を作りなおすと、
            # 内部のエントリの ID が採番され直すので削除されたエントリと同じ ID のエントリが作成される。
            # 一度削除したエントリの ID は欠番にしたい。
            # for group_number in FOOD_GROUPS.keys():
            #     entries = old_book.get_entries_by_group(group_number)
            #     for id_in_group, product_food in entries.items():
            #         new_book.append(product_food, group_number, id_in_group)


# load はスタティックメソッドでよい。
# この辺の継承関係は調整したい。
class STOFC2015FoodBookPickleLoader(BookPickleLoader):
    """Pickle ファイルから日本食品標準成分表2015年版（七訂）の食品を読み込むローダー"""
    def load(self):
        with open(self._pickle_file, mode='rb') as f:
            book = pickle.load(f)
            if isinstance(book, STOFC2015FoodBook):
                return book
            else:
                raise ValueError('不正な値です。 Pickle ファイルに予想とは異なる型のデータが含まれています。')


class MealBookPickleLoader(BookPickleLoader):
    """Pickle ファイルか食事ログを読み込むローダー"""
    def load(self):
        with open(self._pickle_file, mode='rb') as f:
            old_book = pickle.load(f)
            if not isinstance(old_book, MealBook):
                raise ValueError('不正な値です。 Pickle ファイルに予想とは異なる型のデータが含まれています。')
            else:
                return old_book
