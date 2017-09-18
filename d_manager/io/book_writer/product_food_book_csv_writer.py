from d_manager.food.product_food import ProductFood
from d_manager.book.product_food_book import ProductFoodBook


class ProductFoodBookCSVWriter:
    @staticmethod
    def write(book):
        if not isinstance(book, ProductFoodBook):
            raise ValueError()

        rows = list()

        # LABEL
        rows.append(['group_id',
                     'food_id',
                     'maker',
                     'product_name',
                     'common_name',
                     'name',
                     'amount',
                     'energy',
                     'protein',
                     'lipid',
                     'carbohydrate',
                     'salt_equivalent',
                     ])

        for group_id, food_id, food in book.generator():
            if not isinstance(food, ProductFood):
                raise ValueError()

            _row = [group_id,
                    food_id,
                    food.maker_name,
                    food.product_name,
                    food.common_name,
                    food.name,
                    food.amount,
                    food.energy,
                    food.protein,
                    food.lipid,
                    food.carbohydrate,
                    food.salt,
                    ]
            rows.append(list(map(lambda x: str(x), _row)))

        for row in rows:
            print(','.join(row))
