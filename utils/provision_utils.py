from datetime import datetime, timedelta
import logging

def gs(n, s): return f"{n}{s} " if n else ""

def calculate_times_per_day(times_per_day, offset_hours):
    now = datetime.now()
    time_interval = timedelta(hours=24 / times_per_day)
    resulting_times = []
    current_time = datetime(now.year, now.month, now.day, offset_hours)
    for _ in range(int(times_per_day)):
        resulting_times.append(current_time.strftime("%H:%M"))
        current_time += time_interval
    return resulting_times

def print_debug_setup_times(upload_time_offset, upload_frequency):
    date = datetime.now()  
    for x in range(24):
        date=  date.replace(hour=x)
        date=  date.replace(minute=0)
        rup = round_time(date, upload_frequency*60, mode="up", offset_minutes=( upload_time_offset)*60)
        print(date.strftime("%d-%m-%Y %H:%M"))
        print(rup.strftime("%d-%m-%Y %H:%M")) 
        print(rup-date if rup>date else date-rup, "\n")

def round_time(dt, round_minutes, mode='nearest', offset_minutes=0):
    round_seconds = round_minutes * 60
    timestamp = (dt - datetime(1970, 1, 1)).total_seconds()
    remainder =( timestamp % round_seconds) + offset_minutes*60
    if mode == 'nearest':
        adjustment = round_seconds - remainder if remainder > round_seconds / 2 else -remainder
    elif mode == 'up':
        adjustment = round_seconds - remainder if remainder > 0 else 0
    elif mode == 'down':
        adjustment = -remainder if remainder > 0 else 0
    else:
        raise ValueError("Invalid mode. Mode must be one of 'nearest', 'up', or 'down'.")
    rounded_dt = dt + timedelta(seconds=adjustment)
    return rounded_dt

def print_time_setup(uploads_per_day, upload_time_offset, upload_frequency, minimum_upload_frequency_h):
    logging.info("")
    logging.info(f"Uploads per day: {uploads_per_day} | upload_frequency: {upload_frequency}h | upload_time_offset: {upload_time_offset}h | minimum_upload_frequency_h: {minimum_upload_frequency_h}h")
    logging.info(calculate_times_per_day(uploads_per_day, upload_time_offset))

def break_down_delta(delta):
    years = delta.days // 365
    months = (delta.days % 365) // 30
    days = delta.days % 365 % 30
    hours = delta.seconds // 3600
    minutes = (delta.seconds % 3600) // 60
    string = f'{gs(years, "y")}{gs(months, "mo")}{gs(days, "d")}{gs(hours, "h")}{gs(minutes, "m")}'
    return years,months,days,hours,minutes, string


def break_down_time_settings(database):
    upload_frequency_hours = database["settings"][0]["minimum_upload_frequency_h"]
    uploads_per_day = database["settings"][0]
    ["uploads_per_day"]
    upload_time_offset = database["settings"][0]["upload_time_offset"] +0
    upload_frequency = (24/uploads_per_day) 
    minimum_upload_frequency_h = upload_frequency / 2
    return uploads_per_day,upload_time_offset,upload_frequency,minimum_upload_frequency_h