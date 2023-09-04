from time import sleep
from datetime import datetime, timedelta

import pytz
from dateutil.relativedelta import *

from conf.conf import Conf
from data.fake_data import faker
from pytz import timezone
from dateutil.parser import parse


def now():
    return datetime.now()


def get_nearest_work_day() -> str:
    """ Возвращает ближайший рабочий день относительно текущей даты.
    Не учитывает государственные праздники.
    """
    current_date = datetime.now()
    current_weekday = current_date.weekday()
    if current_weekday == 5:
        add_days = 2
    elif current_weekday == 6:
        add_days = 1
    else:
        add_days = 0
    current_date = current_date + timedelta(days=add_days)
    return current_date.strftime("%d.%m.%Y")


def get_next_work_day() -> str:
    """Возвращает следующий рабочий день за рабочим днем относительно текущей даты."""

    current_date = datetime.now()
    current_weekday = current_date.weekday()
    if current_weekday == 4:
        add_days = 3
    elif current_weekday == 5:
        add_days = 2
    else:
        add_days = 1
    current_date = current_date + timedelta(days=add_days)
    return current_date.strftime("%d.%m.%Y")


def diff_time_from_now(date, timeout=0.5):
    # type: (str, float) -> int
    # Считает разницу в секундах между переданной датой и текущим временем
    # Возвращает отрицательные и положительные значения в секундах
    sleep(timeout)
    now_time = now()
    return (now_time - parse(date)).seconds


def get_current_date(format_string="%d.%m.%Y"):
    # type: (str) -> str
    return now().strftime(format_string)


def get_next_date_after_required_date(date_string: str, format_string: str = "%d.%m.%Y") -> str:
    """Метод возвращает следующую дату после нужной (переданной) даты."""
    date = datetime.strptime(date_string, format_string)
    next_date = date + timedelta(days=1)
    return next_date.strftime(format_string)


def get_previous_date_before_required_date(date_string) -> str:
    """Метод возвращает предыдущую дату перед нужной (переданной) датой."""
    date = datetime.strptime(date_string, "%d.%m.%Y")
    next_date = date - timedelta(days=1)
    return next_date.strftime("%d.%m.%Y")


def get_diff_days(date1, date2):
    # type: (str, str) -> int
    """Возвращает разницу дней между датами"""
    days = datetime.strptime(date1, "%d.%m.%Y") - datetime.strptime(date2, "%d.%m.%Y")
    return days.days


def get_diff_days_without_start_day(date1, date2):
    # type: (str, str) -> int
    """Возвращает разницу дней между датами без учета дня начала отсчета"""
    days = datetime.strptime(date1, "%d.%m.%Y") - datetime.strptime(date2, "%d.%m.%Y")
    return days.days


def random_date(format_string="%d.%m.%Y"):
    return faker() \
        .date_time_between(start_date='-30d', end_date='+30d', tzinfo=timezone('Europe/Moscow')) \
        .strftime(format_string)


def get_random_date_greater_then_current(format_string="%Y-%m-%d"):
    return faker() \
        .date_time_between(start_date='+0d', end_date='+30d', tzinfo=timezone('Europe/Moscow')) \
        .strftime(format_string)


def get_date_period(start_date=1, end_date=30, format_string="%Y-%m-%d"):
    """
    Рассчитывает период времени относительо текущей даты
    :param start_date: {int} количество дней от текущей даты, в том числе и отрицательные значения
    :param end_date: {int} количество дней от текущей даты, в том числе и отрицательные значения
    :param format_string: {str} Тип форматирования объекта времени в строку
    :return: {tuple}
    """
    date = datetime.now(tz=timezone('Europe/Moscow'))
    start_date = date + relativedelta(days=+start_date)
    end_date = date + relativedelta(days=+end_date)
    return start_date.strftime(format_string), end_date.strftime(format_string)


def is_date_holiday(date: str, format_string='%Y-%m-%d'):
    holidays = Conf.configuration['holidays']
    is_holiday = any(x[0].strftime(format_string) == date for x in holidays)
    return is_holiday


def get_date_after_required_days_number_with_weekend(days_number: int = 29) -> str:
    """
    Возвращает дату после текущей с указанным смещением на кол-во дней,
    с учетом выпадания конечной даты на выходной день
    """
    current_day, end_date = get_date_period(start_date=0, end_date=days_number)
    while is_date_holiday(date=end_date):
        end_date = get_next_date_after_required_date(date_string=end_date, format_string="%Y-%m-%d")
    return end_date


def get_date_period_with_hh_mm(start_date=1, end_date=30):
    """
    Возвращает период времени относительно текущей даты в формате дд.мм.гггг чч:мм
    :param start_date: {int} количество дней от текущей даты, в том числе и отрицательные значения
    :param end_date: {int} количество дней от текущей даты, в том числе и отрицательные значения
    :return: {tuple}
    """
    return get_date_period(start_date=start_date, end_date=end_date, format_string="%d.%m.%Y %H:%M")


def get_current_time_with_timezone():
    """Метод возвращает текущую дату со временем"""
    tz = pytz.timezone('Europe/Moscow')
    return datetime.now(tz).isoformat(timespec='seconds')


def get_last_week_date(format_string="%Y-%m-%d"):
    # type: (str) -> str
    """Метод возвращает дату, которая была неделю назад."""
    date = datetime.strptime(get_current_date(format_string), format_string)
    next_date = date - timedelta(days=7)
    return next_date.strftime(format_string)


def is_datetime_between_dates_with_delta(date: str, minutes_delta: int):
    """Метод возвращает True если переданная дата/время находится в диапазоне"""
    date = parse(date, dayfirst=True).strftime('%d.%m.%y %H:%M')
    datetime_with_previous_minute = datetime.now() - timedelta(minutes=minutes_delta)
    datetime_with_next_minute = datetime.now() + timedelta(minutes=minutes_delta)
    return datetime_with_previous_minute <= datetime.strptime(date, '%d.%m.%y %H:%M') <= datetime_with_next_minute
