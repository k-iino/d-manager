import datetime
import yaml

from d_manager.book.product_food_book import ProductFoodBook
from d_manager.book.stofc2015_food_book import STOFC2015FoodBook
from d_manager.helper.prompt_helper import PromptHelper
from d_manager.helper.datetime_helper import DateTimeHelper
from d_manager.meal import MealItem
from d_manager.meal import Meal


class InteractiveMealBookLoader:
    """対話的に市販食品を読み込む"""
    def __init__(self, food_books):
        self.food_books = dict()
        for food_book in food_books:
            if isinstance(food_book, ProductFoodBook):
                self.food_books['市販の食品群（product_food）'] = food_book
            elif isinstance(food_book, STOFC2015FoodBook):
                self.food_books['日本食品標準成分表2015（stofc2015）'] = food_book
            else:
                raise ValueError

    def get_meal_item(self):
        # 返す食品項目
        meal_items = list()

        while True:
            # 食品データベースの選択
            PromptHelper.print_msg('食品はどのデータベースのもの？')
            _, name = PromptHelper.choose_from_list(self.food_books)
            food_book = self.food_books[name]

            # 食品情報を ID から選択
            PromptHelper.print_msg('食品の ID を入力してください')
            while True:
                food_id = PromptHelper.get_integer()
                try:
                    if isinstance(food_book, ProductFoodBook):
                        food = food_book.get_food_by_total_id(food_id)
                    elif isinstance(food_book, STOFC2015FoodBook):
                        food = food_book.get_food_by_total_id(food_id)

                    break
                except (ValueError, KeyError):
                    PromptHelper.print_msg('不正な ID です。')

            PromptHelper.print_msg('食品名: {}'.format(food.name))
            PromptHelper.print_msg('摂取した食品の食品単位に対する比率を記入してください。食品単位={}'.format(food.amount))
            scale = PromptHelper.get_float()

            # 確認
            PromptHelper.print_msg('この食品でよろしいですか？')
            PromptHelper.print_msg(yaml.dump(food.to_dict(), allow_unicode=True))
            PromptHelper.print_msg('scale: {}'.format(scale))
            if PromptHelper.confirm_yes_of_no():
                meal_items.append(MealItem(food, scale))
            else:
                PromptHelper.print_msg('登録がキャンセルされました。')

            PromptHelper.print_msg('引き続き登録しますか？')
            if not PromptHelper.confirm_yes_of_no():
                break

        return meal_items

    def load(self, meal_book):
        # いつの食事記録か
        now = datetime.datetime.now()
        today_str = '今日（{}）'.format(now.date())
        # 今日を除く過去一週間
        last_week = DateTimeHelper.get_last_week(now)
        other = 'その他'
        PromptHelper.print_msg('いつの食事ですか？')
        _, date = PromptHelper.choose_from_list([today_str] + last_week + [other])
        # オブジェクトに date と datetime がまじっているが、Meal 側で datetime オブジェクトに統一している
        if date == today_str:
            date = now
        elif date == other:
            PromptHelper.print_msg('いつの食事か、日付を文字列で入力してください？')
            PromptHelper.print_msg("認められる文字列の形式。'2017-09-13', '2017/09/13', '20170913', '2017/9/13'")
            while True:
                str_date = PromptHelper.get_str()
                try:
                    date = DateTimeHelper.get_date_from_str(str_date)
                    break
                except ValueError:
                    PromptHelper.print_msg('不正な日付の形式です。{}'.format(str_date))

        meal_items = self.get_meal_item()
        PromptHelper.print_msg('この食事にメモがあれば')
        meal = Meal(meal_items, _datetime=date, memo='')

        PromptHelper.print_msg('次の食事を登録します。よろしいですか？')
        PromptHelper.print_msg('日付: {}'.format(date))
        for item in meal_items:
            PromptHelper.print_msg('name: {}, scale: {}'.format(item.food.name, item.scale))
        if PromptHelper.confirm_yes_of_no():
            meal_book.append(meal)
        else:
            PromptHelper.print_msg('登録がキャンセルされました。')
