import json
import os
import sys

from d_manager.food.builder import FoodBuilder
from d_manager.nutrient.provider.basic import BasicNutrientsProvider
from d_manager.meal.meal import Meal

FOODS_DATABASE_ROOT_DIR_ENVVAR = 'D_MANAGER_FOODS'


class MealCommand:
    """食事した記録から、食品情報を含めた食事内容の JSON を生成するコマンド"""
    def __init__(self, args):
        self.args = args
        self.food_db_root = None
        if FOODS_DATABASE_ROOT_DIR_ENVVAR in os.environ:
            self.food_db_root = os.environ[FOODS_DATABASE_ROOT_DIR_ENVVAR]
        else:
            raise EnvironmentError('環境変数 {} が設定されていません。'.format(FOODS_DATABASE_ROOT_DIR_ENVVAR))

    def _get_food_json(self, genre, id):
        food_json = None

        genre_dir = os.path.join(self.food_db_root, genre)
        for file in os.listdir(genre_dir):
            name, _ = os.path.splitext(file)
            if int(name) == id:
                json_file = os.path.join(genre_dir, file)
                with open(json_file) as jf:
                    food_json = json.load(jf)

        if food_json is None:
            raise FileNotFoundError('ディレクトリ: {}, ID: {}'.format(genre_dir, id))
        else:
            return food_json

    def do(self):
        """コマンド本体"""
        if len(self.args) > 0:
            json_file = self.args[0]
            with open(json_file) as jf:
                meal_src = json.load(jf)
        else:
            # ファイルの指定がなければ標準入力から受け取る
            stdin = ""
            for l in sys.stdin:
                stdin += l
            else:
                meal_src = json.dumps(stdin)

        # 食品情報
        nutrient_provider = BasicNutrientsProvider()
        food_builder = FoodBuilder(nutrient_provider)
        # 食事情報
        meal = Meal()

        # JSON のパース
        for i in meal_src:
            genre = i[0]
            food_id = i[1]
            scale = i[2]

            # 食事情報
            food = self._get_food_json(genre, int(food_id))
            food = food_builder.build(food['name'], food['amount'], food['nutrients'])
            meal.append_food(food, scale)

        print(meal.to_json())

if __name__ == '__main__':
    cmd = MealCommand(sys.argv)
    cmd.do()
