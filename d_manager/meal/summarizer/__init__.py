import json


class MealNutrientsSummarizer:
    """栄養成分の要約を作成するクラス"""

    def __init__(self, meal):
        self.meal = meal

    def to_dict(self):
        """栄養成分の要約を辞書で得る"""
        total = dict()
        for item in self.meal.items:
            for name, nutrient in item.nutrients.items():
                if name not in total:
                    total[name] = nutrient
                else:
                    total[name] += nutrient
        return total

    def to_json(self):
        """栄養成分の要約を JSON 形式で得る"""
        summary = dict()
        total_nutrients = self.to_dict()
        for name, nutrient in total_nutrients.items():
            # 表示有効桁を反映する
            summary[name] = str(nutrient.quantity.round(nutrient.ndigits))

        return json.dumps(summary)
