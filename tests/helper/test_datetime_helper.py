import unittest
import datetime

from d_manager.helper.datetime_helper import DateTimeHelper


class MyTestCase(unittest.TestCase):
    def test_get_date(self):
        today = datetime.date.today()
        self.assertEqual(today, DateTimeHelper.get_date(datetime.date.today()))
        self.assertEqual(today, DateTimeHelper.get_date(datetime.datetime.now()))

    def test_get_weekday(self):
        day = datetime.date(2017, 9, 1)  # 金曜日
        weekday = 4  # 金曜日は 4
        self.assertEqual(weekday, DateTimeHelper.get_weekday(day))

    def test_get_day_before(self):
        base_date = datetime.date(2017, 9, 3)
        yesterday = datetime.date(2017, 9, 2)
        day_before_yesterday = datetime.date(2017, 9, 1)
        self.assertEqual(yesterday, DateTimeHelper.get_day_before(base_date, 1))
        self.assertEqual(day_before_yesterday, DateTimeHelper.get_day_before(base_date, 2))

    def test_get_yesterday(self):
        base_date = datetime.date(2017, 9, 3)
        yesterday = datetime.date(2017, 9, 2)
        self.assertEqual(yesterday, DateTimeHelper.get_yesterday(base_date))

    def test_get_last_week(self):
        base_date = datetime.date(2017, 9, 3)
        last_week = DateTimeHelper.get_last_week(base_date)
        for i in range(7):
            self.assertEqual(base_date - datetime.timedelta(days=i+1),
                             last_week[i])

if __name__ == '__main__':
    unittest.main()
