import datetime
import calendar


class DateTimeHelper:
    @staticmethod
    def get_date_from_str(strdate):
        # 以下の区切り文字を認める
        if '-' in strdate:
            return datetime.datetime.strptime(strdate, '%Y-%m-%d').date()
        elif '/' in strdate:
            return datetime.datetime.strptime(strdate, '%Y/%m/%d').date()
        elif len(strdate) == 8:  # '20170913' といった形式を予想
            return datetime.datetime.strptime(strdate, '%Y%m%d').date()
        else:
            raise ValueError('認められない日付のフォーマット: {}'.format(strdate))

    @classmethod
    def get_date(cls, dt):
        # datetime は date の子クラスであるのでこの順でないといけない
        if isinstance(dt, datetime.datetime):
            return dt.date()
        elif isinstance(dt, datetime.date):
            return dt
        elif isinstance(dt, str):
            return cls.get_date_from_str(dt)
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
