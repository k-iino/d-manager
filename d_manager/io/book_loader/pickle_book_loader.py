import pickle

from d_manager.food import FOOD_GROUPS
from d_manager.book.product_food_book import ProductFoodBook


class PickleBookLoader:
    def __init__(self, pickle_file):
        self._pickle_file = pickle_file
        pass

    def load(self, book):
        raise NotImplementedError


class PickleProductFoodBookLoader(PickleBookLoader):
    def load(self, new_book):
        with open(self._pickle_file, mode='rb') as f:
            old_book = pickle.load(f)
            if not isinstance(old_book, ProductFoodBook):
                raise ValueError('不正な値です。 Pickle ファイルに予想とは異なる型のデータが含まれています。')

            # 古い ProductFoodBook を食品群毎に読み込んで新しいものに追加していく。
            # この際に、元の分類と食品群内での ID を新しいものでも保持する必要がある。
            for group_number in FOOD_GROUPS.keys():
                entries = old_book.get_entries_by_group(group_number)
                for id_in_group, product_food in entries.items():
                    new_book.append(product_food, group_number, id_in_group)
