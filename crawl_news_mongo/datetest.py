import pytz
from datetime import datetime
#
# print(pytz.timezone('Europe/Berlin'))
# date_in_iso_format_1 = datetime(2019,11,23,11,21,30,tzinfo=pytz.timezone('Asia/Phnom_Penh'))
# date_in_iso_format_2 = datetime(2019,11,23,11,21,30,tzinfo=pytz.timezone('Asia/Ho_Chi_Minh'))
# date_in_iso_format_3 = datetime(2019,11,23,11,21,30,tzinfo=pytz.timezone('Asia/Saigon'))
#
# print(date_in_iso_format_1)
# print(date_in_iso_format_2)
# print(date_in_iso_format_3)


# for tz in pytz.all_timezones:
#     print(tz)


from datetime import datetime
# now = datetime.now() # current date and time
# print(now)
test = "July 15, 2019"
previous = datetime.strptime(test,"%B %d, %Y")
now = previous.replace(tzinfo=pytz.timezone('Asia/Phnom_Penh'))
date_in_iso_format = datetime(2018, 11, 14,tzinfo=pytz.timezone('Asia/Phnom_Penh'))

print(type(now))
print(now)
print(type(date_in_iso_format))
print(date_in_iso_format)
year = now.strftime("%Y")
print("year:", year)
month = now.strftime("%m")
print("month:", month)
day = now.strftime("%d")
print("day:", day)
time = now.strftime("%H:%M:%S")
print("time:", time)
timezone = now.strftime("%z")
print("timezone", timezone)
date_time = now.strftime("%m/%d/%Y, %H:%M:%S")
print("date and time:",date_time)