from datetime import datetime

# currentDate = "Apr 21, 2019"

# datetimeObject = datetime.strptime(currentDate,'%b %d, %Y')

# # print(datetimeObject)

# # datetime_object = datetime.strptime('Jun 1 2005  1:33PM', '%b %d %Y %I:%M%p')

# # print(datetime_object)

# print(datetime.isoformat(datetimeObject))

from pymongo import MongoClient

client = MongoClient('localhost',27017)
db = client.OFFICIAL_DATABASE
col = db['posts']

# r = datetime(12,1,1,11,11,11,11)
# col.insert_one({'date':r})

# def cvertDateToISODate(date):
#     isoTimeObject = datetime.strptime(date,'%b %d, %Y')
#     print(type(datetime.isoformat(isoTimeObject)))
#     return datetime.isoformat(isoTimeObject)

# cvertDateToISODate("Apr 21, 2019")


# for x in col.find({'magazine':'TodaySharing'}):
#     url_test = x['url']
#     print(url_test)
#     date_before = x['date']
#     if(type(date_before) == type("geg")):
#         col.update_one({'url':url_test},{'$set':{"date":cvertDateToISODate(date_before)}})

