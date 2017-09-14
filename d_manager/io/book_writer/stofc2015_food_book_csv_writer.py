# import csv

from d_manager.book.stofc2015_food_book import STOFC2015FoodBook
from d_manager.food.stofc2015_food import STOFC2015Food


class STOFC2015FoodBookCSVWriter:
    @staticmethod
    def write(book):
        if not isinstance(book, STOFC2015FoodBook):
            raise ValueError()

        # csv_writer = csv.writer(sys.stdout, lineterminator='\n')
        rows = list()

        # LABEL
        rows.append(['group_id',
                     'food_id',
                     'groups',
                     'tags',
                     'amount',
                     'energy',
                     'protein',
                     'lipid',
                     'carbohydrate',
                     'salt_equivalent',
                     ])

        for group_id, id_in_group, food in book.generator():
            if not isinstance(food, STOFC2015Food):
                raise ValueError()

            _row = [group_id,
                    group_id * 1000 + id_in_group,
                    ' '.join(food.groups),
                    ' '.join(food.tags),
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

        # csv_writer.writerow(rows)
