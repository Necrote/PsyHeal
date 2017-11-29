import json
from pprint import pprint
import sys
import pymongo
import urllib
import datetime

enddate = datetime.datetime.today()
duration = 15

uri = "mongodb://csubhedar:"+urllib.parse.quote_plus("showoff@123")+"@ds241055.mlab.com:41055/patient_details"

client = pymongo.MongoClient(uri)
db = client.get_default_database()
PDetails = db['patient_details']

personality = ["Openness","Conscientiousness","Extraversion","Agreeableness","Emotional range"]


startdate = enddate - datetime.timedelta(15)


Pname = "NameA"
cursor = PDetails.find_one({'_id':Pname , 'Record.Date':{'$gte': startdate, '$lt': enddate}})

if cursor is None:
	print("No Results")

result = []

for key,value in cursor.items():
 	if 'count' in key:
 		count = value
 	if 'Record' in key:
 		result = value


pprint(result)

# list = []

# attribute = 'Artistic interests'
# factor = personality[0];

# # print(result[1]['Analysis'][0]['name'])

# for i in range(count):
# 	l=len(result[i]['Analysis'])
# 	print(l)
# 	for j in range(l):
# 		if result[i]['Analysis'][j]['name'] == factor:
# 			break
	
# 	parentFactor = result[i]['Analysis'][j]
# 	pprint(parentFactor)


# l = len(result[0]['Analysis'])

# print(l)

