import random
import unittest

from d_manager.food.product_food import ProductFood
from d_manager.book.product_food_book import GROUPS
from d_manager.book.product_food_book import ProductFoodBook
from d_manager.nutrient.basics import Energy, Protein, Lipid, Carbohydrate, SaltEquivalent


class ProductFoodBookTest(unittest.TestCase):

    nutrient_classes = (Energy,
                        Protein,
                        Lipid,
                        Carbohydrate,
                        SaltEquivalent)

    @classmethod
    def __get_randome_amount_nutrients(cls):
        random.seed()
        nutrients = list()
        for nut_cls in cls.nutrient_classes:
            value = random.random() * 500
            nutrients.append(nut_cls(value))
        else:
            return nutrients

    def test_append_and_get(self):
        """食品が正しく登録出来るか"""
        # 確認用に食品を保存しておく辞書
        created_foods = dict()
        # 一つのグループに登録する食品の数
        num_of_foods = 50

        book = ProductFoodBook()

        # append のテスト
        # 全てのグループに指定の数だけ食品を作成し登録する。
        for group_id in GROUPS:
            for i in range(1, num_of_foods + 1):
                maker = '製造者 {}'.format(group_id, i)
                product = '商品名・product name {} {}'.format(group_id, i)
                food_name = '名称/food name {} {}'.format(group_id, i)
                food = ProductFood(maker, product, food_name, '100g')
                food.nutrients = self.__get_randome_amount_nutrients()

                # 市販の食品の場合は登録するまでグループ内の ID が確定せず、
                # 登録時に統合 ID （グループ ID とグループ内の ID から一意に決まる ID）が返ってくる
                # 作成時に予測した統合 ID と一致するかも確認する。
                excepted_total_id = group_id * 1000 + i
                total_id = book.append(group_id, food)
                self.assertEqual(excepted_total_id, total_id)

                created_foods[total_id] = food

        # get_by_total_id のテスト
        for total_id in created_foods.keys():
            excpted = created_foods[total_id]
            actual = book.get_by_total_id(total_id)
            self.assertEqual(excpted, actual)

        # view のテスト用
        import pickle
        with open('../bin/pickle/test_product_food_book.pickle', mode='wb') as f:
            pickle.dump(book, f)

    def test_update(self):
        """登録したエントリの更新についてのテスト"""
        # 確認用に食品を保存しておく辞書
        created_foods = dict()
        # 一つのグループに登録する食品の数
        num_of_foods = 50
        # 一つのグループごとに更新する食品の数
        num_of_update = 20

        book = ProductFoodBook()

        # append
        # 全てのグループに指定の数だけ食品を作成し登録する。
        for group_id in GROUPS:
            for i in range(1, num_of_foods + 1):
                maker = 'maker'
                product = 'product {}'.format(i)
                food_name = 'food name {}'.format(i)
                food = ProductFood(maker, product, food_name, '100g')
                food.nutrients = self.__get_randome_amount_nutrients()
                # 登録
                total_id = book.append(group_id, food)
                created_foods[total_id] = food

        # update
        # ランダムに更新して、更新出来たかを確認
        for group_id in GROUPS:
            # 一度選んだ ID は選ばない
            updated_total_id = list()
            while len(updated_total_id) <= num_of_update:
                # 総合 ID をランダムで生成して、そのエントリをアップデートして確認する
                total_id = group_id * 1000 + random.randrange(1, num_of_foods + 1)
                if total_id in updated_total_id:
                    continue

                # 更新する新しい食品
                maker = 'updated maker {}'.format(i)
                product = 'updated {}'.format(i)
                food_name = 'updated food {}'.format(i)
                new_food = ProductFood(maker, product, food_name, '100g')
                new_food.nutrients = self.__get_randome_amount_nutrients()
                # 更新
                old = book.update(total_id, new_food)
                # 返ってきたものが古いものと一致するか確認する
                excepted = created_foods[total_id]
                self.assertEqual(excepted, old)
                # self.assertEqual(old.name, excepted.name)
                # self.assertEqual(old.product_name, excepted.product_name)
                # self.assertEqual(old.energy, excepted.energy)
                # self.assertEqual(old.protein, excepted.protein)
                # 以後、Book から取得出来るものは更新した食品か確認する
                self.assertEqual(book.get_by_total_id(total_id), new_food)
                # 更新した id は記録しておく
                updated_total_id.append(total_id)

    def test_delete(self):
        """登録したエントリの削除についてのテスト"""
        # 確認用に食品を保存しておく辞書
        created_foods = dict()
        # 一つのグループに登録する食品の数
        num_of_foods = 50
        # 一つのグループごとに削除する食品の数
        num_of_delete = 20

        book = ProductFoodBook()

        # append
        # 全てのグループに指定の数だけ食品を作成し登録する。
        for group_id in GROUPS:
            for i in range(1, num_of_foods + 1):
                maker = 'maker'
                product = 'product {}'.format(i)
                food_name = 'food name {}'.format(i)
                food = ProductFood(maker, product, food_name, '100g')
                food.nutrients = self.__get_randome_amount_nutrients()
                total_id = book.append(group_id, food)
                created_foods[total_id] = food

        # delete
        # ランダムに削除して、削除出来たかを確認
        for group_id in GROUPS:
            # 一度選んだ ID は選ばない
            delete_total_id = list()
            while len(delete_total_id) <= num_of_delete:
                # 総合 ID をランダムで生成して、そのエントリをアップデートして確認する
                total_id = group_id * 1000 + random.randrange(1, num_of_foods + 1)
                if total_id in delete_total_id:
                    continue

                # 削除
                old = book.delete(total_id)
                # 返ってきたものが古いものと一致するか確認する
                excepted = created_foods[total_id]
                self.assertEqual(excepted, old)
                # self.assertEqual(old.name, excepted.name)
                # self.assertEqual(old.product_name, excepted.product_name)
                # self.assertEqual(old.energy, excepted.energy)
                # self.assertEqual(old.protein, excepted.protein)
                # 以後､取得出来ないことを確認する
                with self.assertRaises(KeyError):
                    book.get_by_total_id(total_id)
                # 更新した id は記録しておく
                delete_total_id.append(total_id)


if __name__ == '__main__':
    unittest.main()
