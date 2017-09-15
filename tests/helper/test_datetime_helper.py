import unittest
import datetime

from d_manager.helper.datetime_helper import DateTimeHelper


class MyTestCase(unittest.TestCase):

    @staticmethod
    def __compare_datetime(dt1, dt2):
        pass


    def test_get_date_from_str(self):
        """文字列から日付を取得する"""
        year_strs = ('17', '2017')
        month_strs = ('1', '01', '12')
        day_strs = ('1', '01', '29')
        hour_strs = ('1', '01', '23')
        minute_strs = ('1', '01', '59')
        second_strs = ('1', '01', '59')

        date_seps = ('', '-', '/')
        time_seps = ('', ':')

        fmts = ('{}{}', '{} {}')

        date_strs = ('{}{}{}{}{}'.format(y, sep, m, sep, d)
                     for y in year_strs
                     for m in month_strs
                     for d in day_strs
                     for sep in date_seps
                     )

        day_strs = ('{}{}{}{}{}'.format(h, sep, m, sep, s)
                    for h in hour_strs
                    for m in minute_strs
                    for s in second_strs
                    for sep in time_seps
                    )

        datetime_strs = (fmt.format(date, day)
                         for date in date_strs
                         for day in day_strs
                         for fmt in fmts)

        for datetime_str in datetime_strs:
            dt = DateTimeHelper.get_datetime_from_str(datetime_str)
            self.assertIsInstance(dt, datetime.datetime)

    def test_get_datetime(self):
        """種々の形式のオブジェクトから時間を取得できるか"""
        # datetime はそのまま
        today_dt = datetime.datetime.today()
        self.assertEqual(today_dt, DateTimeHelper.get_datetime(today_dt))
        # date は同日の時刻 00:00:00 だと見做す
        today_dt = datetime.datetime.today().date()
        got_dt = DateTimeHelper.get_datetime(today_dt)
        excepted_dt = datetime.datetime(today_dt.year, today_dt.month, today_dt.day,
                                        hour=0, minute=0, second=0, microsecond=0)
        self.assertTrue(excepted_dt == got_dt)
        # time は本日の同時刻だと見做す
        today_t = datetime.datetime.today().time()
        got_dt = DateTimeHelper.get_datetime(today_t)
        excepted_dt = datetime.datetime(today_dt.year, today_dt.month, today_dt.day,
                                        today_t.hour, today_t.minute, today_t.second,
                                        today_t.microsecond)
        self.assertTrue(excepted_dt == got_dt)
        # 文字列の場合は test_get_date_from_str でテストしているので簡易的に実施
        y = 2017
        m = 9
        d = 15
        h = 22
        mi = 38
        s = '{}/{}/{} {}:{}'.format(y, m, d, h, mi)
        excepted_dt = datetime.datetime(y, m, d, h, mi)
        self.assertEqual(excepted_dt, DateTimeHelper.get_datetime(s))

    def test_get_weekday(self):
        """曜日に対応する番号を取得できるか"""
        day = datetime.date(2017, 9, 1)  # 金曜日
        weekday = 4  # 金曜日は 4
        self.assertEqual(weekday, DateTimeHelper.get_weekday(day))

    def test_get_datetime_before(self):
        """基準日から指定した日付が取得できるか"""
        base_date = datetime.date(2017, 9, 3)
        yesterday = datetime.date(2017, 9, 2)
        day_before_yesterday = datetime.date(2017, 9, 1)
        # 日付だけ確認
        self.assertEqual(yesterday,
                         DateTimeHelper.get_datetime_before(base_date, 1).date())
        self.assertEqual(day_before_yesterday,
                         DateTimeHelper.get_datetime_before(base_date, 2).date())

    def test_get_yesterday(self):
        """基準日の昨日の日付が取得できるか"""
        base_date = datetime.date(2017, 9, 3)
        yesterday = datetime.date(2017, 9, 2)
        # 日付だけ確認
        self.assertEqual(yesterday,
                         DateTimeHelper.get_yesterday(base_date).date())

    def test_get_last_week(self):
        """基準日から一週間まえまでの日付のリストが取得できるか"""
        base_date = datetime.date(2017, 9, 3)
        last_week = DateTimeHelper.get_last_week(base_date)
        for i in range(7):
            # 日付だけ確認
            self.assertEqual(base_date - datetime.timedelta(days=i+1),
                             last_week[i].date())

if __name__ == '__main__':
    unittest.main()
