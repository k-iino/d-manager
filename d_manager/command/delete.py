import argparse

from d_manager.book import BaseBook
from d_manager.book.deleter import ProductFoodDeleter
from d_manager.book.dumper import PickleFileDumper
from d_manager.command import BaseCommand
from d_manager.io.book_loader import ProductFoodPickleLoader

SUB_COMMANDS = {'product_food': 'product_food',
                }


class DeleteCommand(BaseCommand):
    def do(self):
        sub = self.args[0]

        if sub == SUB_COMMANDS['product_food']:
            args = self.args[1:]
            parser = argparse.ArgumentParser(description='市販食品を指定した Pickle ファイルから削除する。')
            parser.add_argument("-i", "--input", type=str,
                                required=True,
                                help="食品を削除する Pickle ファイル")
            parser.add_argument("-t", "--target_id", type=str,
                                required=True,
                                help="削除する食品の id")
            # parser.add_argument("-f", "--force", type=str,
            #                     required=False,
            #                     help="確認なしに削除する")
            _args = parser.parse_args(args)
            pickle_file = _args.input
            target_id = _args.target_id

            book = BaseBook()
            book.set_loader(ProductFoodPickleLoader(pickle_file))
            book.load()

            book.set_deleter(ProductFoodDeleter(target_id=target_id))
            book.delete()

            # 追記モード（'ab'）でファイルを開いて書き込むと、
            # 追記前のデータが残るため取り出したときに追加したエントリが取り出せないので注意。
            book.set_dumper(PickleFileDumper(pickle_file, mode='wb'))
            book.dump()
