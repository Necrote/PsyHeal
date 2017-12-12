import json
from pprint import pprint
import sys
import pymongo
import urllib
import datetime
import sys,traceback
import time
from bson.json_util import dumps
import Constants
import pandas as pd

def selectAttributes(factor , attributes):
	temp_arr = []
	for i in range(0,len(factor["children"])):
		if factor["children"][i]["name"] in attributes:
			temp_arr.append(factor["children"][i])

	factor["children"]=temp_arr
	temp_arr = []
	return factor

def ifExsists(con,newId):
	if(con.find({'_id':newId}).count()>0):
		return True
	else:
		return False

def UploadFile(patientName , JsonFile ):

	try:
	
		with open(JsonFile) as json_file:
			json_data = json.load(json_file)		

		persondata = json_data["personality"]

		uri = "mongodb://csubhedar:"+urllib.parse.quote_plus("showoff@123")+"@ds241055.mlab.com:41055/patient_details"

		date = datetime.datetime.now()

		client = pymongo.MongoClient(uri)
		db = client.get_default_database()
		PDetails = db['patient_details']
		count = 0

		#Selecting for Openness
		persondata[0] = selectAttributes(persondata[0],Constants.OpAttri)

		#Selecting for Conscientiousness
		persondata[1] = selectAttributes(persondata[1],Constants.ConAttri)

		#Selecting for Extraversion
		persondata[2] = selectAttributes(persondata[2],Constants.ExtraAttri)

		#Selecting for Agreeableness
		persondata[3] = selectAttributes(persondata[3],Constants.AgreeAttri)

		#Selecting for Emotional Range
		persondata[4] = selectAttributes(persondata[4],Constants.EmoAttri)


		if (ifExsists(PDetails,patientName) ):
			cursor = PDetails.find_one({'_id':patientName})
			# print(cursor)
			for key,value in cursor.items():
			 	if 'count' in key:
			 		count = value;

			count+=1
			recordID = patientName+ str(count)

			SEED_DATA = {
				'Rid':recordID,
				 'Date':date,
			 	'Analysis':persondata}
			
			PDetails.update({'_id': patientName},{'$addToSet':{'Record':SEED_DATA}})
			PDetails.update({'_id': patientName},{'$set':{'count': count}})
			print("Record Updated")
		else:
			count+=1;
			recordID=patientName+str(count)
			SEED_DATA = [
	 		{
				'_id' : patientName,
				'count': count,
				'Record' : [
					{'Rid':recordID,
				 	'Date':date,
			 		'Analysis':persondata}
				]
	 	 	}
			]
			print("Record Inserted")
			PDetails.insert_many(SEED_DATA)

		client.close()

		return True

	except:

		exc_type, exc_value, exc_traceback = sys.exc_info()
		traceback.print_exception(exc_type, exc_value, exc_traceback)

		return False

def getIsoDate(timevalue):
	readable_date = time.strftime("%Y-%m-%d", time.localtime(int(timevalue / 1000)))
	return readable_date


def getDataFrame(Pname , recordNumber , number):

	uri = "mongodb://csubhedar:"+urllib.parse.quote_plus("showoff@123")+"@ds241055.mlab.com:41055/patient_details"

	client = pymongo.MongoClient(uri)
	db = client.get_default_database()
	PDetails = db['patient_details']


	cursor = PDetails.find_one({'_id':Pname})

	if cursor is None:
		return None

	result = []

	for key,value in cursor.items():
 		if 'count' in key:
 			count = value
 		if 'Record' in key:
 			result = value

	if recordNumber > count or recordNumber-number<0:
 		return

	RidList = []
	endpoint = recordNumber - number
	colList = []
	finalList = []
	listsize = 0

	for i in range(recordNumber,endpoint,-1):
		RidList.append((Pname+str(i)))

	for i in range(count):
		if result[i]['Rid'] in RidList:
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

	if len(finalList)==0:
		return "No Results Found"

	df = pd.DataFrame(finalList)
	df.columns = colList
	df = df.sort_values(by = "Date")

	avglist = df[colList[1]].tolist()
	mean = sum(avglist)/len(avglist)
	lastrow = []
	lastrow.insert(colList.index('Date'),None)

	for head in df.columns:
		if head != 'Date':
			avglist = df[head].tolist()
			mean = sum(avglist)/len(avglist)
			lastrow.insert(colList.index(head),mean)

	df.loc[len(df)] = lastrow

	return df
