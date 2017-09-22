import json
import sys

from d_manager.meal.meal import Meal
from d_manager.food.builder import FoodBuilder
from d_manager.nutrient.provider.basic import BasicNutrientsProvider


class SummaryCommand:
    def __init__(self, args):
        self.args = args

    def do(self):
        # 食品情報
        nutrient_provider = BasicNutrientsProvider()
        food_builder = FoodBuilder(nutrient_provider)
        # 複数の食事記録を一つの食事記録にまとめてから要約を作成する
        base_meal = Meal()
        
        if len(self.args) > 0:
            # 複数の JSON ファイルの指定を受け付ける
            for json_file in self.args:
                with open(json_file) as jf:
                    j = json.load(jf)
                    for i in j:
                        # fixme
                        # 実際には食品情報ではなく、食事記録の項目である
                        # 食事（Meal）関係にしては Builder クラスなどを作っていないので、
                        # 食事を Food に変換してから食事情報をまとめている
                        food = food_builder.build(i['name'], i['amount'], i['nutrients'])
                        base_meal.append_food(food, 1)  # スケールは既に調整済みなので 1 固定
        else:
            # ファイルの指定がなければ標準入力から受け取る
            stdin = ""
            for l in sys.stdin:
                stdin += l
            else:
                j = json.dumps(stdin)
                for i in j:
                    food = food_builder.build(i['name'], i['amount'], i['nutrients'])
                    base_meal.append_food(food, 1)

        summary_json = base_meal.to_summary_json()

        # todo CSV 出力
        # 別コマンドでいいか。例えば、 summary2csv など

        print(summary_json)
