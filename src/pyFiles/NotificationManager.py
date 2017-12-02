import json
from pprint import pprint
import sys
import pymongo
import urllib
import datetime
import time
from bson.json_util import dumps

def ifExsists(con,newId):
	if(con.find({'_id':newId}).count()>0):
		return True
	else:
		return False


def createNotification(pId,doctorIds):

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
	 					'Status': status
					}
				
				NotiDb.update({'_id' : doctorId},{'$addToSet' : {'Notifications' : SEED_DATA}})

			else:
				SEED_DATA = [
				{
					'_id' : doctorId,
					'Notifications': [
						{'PatientId' : pId,
						'Date' : date,
						'Status': status}
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
				if(array[i]["Status"] == False):
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


# doctors = []
# doctors.append("D1")
# info=getNotifications("D1",True)
# pprint(info)