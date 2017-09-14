import argparse

from d_manager.command import BaseCommand
from d_manager.io.book_loader.pickle_book_loader import ProductFoodBookPickleLoader
from d_manager.io.book_writer.product_food_book_csv_writer import ProductFoodBookCSVWriter

FORMATS = {'csv': None,
           # "'yaml': None,
           }


class ViewProductFoodPickleFileCommand(BaseCommand):
    """市販食品の  Pickle ファイルを指定した形式で表示するコマンド"""
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
        pickle_loader = ProductFoodBookPickleLoader(self.__source_pickle)
        book = pickle_loader.load()

        if self.__output_format == 'csv':
            writer = ProductFoodBookCSVWriter()
            writer.write(book)
        elif self.__output_format == 'yaml':
            raise NotImplementedError
