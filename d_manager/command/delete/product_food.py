import os
import argparse
import yaml

from d_manager.command.add import BaseCommand
from d_manager.book.product_food_book import ProductFoodBook
from d_manager.io.book_loader.interactive_product_food_book_loader import Helper as InteractiveHelper
from d_manager.io.book_loader.pickle_book_loader import ProductFoodBookPickleLoader
from d_manager.io.book_writer.pickle_book_writer import PickleBookWriter


class DeelteProductFoodCommand(BaseCommand):
    """指定した総合 ID の食品を Book に追加するコマンド"""
    def __init__(self, args):
        parser = argparse.ArgumentParser(description='対話的に市販食品を追加する。')
        parser.add_argument("-i", "--input", type=str,
                            required=True,
                            help="食品を削除する Pickle ファイル")
        parser.add_argument("-t", "--target_id", type=str,
                            required=True,
                            help="削除する食品の総合 ID")
        self.__args = parser.parse_args(args)

    def do(self):
        pickle_file = self.__args.input
        delete_target_id = self.__args.target_id

        if not os.path.exists(pickle_file):
            raise ValueError('{} が見つかりません。'.format(pickle_file))

        pickle_loader = ProductFoodBookPickleLoader(pickle_file)
        food_book = pickle_loader.load()

        # 確認をする
        target_food = food_book.get_entry_by_total_id(delete_target_id)
        print('以下の食品を削除します。よろしいですか？')
        print(yaml.dump(target_food.to_dict()))
        if InteractiveHelper.confirm_yes_of_no():
            food_book.delete(delete_target_id)

            # 追記モード（'ab'）でファイルを開いて書き込むと、
            # 追記前のデータが残るため取り出したときに追加したエントリが取り出せないので注意。
            writer = PickleBookWriter(pickle_file, mode='wb')
            writer.write(food_book)
        else:
            print('キャンセルされました。')
