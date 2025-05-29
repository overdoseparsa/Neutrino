from datetime import datetime, timedelta

def is_time_difference_less(time1, time2, max_difference)->bool:

    if isinstance(time1, str):
        time1 = datetime.strptime(time1, '%Y-%m-%d %H:%M:%S')
    if isinstance(time2, str):
        time2 = datetime.strptime(time2, '%Y-%m-%d %H:%M:%S')
    difference = abs(time1 - time2)
    return difference < max_difference

