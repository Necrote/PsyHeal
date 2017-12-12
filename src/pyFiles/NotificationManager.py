import json
from pprint import pprint
import sys
import pymongo
import urllib
import datetime
import time
from bson.json_util import dumps
import Constants
import sqlite3 as sql
import conditionUtil

def ifExsists(con,newId):
	if(con.find({'_id':newId}).count()>0):
		return True
	else:
		return False


def createNotification(pId,doctorIds,count,criticalvalues):

	try: 
		uri = "mongodb://csubhedar:"+urllib.parse.quote_plus("showoff@123")+"@ds241055.mlab.com:41055/patient_details"

		date = datetime.datetime.now()
		client = pymongo.MongoClient(uri)
		db = client.get_default_database()
		status = False

		NotiDb = db['notifications']

		for doctorId in doctorIds:

			if(ifExsists(NotiDb,doctorId)):
				SEED_DATA = {

						'PatientId' : pId,
	 					'Date' : date,
	 					'Status': status,
	 					'Count' : count,
	 					'CriticalList' : criticalvalues
					}
				
				NotiDb.update({'_id' : doctorId},{'$addToSet' : {'Notifications' : SEED_DATA}})

			else:
				SEED_DATA = [
				{
					'_id' : doctorId,
					'Notifications': [
						{'PatientId' : pId,
						'Date' : date,
						'Status': status,
						'Count' : count,
						'CriticalList' : criticalvalues}
					]
				}
				]

				NotiDb.insert_many(SEED_DATA)

		client.close()    

		return True

	except:

		return False

# Read Notifiacation

def getNotifications(doctorId,value):
	uri = "mongodb://csubhedar:"+urllib.parse.quote_plus("showoff@123")+"@ds241055.mlab.com:41055/patient_details"

	client = pymongo.MongoClient(uri)
	db = client.get_default_database()


	NotiDb = db['notifications']


	if value != None:
		cursor = NotiDb.find({"$and":[{"Notifications.Status": value},{"_id":doctorId}]})

		for doc in cursor:
			array = doc['Notifications']
			finalarr = []
			for i in range(len(array)):
				if(array[i]["Status"] == value):
					finalarr.append(array[i])
		doc['Notifications'] = finalarr
		result = dumps(doc)
	else :
		cursor = NotiDb.find({"_id" : doctorId})
		result = dumps(cursor)
	
	
	info = json.loads(result) 

	return info

def getIsoDate(timevalue):
	readable_date = time.strftime("%Y-%m-%d", time.localtime(int(timevalue / 1000)))
	return readable_date


def conditionalNotification(Pname):
	uri = "mongodb://csubhedar:"+urllib.parse.quote_plus("showoff@123")+"@ds241055.mlab.com:41055/patient_details"

	client = pymongo.MongoClient(uri)
	db = client.get_default_database()

	PDetails = db['patient_details']
	NotiDb = db['notifications']
	dbPath = "src/database/"

	cursor = PDetails.find_one({'_id':Pname})

	if cursor is None:
		return None

	for key,value in cursor.items():
 		if 'count' in key:
 			count = value
 		if 'Record' in key:
 			result = value

	if count < Constants.CriticalCount:
 		return None

	finalList = []
	colList = []
	endpoint = count - Constants.recordLimit
	RidList = []
	arr = [0]*5

	for i in range(count,endpoint,-1):
		RidList.append((Pname+str(i)))

	for i in range(count):
		if result[i]['Rid'] in RidList:
			templist = []
			l = len(result[i]['Analysis'])
			for j in range(l):
				parentFactor = result[i]['Analysis'][j]
				children = parentFactor['children']
				for k in range(len(children)):
					if children[k]['name'] not in colList:
						colList.append(children[k]['name'])
					templist.insert(colList.index(children[k]['name']),children[k]['percentile'])						

			finalList.append(templist)		

	cols = len(finalList[0])
	rows = len(finalList)
	totals = cols * [0.0]
	
	for i in range(rows):
		for j in range(cols):
			totals[j] += finalList[i][j]

	mean = [total/rows for total in totals]


# Condition for Generating Notifications

	result = conditionUtil.isNotificationRequired(mean,colList)

	if result != False:

		try:
			conn = sql.connect(dbPath+"psyheal.db")
			cur = conn.cursor()
			cur.execute("SELECT username FROM user WHERE accType = 'doctor' ")
			query = cur.fetchall()
			doctorsList = []
			for i in query:
				doctorsList.append(i[0])
			createNotification(Pname,doctorsList,count,result)
		except:
			error = "internal DB error."
		finally:
			conn.close()


def setViewed(DoctorId,Pid,count):
	uri = "mongodb://csubhedar:"+urllib.parse.quote_plus("showoff@123")+"@ds241055.mlab.com:41055/patient_details"
	client = pymongo.MongoClient(uri)
	db = client.get_default_database()
	
	NotiDb = db['notifications']		

	cursor = NotiDb.find_one({"_id" : DoctorId})

	for key,value in cursor.items():
 		if 'Notifications' in key:
 			notiarray = value
 		
	for i in range(len(notiarray)):
		if notiarray[i]['PatientId'] == Pid and notiarray[i]['Count'] == count:
			if notiarray[i]['Status'] == False:
				path = 'Notifications.'+str(i)+'.Status'
				NotiDb.update({'_id': DoctorId},{'$set':{path : True}})


# conditionalNotification("p1")
# setViewed("d1","p1",11)
result=getNotifications("d1",None)
pprint(result)