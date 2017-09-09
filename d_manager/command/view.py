import sys
import argparse

from d_manager.book import Book
from d_manager.command import BaseCMD
from d_manager.book.loader import STOFC2015r7FoodPickleLoader
from d_manager.book.dumper import YAMLDumper

SUB_COMMANDS = {'stofc2015r7': 'stofc2015r7',  # 日本食品標準成分表2015年版（七訂）の変換
                }


class ViewPickleAsYamlCMD(BaseCMD):
    def do(self):
        sub = self.args[0]

        if sub == SUB_COMMANDS['stofc2015r7']:
            args = self.args[1:]
            parser = argparse.ArgumentParser(description='日本食品標準成分表2015年版（七訂）のエクセルファイルを Pickle ファイルにコンバートする.')
            parser.add_argument("-i", "--input", type=str,
                                required=True,
                                help="入力ファイル")
            _args = parser.parse_args(args)
            # 標準入力から読み込めるようにすべきか？
            # if _args.input:
            #     _input = _args.input
            # else:
            #     _input = sys.stdin
            _input = _args.input

            book = Book(STOFC2015r7FoodPickleLoader(_input),
                        YAMLDumper())
            book.load()
            book.dump()
        else:
            raise Exception('サブコマンド %s は未定義です。' % sub)
