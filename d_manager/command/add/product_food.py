import os
import argparse

from d_manager.command.add import BaseCommand

from d_manager.book.product_food_book import ProductFoodBook
from d_manager.io.book_loader.pickle_book_loader import ProductFoodBookPickleLoader
from d_manager.io.book_loader.interactive_product_food_book_loader import InteractiveProductFoodBookLoader
from d_manager.io.book_writer.pickle_book_writer import PickleBookWriter
from d_manager.config.meal_yaml_config import MealYAMLConfig
from d_manager.config.meal_yaml_config import PRODUCT_FOOD_BOOK_TYPE

# 設定ファイル
D_MANAGER_PATH = 'D_MANAGER_PATH'  # 環境変数
DEFAULT_CONF_FILE = 'config'


class AddProductFoodCommand(BaseCommand):
    """市販の食品を Book に追加するコマンド"""
    def __init__(self, args):
        # parser = argparse.ArgumentParser(description='対話的に市販食品を追加する。')
        # parser.add_argument("-b", "--book", type=str,
        #                     required=False,
        #                     help="食品を追加するデータベースファイル")
        # parsed_args = parser.parse_args(args)

        # 設定ファイル
        # 環境変数で指定されたディレクトリ以下の設定ファイルを読み込む
        self.config = None
        if D_MANAGER_PATH in os.environ:
            d_home_dir = os.environ[D_MANAGER_PATH]
            if os.path.exists(d_home_dir) and os.path.isdir(d_home_dir):
                config_file = os.path.join(d_home_dir, DEFAULT_CONF_FILE)
                # 設定読み込み
                self.config = MealYAMLConfig(config_file)
            else:
                ValueError('{} が存在しません。'.format(d_home_dir))
        else:
            ValueError('環境変数 {} が設定されていません。'.format(D_MANAGER_PATH))

        # # 設定ファイルが存在しないなら、オプションに指定してあるファイルを利用する
        # self.book_file = None
        # if self.config is None:
        #     self.book_file = parsed_args.book


    def do(self):
        # 読み込む Pickle ファイルは設定ファイルを優先
        if self.config is not None:
            pickle_file = self.config.get_book_from_type(PRODUCT_FOOD_BOOK_TYPE)
        # elif self.book_file is not None:
        #     pickle_file = self.book_file
        else:
            ValueError('設定ファイルが設定されていません。')

        # 存在する場合は先に読み込んでおく。
        if os.path.exists(pickle_file):
            pickle_loader = ProductFoodBookPickleLoader(pickle_file)
            book = pickle_loader.load()
        else:
            book = ProductFoodBook()

        # 対話的に読み込む
        print('{} を読み込みます。'.format(pickle_file))
        interactive_loader = InteractiveProductFoodBookLoader()
        interactive_loader.load(book)

        # 追記モード（'ab'）でファイルを開いて書き込むと、
        # 追記前のデータが残るため取り出したときに追加したエントリが取り出せないので注意。
        writer = PickleBookWriter(pickle_file, mode='wb')
        writer.write(book)
