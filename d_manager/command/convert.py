import argparse

from d_manager.command import BaseCMD

from d_manager.book import Book
from d_manager.book.loader import STOFC2015r7FoodExcelLoader
from d_manager.book.loader import STOFC2015r7FoodPickleLoader
from d_manager.book.dumper import PickleStdOutDumper
from d_manager.book.dumper import PickleFileDumper

SUB_COMMANDS = {'stofc2015r7': 'stofc2015r7',  # 日本食品標準成分表2015年版（七訂）の変換
                }


class ConvertToPickleCMD(BaseCMD):
    def do(self):
        sub = self.args[0]

        if sub == SUB_COMMANDS['stofc2015r7']:
            args = self.args[1:]
            parser = argparse.ArgumentParser(description='日本食品標準成分表2015年版（七訂）のエクセルファイルを Pickle ファイルにコンバートする.')
            parser.add_argument("-i", "--input", type=str,
                                required=True,
                                help="入力ファイル")
            parser.add_argument("-a", "--append", type=str,
                                required=False,
                                help="追記する Pickle ファイル")
            _args = parser.parse_args(args)

            book = Book()
            if _args.append:
                # 追記する場合は標準出力に出力せず追加する。
                print('append:', _args.input, ' to ', _args.append)
                book.set_loader(STOFC2015r7FoodPickleLoader(_args.append))
                book.load()
                book.set_loader(STOFC2015r7FoodExcelLoader(_args.input))
                book.load()
                # 追記モード（'ab'）でファイルを開いて書き込むと、
                # 追記前のデータが残るため取り出したときに追加したエントリが取り出せないので注意。
                book.set_dumper(PickleFileDumper(_args.append, mode='wb'))
                book.dump()
            else:
                # 追記する Pickle ファイルが指示されていない場合は標準出力に出力する。
                book.set_loader(STOFC2015r7FoodExcelLoader(_args.input))
                book.load()
                book.set_dumper(PickleStdOutDumper())
                book.dump()

        else:
            raise Exception('サブコマンド %s は未定義です。' % sub)
