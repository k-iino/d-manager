import unittest

from d_manager.food import FOOD_GROUPS
from d_manager.food.stofc2015_food import STOFC2015Food
from d_manager.book.stofc2015_food_book import STOFC2015FoodBook
from d_manager.food.product_food import ProductFood


class STOFC2015FoodBookTestCase(unittest.TestCase):
    def test_append(self):
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

        book = STOFC2015FoodBook()
        book.append(stofc2015_food, valid_group_id, food_id_in_group)
        # 一つしか食品を追加していないので、最初に取得できるものと一致する
        for appended in book.generator():
            self.assertEqual(stofc2015_food, appended)

        # 不正なグループ ID
        invalid_group_id = 'invalid'
        with self.assertRaises(ValueError):
            book.append(stofc2015_food, invalid_group_id, food_id_in_group)

        # 不正なエントリ
        product_food = ProductFood(maker_name='maker',
                                   product_name='product',
                                   food_name='food',
                                   amount='100g')
        with self.assertRaises(ValueError):
            book.append(product_food, valid_group_id, food_id_in_group)

    def test_generator(self):
        created_entries = list()

        book = STOFC2015FoodBook()

        group_list = ['group1', 'group2']
        tag_list = ['tag1', 'tag2', 'tag3']
        food_amount = '100g'

        # 全てのグループで適当な数のエントリを作成して登録する
        for i in FOOD_GROUPS.keys():
            group_id = i
            for j in range(50):
                food_id_in_group = j
                food_id = int(i) * 1000 + j
                stofc2015_food = STOFC2015Food(group_id,
                                               food_id_in_group,
                                               food_id,
                                               group_list, tag_list,
                                               food_amount)
                book.append(stofc2015_food, group_id, food_id_in_group)
                created_entries.append(stofc2015_food)

        # 確認
        i = 0
        for appended in book.generator():
            self.assertEqual(created_entries[i], appended)
            i += 1

    def test_get_food_by_total_id(self):
        book = STOFC2015FoodBook()
        group_list = ['group1', 'group2']
        tag_list = ['tag1', 'tag2', 'tag3']
        food_amount = '100g'

        # 全てのグループで適当な数のエントリを作成して登録する
        created_foods_by_total_id = dict()
        for i in FOOD_GROUPS.keys():
            group_id = i
            for j in range(50):
                food_id_in_group = j
                food_id = int(i) * 1000 + j
                stofc2015_food = STOFC2015Food(group_id,
                                               food_id_in_group,
                                               food_id,
                                               group_list, tag_list,
                                               food_amount)
                book.append(stofc2015_food, group_id, food_id_in_group)
                created_foods_by_total_id[food_id] = stofc2015_food

        # 確認
        for food_id in created_foods_by_total_id.keys():
            food = book.get_food_by_total_id(food_id)
            excepted = created_foods_by_total_id[food_id]
            self.assertEqual(food, excepted)


    def test_get_foods_by_group(self):
        book = STOFC2015FoodBook()
        group_list = ['group1', 'group2']
        tag_list = ['tag1', 'tag2', 'tag3']
        food_amount = '100g'

        # 全てのグループで適当な数のエントリを作成して登録する
        created_foods_by_group = dict()
        for i in FOOD_GROUPS.keys():
            group_id = i
            created_foods_by_group[i] = dict()
            for j in range(50):
                food_id_in_group = j
                food_id = int(i) * 1000 + j
                stofc2015_food = STOFC2015Food(group_id,
                                               food_id_in_group,
                                               food_id,
                                               group_list, tag_list,
                                               food_amount)
                book.append(stofc2015_food, group_id, food_id_in_group)
                created_foods_by_group[i][j] = stofc2015_food

        # 確認
        for i in FOOD_GROUPS.keys():
            group_entries = book.get_foods_by_group(i)
            for j in range(50):
                appended = group_entries[j]
                excepted = created_foods_by_group[i][j]
                self.assertEqual(appended, excepted)


if __name__ == '__main__':
    unittest.main()
