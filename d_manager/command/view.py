import argparse

from d_manager.book import BaseBook
from d_manager.book.dumper import YAMLDumper
from d_manager.command import BaseCommand
from d_manager.io.book_loader import ProductFoodPickleLoader
from d_manager.io.book_loader import STOFC2015r7FoodPickleLoader

SUB_COMMANDS = {'product_food': 'product_food',
                'stofc2015r7': 'stofc2015r7',  # 日本食品標準成分表2015年版（七訂）の変換
                }


class ViewPickleAsYamlCommand(BaseCommand):
    def do(self):
        sub = self.args[0]

        if sub == SUB_COMMANDS['stofc2015r7']:
            args = self.args[1:]
            parser = argparse.ArgumentParser(description='日本食品標準成分表2015年版（七訂）の Pickle ファイルの内容を YAML 形式に表示。')
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
            book = BaseBook(STOFC2015r7FoodPickleLoader(_input),
                            YAMLDumper())
            book.load()
            book.dump()

        elif sub == SUB_COMMANDS['product_food']:
            args = self.args[1:]
            parser = argparse.ArgumentParser(description='市販食品の Pickle ファイルの内容を YAML 形式に表示。')
            parser.add_argument("-i", "--input", type=str,
                                required=True,
                                help="入力ファイル")
            _args = parser.parse_args(args)
            _input = _args.input
            book = BaseBook(ProductFoodPickleLoader(_input),
                            YAMLDumper())
            book.load()
            book.dump()
        else:
            raise Exception('サブコマンド %s は未定義です。' % sub)
