import json

from d_manager.meal import MealItem
from d_manager.meal import Meal
from d_manager.quantity.quantity import FoodQuantity
from d_manager.nutrient.provider.basic import BasicNutrientsProvider

NAME_KEY = 'name'
AMOUNT_KEY = 'amount'
NUTRIENTS_KEY = 'nutrients'


class MealBuilder:
    def __init__(self):
        self.meal = Meal()

    def build(self):
        """食事記録を得る"""
        return self.meal

    # todo: JSON 入出力関係の実装分離
    def build_json(self):
        """食事記録を JSON で得る"""
        jl = list()
        for meal_item in self.meal.items:
            d = dict()
            d[NAME_KEY] = meal_item.name
            # 量の表示有効桁
            # 食品情報の結びつき
            d[AMOUNT_KEY] = str(meal_item.amount.round(1))
            d[NUTRIENTS_KEY] = dict()
            for k, nutrient in meal_item.nutrients.items():
                d[NUTRIENTS_KEY][k] = str(nutrient.quantity.round(nutrient.ndigits))
            jl.append(d)

        return json.dumps(jl)

    def append_food(self, food, scale):
        """
        摂取した食品を食事記録に追加する

        :param food: 食品データ
        :param scale: 食品の食品単位（基準量）に対する摂取倍率
        :return:
        """
        # 摂取倍率を反映しつつ登録する
        item = MealItem(name=food.name,
                        amount=food.amount * scale,
                        nutrients={name: nutrient * scale
                                   for (name, nutrient) in food.nutrients.items()})
        self.meal.append(item)

    # todo: JSON 入出力関係の実装分離
    def append_json(self, json_str):
        """
        JSON 形式の食事記録から食事記録を追加

        入力サンプル

        [
          {
            "name": "some product food",
            "amount": "150.0 g",
            "nutrients": {
              "energy": "246.0 kcal",
              "protein": "25.0 g",
              "lipid": "5.8 g",
              "carbohydrate": "60.8 g",
              "salt": "0.702 g"
            }
          },
          ...
        ]
        """
        item_list = json.loads(json_str)
        for item_dict in item_list:    
            name = item_dict[NAME_KEY]
            amount = FoodQuantity.from_str(item_dict[AMOUNT_KEY])
            nutrients = dict()

            nutrient_provider = BasicNutrientsProvider()
            for name, amount_str in item_dict[NUTRIENTS_KEY].items():
                nutrients[name] = nutrient_provider.provide_from_str(name, amount_str)

            item = MealItem(name, amount, nutrients)
            self.meal.append(item)
