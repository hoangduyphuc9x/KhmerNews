import pytz
from datetime import datetime

print(pytz.timezone('Europe/Berlin'))
date_in_iso_format = datetime(2019,11,23,11,21,30,tzinfo=pytz.timezone('Asia/Phnom_Penh'))
print(date_in_iso_format)

# for tz in pytz.all_timezones:
#     print(tz)
