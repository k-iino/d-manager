import argparse
import os

from d_manager.book import Book
from d_manager.command import BaseCMD

SUB_COMMANDS = {'my_food': 'my_food',
                }

class AddMyFoodCMD(BaseCMD):
    def do(self):
        sub = self.args[0]

        if sub == SUB_COMMANDS['my_foods']:
            args = self.args[1:]
            parser = argparse.ArgumentParser(description='対話的に市販食品を追加する。')
            parser.add_argument("-i", "--input", type=str,
                                required=True,
                                help="食品を追加する Pickle ファイル")
            _args = parser.parse_args(args)

            pickle_file = _args.input

            book = Book()
            # 存在しない場合は新規作成するので読み込まない。
            if os.path.exists(pickle_file):
                book.set_loader(STOFC2015r7FoodPickleLoader(_args.append))

            # 追記する場合は標準出力に出力せず追加する。

            book.load()
            book.set_loader(STOFC2015r7FoodExcelLoader(_args.input))
            book.load()
            # 追記モード（'ab'）でファイルを開いて書き込むと、
            # 追記前のデータが残るため取り出したときに追加したエントリが取り出せないので注意。
            book.set_dumper(PickleFileDumper(_args.append, mode='wb'))
            book.dump()
        else:
            raise Exception('サブコマンド %s は未定義です。' % sub)
