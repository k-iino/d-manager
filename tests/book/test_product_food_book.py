import random
import unittest

from d_manager.food import BaseFood
from d_manager.food.product_food import ProductFood
from d_manager.book.product_food_book import ProductFoodBook


class ProductFoodBookTest(unittest.TestCase):
    def test_init(self):
        book = ProductFoodBook()

        # Good
        product_food = ProductFood(maker_name='maker',
                                   product_name='product',
                                   food_name='food',
                                   amount='100g')
        product_food.set_nutrients_list(['1kcal', '1g', '2g', '3g', '4g'])
        group_number = 1
        book.append(product_food, group_number)

        # Bad
        invalid_entry = BaseFood('some food', '100g')
        with self.assertRaises(ValueError):
            book.append(invalid_entry, group_number)

        invalid_group_number = 'foo'
        with self.assertRaises(ValueError):
            book.append(product_food, invalid_group_number)

    def test_id_in_group(self):
        """食品のグループ内での採番が正しくされているかを確認"""
        book = ProductFoodBook()
        group_number = 1
        excepted_ids = list()

        # Good
        food_one = ProductFood(maker_name='maker',
                               product_name='product',
                               food_name='one',
                               amount='100g')
        food_one.set_nutrients_list(['1kcal', '1g', '2g', '3g', '4g'])
        id1 = book.append(food_one, group_number)
        self.assertEqual(id1, 1001)
        excepted_ids.append(id1)

        food_two = ProductFood(maker_name='maker',
                               product_name='product',
                               food_name='twi',
                               amount='100g')
        food_two.set_nutrients_list(['1kcal', '1g', '2g', '3g', '4g'])
        id2 = book.append(food_two, group_number)
        self.assertEqual(id2, 1002)
        excepted_ids.append(id2)

        for id_in_group in book.get_foods_by_group(group_number).keys():
            # グループ内での採番の規則の実装が変わったら意味がなくなる
            total_id = ProductFood.get_total_id(group_number, id_in_group)
            if total_id not in excepted_ids:
                self.fail()

    def test_delete(self):
        """削除のテスト"""
        book = ProductFoodBook()
        group_number = 1
        num_of_checking = 10
        appended_entries = dict()

        # Book に食品データを入れる
        for i in range(num_of_checking):
            _f = ProductFood(maker_name='some maker',
                             product_name='product {}'.format(i),
                             food_name='delicious food',
                             amount='100g')
            _f.set_nutrients_list(['1kcal', '1g', '2g', '3g', '4g'])
            _total_id = book.append(_f, group_number)
            appended_entries[_total_id] = _f

        # 無作為に削除していく
        random.seed()
        for _ in range(num_of_checking):
            # 作成したリストから無作為に選択して削除する
            _target_total_id = random.choice(list(appended_entries.keys()))
            deleted = book.delete(_target_total_id)
            # 指定の ID として追加したものと、削除されたものが同じインスタンスか
            self.assertIs(deleted, appended_entries[_target_total_id])
            self.assertEqual(deleted.product_name, appended_entries[_target_total_id].product_name)
            # 削除したものは作成済みの辞書からも削除しておく
            del appended_entries[_target_total_id]

        # 全て削除したのでグループには何も含まれていないはず
        self.assertEqual(0, len(list(book.get_foods_by_group(group_number).keys())))

    def test_update(self):
        """更新のテスト"""
        book = ProductFoodBook()
        group_number = 1
        num_of_checking = 10
        appended_entries = dict()

        # Book に食品データを入れる
        for i in range(num_of_checking):
            _new = ProductFood(maker_name='some maker',
                               product_name='product {}'.format(i),
                               food_name='delicious food',
                               amount='100g')
            _new.set_nutrients_list(['1kcal', '1g', '2g', '3g', '4g'])
            _total_id = book.append(_new, group_number)
            appended_entries[_total_id] = _new

        # 無作為に更新していく
        random.seed()
        # 更新した食品の商品名に付ける接頭辞
        new_product_name_prefix = 'updated_'
        for _ in range(num_of_checking):
            # 作成したリストから無作為に選択して更新する
            _target_total_id = random.choice(list(appended_entries.keys()))
            # 更新用データ
            _old = appended_entries[_target_total_id]
            _new = ProductFood(maker_name='some maker',
                               product_name='{}{}'.format(new_product_name_prefix, _old.product_name),
                               food_name='delicious food',
                               amount='100g')
            _new.set_nutrients_list(['1kcal', '1g', '2g', '3g', '4g'])

            _updated = book.update(_target_total_id, _new)
            # 指定の ID として追加したものと、削除されたものが同じインスタンスか
            self.assertIs(_old, _updated)
            # 更新したものは作成済みの辞書からも削除しておく
            del appended_entries[_target_total_id]

        # 更新された各エントリの名前を確認
        for _food in book.get_foods_by_group(group_number).values():
            self.assertTrue(_food.product_name.startswith(new_product_name_prefix))


if __name__ == '__main__':
    unittest.main()
