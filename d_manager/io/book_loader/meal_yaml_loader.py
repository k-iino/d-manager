import yaml
import datetime

from d_manager.meal import Meal
from d_manager.meal import MealItem
from d_manager.meal import AdjustMealItem
from d_manager.book.meal_book import MealBook
from d_manager.config.meal_yaml_config import MealYAMLConfig
from d_manager.nutrient.basics import Energy, Protein, Lipid, Carbohydrate, SaltEquivalent
from d_manager.helper.datetime_helper import DateTimeHelper
from d_manager.io.book_loader.pickle_book_loader import STOFC2015FoodBookPickleLoader
from d_manager.io.book_loader.pickle_book_loader import ProductFoodBookPickleLoader

# 各要素のキー
DATETIME_KEY = 'datetime'
DATE_KEY = 'date'
FOOD_KEY = 'food'
ADJUST_KEY = 'adjust'
MEMO_KEY = 'memo'


class MealYAMLLoader:
    """食事の YAML を読み込み、Book にセットする"""
    def __init__(self, config):
        if isinstance(config, MealYAMLConfig):
            self.__config = config
        else:
            raise ValueError

    def __get_taking_time(self, meal_y):
        """時刻取得"""
        if DATETIME_KEY in meal_y.keys():
            taking_time = meal_y[DATETIME_KEY]
        elif DATE_KEY in meal_y.keys():
            taking_time = meal_y[DATE_KEY]
        else:
            # 取得できなければ今現在の時刻を使う
            taking_time = datetime.datetime.now()

        # 以下の記述も許容する
        # if taking_time in ('now', 'today', 'yesterday')
        #     raise NotImplementedError
        
        return DateTimeHelper.get_datetime(taking_time)

    def __get_meal_items(self, y):
        """食事の項目のリストを取得する"""
        meal_items = list()

        # 食品はひとつもなく一時的な栄養素の登録も認める
        if FOOD_KEY not in y.keys():
            return meal_items

        for food_info in y[FOOD_KEY]:
            # カンマ区切り
            _t = food_info.split(',')
            _type = _t[0]
            _id = int(_t[1])
            _scale = float(_t[2])
            _food_book_file = self.__config.get_book_from_type(_type)
            if _type == 'product':
                loader = ProductFoodBookPickleLoader(_food_book_file)
                _food_book = loader.load()
            elif _type == 'stofc2015':
                loader = STOFC2015FoodBookPickleLoader(_food_book_file)
                _food_book = loader.load()
            else:
                raise NotImplementedError
            # 全ての Book クラスに以下のメソッドが実装されていること前提。
            _food = _food_book.get_by_total_id(_id)
            meal_items.append(MealItem(_food, _scale))

        return meal_items

    def __get_adjust_nutrients(self, y):
        adjust_nutrients = list()

        # 調整用の栄養素は設定されてなくてもよい。
        if ADJUST_KEY not in y.keys():
            return adjust_nutrients

        for name, amount in y[ADJUST_KEY].items():
            n = name.lower()
            if n in ('energy', 'ene'):
                adjust_nutrients.append(Energy(amount))
            elif n in ('protein', 'pro'):
                adjust_nutrients.append(Protein(amount))
            elif n in ('lipid'):
                adjust_nutrients.append(Lipid(amount))
            elif n in ('carbohydrate', 'carbo'):
                adjust_nutrients.append(Carbohydrate(amount))
            elif n in ('salt_equivalent', 'salt'):
                adjust_nutrients.append(SaltEquivalent(amount))
            else:
                raise NotImplementedError

        return adjust_nutrients

    def __get__memo(self, y):
        # 調整用の栄養素は設定されてなくてもよい。
        if MEMO_KEY not in y.keys():
            return ''
        else:
            return y[MEMO_KEY]

    def load(self, book, yaml_file):
        if not isinstance(book, MealBook):
            raise ValueError
        with open(yaml_file, mode='r') as f:
            meal_yaml = yaml.load(f)

        taking_datetime = self.__get_taking_time(meal_yaml)
        meal_items = self.__get_meal_items(meal_yaml)
        adjust_nutrients = self.__get_adjust_nutrients(meal_yaml)
        memo = self.__get__memo(meal_yaml)

        meal = Meal(taking_datetime, memo)
        for m_item in meal_items:
            meal.append(m_item)
        if len(adjust_nutrients) > 0:
            adjust_item = AdjustMealItem()
            adjust_item.set_nutrients(adjust_nutrients)
            meal.append(adjust_item)
        
        return meal
