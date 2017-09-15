import argparse

from d_manager.command import BaseCommand
from d_manager.io.book_loader.pickle_book_loader import MealBookPickleLoader
from d_manager.io.book_writer.meal_log_csv_writer import CSVMealLogWriter

FORMATS = {'csv': None,
           }


class ViewMealLogPickleFileCommand(BaseCommand):
    """市販食品の  Pickle ファイルを指定した形式で表示するコマンド"""
    def __init__(self, args):
        parser = argparse.ArgumentParser(description='対話的に市販食品を追加する。')
        # Optional
        parser.add_argument("-m", "--meal_log", type=str,
                            required=True,
                            help="表示する Pickle ファイル")
        parser.add_argument("-t", "--type", type=str, default='csv',
                            required=False,
                            help="表示形式")
        parser.add_argument('-s', "--summary",
                            action="store_true",
                            required=False,
                            help="日毎の概要を表示")
        self.__args = parser.parse_args(args)
        self.__source_pickle = self.__args.meal_log
        self.__is_summary = self.__args.summary
        if self.__args.type not in FORMATS.keys():
            raise ValueError('形式 {} には対応していません。'.format(self.__args.type))
        else:
            self.__output_format = self.__args.type

    def do(self):
        pickle_loader = MealBookPickleLoader(self.__source_pickle)
        food_book = pickle_loader.load()

        if self.__output_format == 'csv':
            writer = CSVMealLogWriter()
            if self.__is_summary:
                writer.daily_summary(food_book)
            else:
                writer.write(food_book)
        elif self.__output_format == 'yaml':
            raise NotImplementedError
