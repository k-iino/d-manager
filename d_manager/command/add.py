import argparse
import os

from d_manager.command import BaseCMD

from d_manager.book import Book
from d_manager.book.loader import ProductFoodPickleLoader
from d_manager.book.loader import InteractivelyProductFoodLoader
from d_manager.book.dumper import PickleFileDumper

SUB_COMMANDS = {'product_food': 'product_food',
                }


class AddInteractivelyCMD(BaseCMD):
    def do(self):
        sub = self.args[0]

        if sub == SUB_COMMANDS['product_food']:
            args = self.args[1:]
            parser = argparse.ArgumentParser(description='対話的に市販食品を追加する。')
            parser.add_argument("-i", "--input", type=str,
                                required=True,
                                help="食品を追加する Pickle ファイル")
            _args = parser.parse_args(args)

            book = Book()
            pickle_file = _args.input
            book.set_loader(ProductFoodPickleLoader(pickle_file))
            # 存在する場合は先に読み込んでおく。
            if os.path.exists(pickle_file):
                book.load()

            # 対話的に読み込む
            book.set_loader(InteractivelyProductFoodLoader())
            book.load()

            # 追記モード（'ab'）でファイルを開いて書き込むと、
            # 追記前のデータが残るため取り出したときに追加したエントリが取り出せないので注意。
            book.set_dumper(PickleFileDumper(pickle_file, mode='wb'))
            book.dump()
        else:
            raise Exception('サブコマンド %s は未定義です。' % sub)
