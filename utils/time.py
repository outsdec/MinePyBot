from datetime import datetime, timedelta, timezone
import pytz

def get_end_of_week():
    now = datetime.now(pytz.timezone("Asia/Almaty"))
    end_of_week = now + timedelta(days=(6 - now.weekday()))  # 6 - текущий день недели, чтобы получить конец недели
    end_of_week = end_of_week.replace(hour=23, minute=59, second=59)  # Установка времени в конец дня
    return end_of_week