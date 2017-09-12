import os
import argparse

from d_manager.command.add import BaseCommand

from d_manager.book.product_food_book import ProductFoodBook
from d_manager.io.book_loader.pickle_book_loader import PickleProductFoodBookLoader
from d_manager.io.book_loader.interactive_book_loader import InteractiveProductFoodBookLoader
from d_manager.io.book_writer.pickle_book_writer import PickleBookWriter


class AddProductFoodCommand(BaseCommand):
    """市販の食品を Book に追加するコマンド"""
    def __init__(self, args):
        parser = argparse.ArgumentParser(description='対話的に市販食品を追加する。')
        parser.add_argument("-i", "--input", type=str,
                            required=True,
                            help="食品を追加する Pickle ファイル")
        self.__args = parser.parse_args(args)

    def do(self):
        pickle_file = self.__args.input

        # 存在する場合は先に読み込んでおく。
        if os.path.exists(pickle_file):
            pickle_loader = PickleProductFoodBookLoader(pickle_file)
            book = pickle_loader.load()
        else:
            book = ProductFoodBook()

        # 対話的に読み込む
        interactive_loader = InteractiveProductFoodBookLoader()
        interactive_loader.load(book)

        # 追記モード（'ab'）でファイルを開いて書き込むと、
        # 追記前のデータが残るため取り出したときに追加したエントリが取り出せないので注意。
        writer = PickleBookWriter(pickle_file, mode='wb')
        writer.write(book)
