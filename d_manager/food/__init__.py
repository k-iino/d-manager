from d_manager.quantity.quantity import FoodQuantity


class Food:
    def __init__(self, name, amount):
        self.name = str(name)
        self.nutrients = dict()
        # 食品単位
        # 食事に含まれる栄養素がどれくらいの量の食品における含有量かを示す基準となる量。
        # 例えば一般の加工食品だったら「栄養成分表示」に食品単位が重量か体積で示されている
        self.amount = FoodQuantity.from_str(amount)

    def set_nutrient(self, name, nutrient):
        self.nutrients[name] = nutrient
