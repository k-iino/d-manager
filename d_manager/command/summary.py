import sys

from d_manager.meal.builder import MealBuilder
from d_manager.meal.summarizer import MealNutrientsSummarizer


class SummaryCommand:
    def __init__(self, args):
        self.args = args

    def do(self):
        # 複数の食事記録を一つの食事記録にまとめてから要約を作成する
        meal_builder = MealBuilder()
        
        if len(self.args) > 0:
            # 複数の JSON ファイルの指定を受け入れる
            for json_file in self.args:
                with open(json_file) as f:
                    json_str = f.read()
                    meal_builder.append_json(json_str)
        else:
            # ファイルの指定がなければ標準入力から受け取る
            json_str = ""
            for l in sys.stdin:
                json_str += l
            else:
                meal_builder.append_json(json_str)

        meal = meal_builder.build()
        summarizer = MealNutrientsSummarizer(meal)

        print(summarizer.to_json())
