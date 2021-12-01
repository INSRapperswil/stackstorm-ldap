from datetime import timedelta, datetime
import pytz

__all__ = [
    'to_dict',
    'tuple_list_to_list_of_dicts',
    'absolute_adinterval_to_datetime',
    'relative_adinterval_to_timedelta',
    'datetime_to_absolute_adinterval',
    'timedelta_to_relative_adinterval',
    'datetime_to_string',
    'string_to_datetime'
]


def datetime_to_string(date_time):
    if date_time:
        return date_time.strftime('%Y-%m-%d %H:%M:%S%Z')
    else:
        return None


def string_to_datetime(string):
    if string:
        return datetime.strptime(string, '%Y-%m-%d %H:%M:%S%Z')
    else:
        return None


def to_dict(obj):
    if isinstance(obj, set):
        return list(obj)
    return obj.__dict__


def tuple_list_to_list_of_dicts(userlist):
    user_obj_list = []
    for user_tuple in userlist:
        user_obj = user_tuple[1]
        for key, value in user_obj.items():
            user_obj[key] = bytes(value[0]).decode("utf-8")
        user_obj_list.append(user_obj)
    return user_obj_list


def timedelta_to_relative_adinterval(delta):
    return int(delta.total_seconds() * 10000000)


def datetime_to_absolute_adinterval(date_time):
    adinterval = int(0x7FFFFFFFFFFFFFFF)
    if date_time:
        ad_epoch = datetime(1601, 1, 1, tzinfo=pytz.utc)
        adinterval = timedelta_to_relative_adinterval(date_time - ad_epoch)

    return adinterval


def relative_adinterval_to_timedelta(adinterval):
    """
    Converts Relative AD Interval (https://msdn.microsoft.com/en-us/library/ms684426(v=vs.85).aspx)
    to positive Python timedelta.
    Returns None if the interval represents 'never'.
    :param adinterval: string of negative long int representing 100-nanosecond intervals
    """
    relative_never = [0, -0x8000000000000000]
    adinterval_int = int(adinterval)
    if adinterval_int in relative_never:
        return None
    seconds = abs(adinterval_int / 10000000)
    return timedelta(seconds=seconds)


def absolute_adinterval_to_datetime(adinterval):
    """
    Converts Absolute AD Interval (https://msdn.microsoft.com/en-us/library/ms684426(v=vs.85).aspx)
    to Python datetime in UTC.
    Returns None if the interval represents 'never'.
    :param adinterval: string of long int representing 100-nanosecond intervals since Jan 1, 1601 UTC
    """
    absolute_never = [0, 0x7FFFFFFFFFFFFFFF]
    if int(adinterval) in absolute_never:
        return None
    delta = relative_adinterval_to_timedelta(adinterval)
    ad_epoch = datetime(1601, 1, 1, tzinfo=pytz.utc)
    return ad_epoch + delta
