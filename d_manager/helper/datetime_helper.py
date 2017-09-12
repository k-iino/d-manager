import datetime
import calendar


class DateTimeHelper:
    # 全て0埋めした10進数
    DATE_FORMAT = '%Y-%m-%d'
    TIME_FORMAT = '%H:%M:%S'
    DATETIME_FORMAT = '{} {}'.format(DATE_FORMAT, TIME_FORMAT)

    @staticmethod
    def get_date(dt):
        # datetime は date の子クラスであるのでこの順でないといけない
        if isinstance(dt, datetime.datetime):
            return dt.date()
        elif isinstance(dt, datetime.date):
            return dt
        else:
            raise ValueError

    @classmethod
    def get_weekday(cls, dt):
        date = cls.get_date(dt)
        return calendar.weekday(date.year, date.month, date.day)

    @classmethod
    def get_day_before(cls, base_date, n):
        return cls.get_date(base_date) + datetime.timedelta(days=-n)

    @classmethod
    def get_yesterday(cls, dt):
        """前日の date を返す"""
        return cls.get_day_before(dt, 1)

    @classmethod
    def get_last_week(cls, dt):
        """指定した日付から一週間前までの date のリストを返す"""
        date = cls.get_date(dt)
        last_week = list()
        for n in range(1, 8):
            last_week.append(cls.get_day_before(date, n))
        else:
            return last_week
