import os
import argparse
import datetime

# 許容する時刻の文字列形式
DATETIME_FORMAT = ('{}{}', '{} {}')
DATE_FORMATS = ('%Y%m%d', '%Y-%m-%d', '%Y/%m/%d')
TIME_FORMATS = ('', '%H%M', '%H:%M',
                '%H%M%S', '%H:%M:%S')

# 食事記録のパス
# ファイルとディレクトリに含まれる時刻の組み合わせを変更する場合、注意
# get_date_from_meal_file はディレクトリ名に月の表記が含まれていることを前提に実装している
MEAL_DIR_FORMAT = '%Y-%m'
MEAL_FILE_FORMAT = '%d_%H%M%S.json'

# 要約のパス
SUMMARY_DIR_FORMAT = '%Y'
SUMMARY_FILE_FORMAT = '%m-%d.json'


def get_meal_file_path(dt, base_dir=''):
    """
    時刻から食事記録の相対ファイルパスを得る

    :param dt:
    :param base_dir:
    :return: ディレクトリ名とファイル名のタプル
    """
    _dir = os.path.join(base_dir, dt.strftime(MEAL_DIR_FORMAT))
    _file = dt.strftime(MEAL_FILE_FORMAT)
    return _dir, _file


def get_date_from_meal_file(_dir, _f):
    """食事記録のファイルパスから時刻情報を得る"""
    year_month_dt = datetime.datetime.strptime(os.path.basename(_dir), MEAL_DIR_FORMAT)
    others_dt = datetime.datetime.strptime(_f, MEAL_FILE_FORMAT)
    return datetime.datetime(year=year_month_dt.year,
                             month=year_month_dt.month,
                             day=others_dt.day,
                             hour=others_dt.hour,
                             minute=others_dt.minute,
                             second=others_dt.second)


def get_summary_file_path(dt, base_dir=''):
    """
    時刻から要約ファイルの相対ファイルパスを得る

    :param dt:
    :param base_dir:
    :return: ディレクトリ名とファイル名のタプル
    """
    _dir = os.path.join(base_dir, dt.strftime(SUMMARY_DIR_FORMAT))
    _file = dt.strftime(SUMMARY_FILE_FORMAT)
    return _dir, _file


def get_date(date_str):
    """文字列から時刻を取得"""
    date_str = date_str.lower()
    if date_str == 'now':
        dt = datetime.datetime.now()
    elif date_str == 'today':
        # now や詳細指定との差別化のため、日付のみの指定は時間は0時0分0秒とする。
        _dt = datetime.datetime.today()
        dt = datetime.datetime(year=_dt.year, month=_dt.month, day=_dt.day)
    elif date_str == 'yesterday':
        _dt = datetime.datetime.today() - datetime.timedelta(days=1)
        dt = datetime.datetime(year=_dt.year, month=_dt.month, day=_dt.day)
    elif date_str == 'tomorrow':
        _dt = datetime.datetime.today() + datetime.timedelta(days=1)
        dt = datetime.datetime(year=_dt.year, month=_dt.month, day=_dt.day)
    else:
        dt = None
        fmts = (fmt.format(date, time) for fmt in DATETIME_FORMAT
                for time in TIME_FORMATS
                for date in DATE_FORMATS)
        for fmt in fmts:
            try:
                dt = datetime.datetime.strptime(date_str, fmt)
                break
            except ValueError:
                continue
        if dt is None:
            msg = '{} は適切な日付の文字列ではありません。'.format(date_str)
            raise ValueError(msg)

    return dt
