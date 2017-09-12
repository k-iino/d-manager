import unittest

from d_manager.food.stofc2015_food import STOFC2015Food


class STOFC2015FoodTestCase(unittest.TestCase):
    def test_init(self):
        valid_group_id = 1
        food_id_in_group = 1
        food_id = 1
        group_list = ['group1', 'group2']
        tag_list = ['tag1', 'tag2', 'tag3']
        food_amount = '100g'
        nutrients = ['1kcal', '1g', '2g', '3g', '4g']
        stofc2015_food = STOFC2015Food(valid_group_id,
                                       food_id_in_group,
                                       food_id,
                                       group_list, tag_list,
                                       food_amount)
        stofc2015_food.set_nutrients_list(nutrients)

        invalid_group_id = 'invalid'
        with self.assertRaises(ValueError):
            stofc2015_food = STOFC2015Food(invalid_group_id,
                                           food_id_in_group,
                                           food_id,
                                           group_list, tag_list,
                                           food_amount)


if __name__ == '__main__':
    unittest.main()
