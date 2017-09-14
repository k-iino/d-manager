import argparse

from d_manager.command import BaseCommand
from d_manager.io.book_loader.pickle_book_loader import STOFC2015FoodBookPickleLoader
from d_manager.io.book_writer.stofc2015_food_book_csv_writer import STOFC2015FoodBookCSVWriter

FORMATS = {'csv': None,
           # 'yaml': None,
           }


class ViewSTOFC2015PickleFileCommand(BaseCommand):
    """日本食品標準成分表2015年版の  Pickle ファイルを指定した形式で表示するコマンド"""
    def __init__(self, args):
        parser = argparse.ArgumentParser(description='対話的に市販食品を追加する。')
        parser.add_argument("-i", "--input", type=str,
                            required=True,
                            help="表示する Pickle ファイル")
        parser.add_argument("-t", "--type", type=str,
                            required=True,
                            help="表示形式")
        self.__args = parser.parse_args(args)
        self.__source_pickle = self.__args.input
        if self.__args.type not in FORMATS.keys():
            raise ValueError('形式 {} には対応していません。'.format(self.__args.type))
        else:
            self.__output_format = self.__args.type

    def do(self):
        pickle_loader = STOFC2015FoodBookPickleLoader(self.__source_pickle)
        food_book = pickle_loader.load()

        if self.__output_format == 'csv':
            writer = STOFC2015FoodBookCSVWriter()
            writer.write(food_book)
        else:
            raise NotImplementedError
