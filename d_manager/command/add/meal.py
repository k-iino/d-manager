import os
import argparse

from d_manager.command.add import BaseCommand
from d_manager.book.meal_book import MealBook
from d_manager.config.meal_yaml_config import MealYAMLConfig
from d_manager.io.book_loader.pickle_book_loader import MealBookPickleLoader
from d_manager.io.book_writer.pickle_book_writer import PickleBookWriter
from d_manager.io.book_loader.meal_interactive_loader import MealInteractiveLoader
from d_manager.io.book_loader.meal_yaml_loader import MealYAMLLoader
from d_manager.helper.prompt_helper import  PromptHelper

# 設定ファイル
D_MANAGER_PATH = 'D_MANAGER_PATH'  # 環境変数
DEFAULT_CONF_FILE = 'config'


class AddMealCommand(BaseCommand):
    """食品ログを記録するコマンド"""
    def __init__(self, args):
        # 入力ファイル
        self.__meal_input = None
        # 食事 Book
        self.__meal_book = None

        # 暗黙の設定ファイルを利用
        # 食事を YAML 形式のテキストファイルから読み込む
        # d-manager add meal -i meal.yaml
        # 食事を対話的に読み込む
        # d-manager add meal
        #
        # 明示的に設定ファイルを指定する
        # 食事を YAML 形式のテキストファイルから読み込む
        # d-manager add meal -c config -i meal.yaml
        # 食事を対話的に読み込む
        # d-manager add meal -c config
        parser = argparse.ArgumentParser(description='食事ログを追加する。')
        parser.add_argument("-m", "--meal", type=str,
                            required=True,  # 現状は YAML ファイルのみ
                            help="食事内容が記録された入力ファイル（YAML形式）")
        parser.add_argument("-c", "--config", type=str,
                            required=False,
                            help="設定ファイル")
        parser.add_argument('-f', '--force',
                            required=False,
                            action="store_true",
                            help="確認せずに登録する。")
        # parser.add_argument("-l", "--log", type=str,
        #                     required=False,
        #                     help="食事ログを追記するファイル")
        parsed_args = parser.parse_args(args)

        # 入力ファイル
        self.__meal_input = parsed_args.meal
        # 確認せずに強制的に書き込むか
        self.__force = parsed_args.force

        # 設定ファイルを優先する
        if D_MANAGER_PATH in os.environ:
            d_home_dir = os.environ[D_MANAGER_PATH]
            if os.path.exists(d_home_dir) and os.path.isdir(d_home_dir):
                self.config_file = os.path.join(d_home_dir, DEFAULT_CONF_FILE)
            else:
                raise EnvironmentError('設定ファイルが見つかりません.',
                                       ' 環境変数 {} の内容が不正です。'.format(d_home_dir),
                                       '存在しないかディレクトリでありません。')
        elif parsed_args.config is not None:
            # 環境変数で指定されたディレクトリ以下の設定ファイルを読み込む
            self.config_file = parsed_args.config
        else:
            raise EnvironmentError('設定ファイルが指定されていません。',
                                   '環境変数にもコマンドのオプションとしても指定されていません。')


    def do(self):
        # 設定読み込み
        config = MealYAMLConfig(self.config_file)

        # 食事ログの準備
        if os.path.exists(config.meal_book):
            meal_book = MealBookPickleLoader(config.meal_book).load()
        else:
            meal_book = MealBook()

        if self.__meal_input is None:
            # 対話的に読み取り
            # todo
            # loader = MealInteractiveLoader(config)
            # loader.load(meal_book)
            raise NotImplementedError
        else:
            loader = MealYAMLLoader(config)
            meal = loader.load(meal_book, self.__meal_input)
            if self.__force:
                meal_book.append(meal)
            else:
                # 確認する
                PromptHelper.print_msg('以下の食品を登録します。よろしいですか?')
                PromptHelper.print_meal(meal)
                if PromptHelper.confirm_yes_of_no():
                    meal_book.append(meal)
                else:
                    PromptHelper.print_msg('キャンセルしました。')

        # 食事ログファイルへの書き込み
        # 追記モード（'ab'）でファイルを開いて書き込むと、
        # 追記前のデータが残るため取り出したときに追加したエントリが取り出せないので注意。
        writer = PickleBookWriter(config.meal_book, mode='wb')
        writer.write(meal_book)
