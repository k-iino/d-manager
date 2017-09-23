from d_manager.food import Food


class FoodBuilder:
    def __init__(self, nutrient_provider):
        self.nutrient_provider = nutrient_provider

    def build(self, name, amount, nutrients):
        food = Food(name, amount)
        for n_name, n_amount in nutrients.items():
            # todo パース不可能な栄養素が合った場合は、例外をキャッチして次の栄養素にループを継続する
            nutrient = self.nutrient_provider.provide_from_str(n_name, n_amount)
            food.set_nutrient(n_name, nutrient)

        return food
