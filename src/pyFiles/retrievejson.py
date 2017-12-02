import json
from pprint import pprint
import sys
import pymongo
import urllib
import datetime
import Constants
import pandas as pd

enddate = datetime.datetime.today()
duration = 15

uri = "mongodb://csubhedar:"+urllib.parse.quote_plus("showoff@123")+"@ds241055.mlab.com:41055/patient_details"

client = pymongo.MongoClient(uri)
db = client.get_default_database()
PDetails = db['patient_details']

startdate = enddate - datetime.timedelta(duration)

Pname = "NameA"
cursor = PDetails.find_one({'_id':Pname})

if cursor is None:
	print("No Results")

result = []

for key,value in cursor.items():
 	if 'count' in key:
 		count = value
 	if 'Record' in key:
 		result = value


# list = []

# attribute = 'Adventurousness'
# factor = Constants.personality_traits[0];

# print(result[1]['Analysis'][0]['name'])

# Older For
# for i in range(count):
# 	l=len(result[i]['Analysis'])
# 	if not(startdate <= result[i]["Date"] <= enddate):
# 		continue
# 	for j in range(l):
# 		if result[i]['Analysis'][j]['name'] == factor:
# 			break
	
# 	parentFactor = result[i]['Analysis'][j]
# 	children = len(parentFactor["children"])
# 	for j in range(children):
# 		if parentFactor["children"][j]["name"] == attribute:
# 			list.append(parentFactor["children"][j]["percentile"])

# l = len(result[0]['Analysis'])

#New Try

colList = []
finalList = []
listsize = 0

for i in range(count):
	if not(startdate <= result[i]["Date"] <= enddate):
		continue
	templist = []
	if "Date" not in colList:
		colList.append("Date")

	templist.insert(colList.index("Date"),result[i]["Date"])
	l=len(result[i]['Analysis'])
	for j in range(l):
		parentFactor = result[i]['Analysis'][j]
		children = parentFactor['children']
		for k in range(len(children)):
			if children[k]['name'] not in colList:
				colList.append(children[k]['name'])
			templist.insert(colList.index(children[k]['name']),children[k]['percentile']*100)		

	finalList.append(templist)		

# print(colList)
# print(finalList)

df = pd.DataFrame(finalList)
df.columns = colList
df = df.sort_values(by="Date")

avglist = df[colList[1]].tolist()
mean = sum(avglist)/len(avglist)
# print(mean)
lastrow = []
lastrow.insert(colList.index('Date'),None)

for head in df.columns:
	if head != 'Date':
		avglist = df[head].tolist()
		mean = sum(avglist)/len(avglist)
		lastrow.insert(colList.index(head),mean)

df.loc[len(df)] = lastrow
print(df)