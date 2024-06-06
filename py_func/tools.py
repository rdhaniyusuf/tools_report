from datetime import datetime
import pytz
import time as tsleep

import win32com.client as win32

def format_id_time():
    dt =datetime.utcnow()
    id_tz = pytz.timezone("Asia/Jakarta")
    dt_id = dt.replace(tzinfo=pytz.utc).astimezone(id_tz)
    formated_date = dt_id.strftime("%d %B %Y")
    hour = dt_id.hour
    if 7<= hour <10:
        period_day = "Pagi"
    elif 10<= hour <16:
        period_day = "Siang"
    elif 15<= hour <24:
        period_day = "Sore"
    
    return [formated_date, period_day]