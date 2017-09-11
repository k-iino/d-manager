import argparse

from d_manager.command.add import BaseCommand

from d_manager.book.product_food_book import ProductFoodBook


class DeelteProductFoodCommand(BaseCommand):
    """市販の食品を Book に追加するコマンド"""
    def __init__(self, args):
        parser = argparse.ArgumentParser(description='対話的に市販食品を追加する。')
        parser.add_argument("-i", "--input", type=str,
                            required=True,
                            help="食品を削除する Pickle ファイル")
        parser.add_argument("-t", "--target", type=str,
                            required=True,
                            help="削除する食品の ID")
        self.__args = parser.parse_args(args)

    def do(self):
        pickle_file = self.__args.input
        delete_target = self.__args.target
        raise NotImplementedError
