import os
import argparse
import yaml

from d_manager.command.add import BaseCommand
from d_manager.book.meal_book import MealBook
from d_manager.io.book_loader.pickle_book_loader import STOFC2015FoodBookPickleLoader
from d_manager.io.book_loader.pickle_book_loader import ProductFoodBookPickleLoader
from d_manager.io.book_loader.pickle_book_loader import MealBookPickleLoader
from d_manager.io.book_writer.pickle_book_writer import PickleBookWriter
from d_manager.io.book_loader.interactive_meal_book_loader import InteractiveMealBookLoader

# 設定ファイル
SOURCE_TYPES = ()


class AddMealLogCommand(BaseCommand):
    """食品ログを記録するコマンド"""
    def __init__(self, args):
        parser = argparse.ArgumentParser(description='食事ログを追加する。')
        parser.add_argument("-l", "--log", type=str,
                            required=True,
                            help="食事ログを追記するファイル")
        parser.add_argument("-c", "--config", type=str,
                            required=True,
                            help="設定ファイル")
        self.__args = parser.parse_args(args)
        self.log_file = self.__args.log
        self.config_file = self.__args.config

        if not os.path.exists(self.__args.config):
            raise FileNotFoundError('設定ファイルが見つかりません。')
        else:
            with open(self.config_file) as cf:
                self.configs = yaml.load(cf)

    def do(self):
        if os.path.exists(self.log_file):
            meal_book = MealBookPickleLoader(self.log_file).load()
        else:
            meal_book = MealBook()

        # 食品データのファイルの準備
        product_food_book = None
        stofc2015_food_book = None

        for config in self.configs:
            if config['type'] == 'product_food':
                product_food_book = ProductFoodBookPickleLoader(config['file']).load()
            elif config['type'] == 'stofc2015_food':
                stofc2015_food_book = STOFC2015FoodBookPickleLoader(config['file']).load()

        # 対話的に読み取り
        loader = InteractiveMealBookLoader([product_food_book,
                                            stofc2015_food_book])
        loader.load(meal_book)

        # 食事ログファイルへの書き込み
        # 追記モード（'ab'）でファイルを開いて書き込むと、
        # 追記前のデータが残るため取り出したときに追加したエントリが取り出せないので注意。
        writer = PickleBookWriter(self.log_file, mode='wb')
        writer.write(meal_book)
