import datetime
import calendar

# 読み取り可能な日付、時刻のフォーマット
DATE_FORMATS = ('%Y-%m-%d',  # 西暦 ( 4桁) の 10 進表記
                '%Y/%m/%d',
                '%Y%m%d',
                '%y-%m-%d',  # 0埋めした10進数で表記した世紀ありの年
                '%y/%m/%d',
                '%y%m%d',
                )
TIME_FORMATS = ('%H:%M',
                '%H:%M:%S',
                '%H%M',
                '%H%M%S',
                )


class DateTimeHelper:
    @staticmethod
    def get_datetime_from_str(date_string):
        date_string = date_string.strip()
        dt = None
        for whole_fmt in ('{}{}', '{} {}'):
            for date_fmt in DATE_FORMATS:
                for time_fmt in TIME_FORMATS:
                    fmt = whole_fmt.format(date_fmt, time_fmt)
                    try:
                        dt = datetime.datetime.strptime(date_string, fmt)
                    except ValueError:
                        continue
        if dt is None:
            raise ValueError('認められない日付のフォーマット: {}'.format(date_string))
        else:
            return dt

    @classmethod
    def get_datetime(cls, t):
        # datetime は date の子クラスであるのでこの順でないといけない
        if isinstance(t, datetime.datetime):
            return t
        elif isinstance(t, datetime.date):
            # 時刻は 00:00:00 だと見做す
            return datetime.datetime(year=t.year,
                                     month=t.month,
                                     day=t.day)
        elif isinstance(t, datetime.time):
            # 日付は本日だと見做す
            _dt = datetime.datetime.today()
            return datetime.datetime(year=_dt.year,
                                     month=_dt.month,
                                     day=_dt.day,
                                     hour=t.hour,
                                     minute=t.minute,
                                     second=t.second,
                                     microsecond=t.microsecond)
        elif isinstance(t, str):
            return cls.get_datetime_from_str(t)
        else:
            raise ValueError

    @classmethod
    def get_weekday(cls, t):
        """曜日を表す数字を取得、月曜が0"""
        date = cls.get_datetime(t).date()
        return calendar.weekday(date.year, date.month, date.day)

    @classmethod
    def get_datetime_before(cls, base_date, n):
        return cls.get_datetime(base_date) + datetime.timedelta(days=-n)

    @classmethod
    def get_yesterday(cls, dt):
        """前日の datetime を返す"""
        return cls.get_datetime_before(dt, 1)

    @classmethod
    def get_last_week(cls, dt):
        """指定した日付から一週間前までの datetime のリストを返す"""
        dt = cls.get_datetime(dt)
        last_week = list()
        for n in range(1, 8):
            last_week.append(cls.get_datetime_before(dt, n))
        else:
            return last_week
