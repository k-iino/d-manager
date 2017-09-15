from d_manager.food import BaseFood
from d_manager.food.product_food import ProductFood
from d_manager.food.stofc2015_food import STOFC2015Food


class FoodHelper:
    """食品に関する"""
    @staticmethod
    def get_actual_nutrients(food, scale):
        """食品とその食品の食品単位に対する摂取比率から、摂取した実際の栄養素の量を返す"""
        if not isinstance(food, BaseFood):
            raise ValueError

        actual_nutrients = dict()
        for key, nutrient in food.nutrients.items():
            actual_nutrients[key] = nutrient * float(scale)

        return actual_nutrients

    @staticmethod
    def sum_nutrients(food1, scale_of_food1, food2, scale_of_food2):
        """二つの食品の栄養素を加算して求める"""
        pass
        # # 加算した栄養素は辞書から削除するため複製しておく
        # nutrients_of_food1 = dict(food1.nutrients)
        # nutrients_of_food2 = dict(food2.nutrients)
        #
        # result = dict()
        # for k1, v1 in nutrients_of_food1.items():
        #     if k1 in nutrients_of_food2.keys():
        #         # Food1 と Food2 と両方に含まれている栄養素
        #         result[k1] = v1 * scale_of_food1 + nutrients_of_food2[k1] * scale_of_food2
        #         del nutrients_of_food2[k1]
        #     else:
        #         # Food1 に含まれているが Food2 には含まれていない栄養素
        #         result[k1] = v1 * scale_of_food1
        #
        # # Food1 には無く Food2 には含まれている栄養素
        # for k2, v2 in nutrients_of_food2.items():
        #     result[k2] = v2 * scale_of_food2
        #
        # return result
