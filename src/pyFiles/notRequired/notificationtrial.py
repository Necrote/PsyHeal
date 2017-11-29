import json
from pprint import pprint
import sys
import pymongo
import urllib
import datetime
import time
from bson.json_util import dumps

uri = "mongodb://csubhedar:"+urllib.parse.quote_plus("showoff@123")+"@ds241055.mlab.com:41055/patient_details"

client = pymongo.MongoClient(uri)
db = client.get_default_database()


NotiDb = db['notifications']

doctorId =	"D1"
value = False

if value != None:
	cursor = NotiDb.find({"$and":[{"Notifications.Status": value},{"_id":doctorId}]},{"Notifications.$.Status":1})
else :
	cursor = NotiDb.find({"_id" : doctorId})

result = dumps(cursor,cls=DateTimeEncoder)

info = json.loads(result) 

pprint(info)

bson_timevalue = info[0]["Notifications"][0]["Date"]["$date"]
readable_date = time.strftime("%Y-%m-%d", time.localtime(int(bson_timevalue / 1000)))

print(readable_date) 

