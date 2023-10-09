from datetime import date, datetime, time, timedelta


def get_date_slug(d: date | datetime, pattern="%Y%m%d") -> str:
    """
    Return a string representation of a date or datetime object.

    """
    return d.strftime(pattern)


def timedelta_to_minutes(td: timedelta) -> int:
    """
    Return a rounded conversion from minutes to seconds.
    """
    return td.seconds // 60


def substract_times(end: time, start: time) -> timedelta:
    """
    Workaround to allow a substraction between two time objects, assuming they occur the
    same day.
    """
    return datetime.combine(date.min, end) - datetime.combine(date.min, start)


def add_delta_to_time(td: timedelta, tim: time):
    """
    Workaround to allow adding a timedelta to time objects, assuming result is the same
    day.
    """
    return (datetime.combine(date.min, tim) + td).time()


def get_nb_months(start, end):
    """
    Return the number of months between two dates.
    """
    return (end.year - start.year) * 12 + (end.month - start.month)
