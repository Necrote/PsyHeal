import json
from pprint import pprint
import sys
import pymongo
import urllib
import datetime

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
				SEED_DATA = 
					{
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

uri = "mongodb://csubhedar:"+urllib.parse.quote_plus("showoff@123")+"@ds241055.mlab.com:41055/patient_details"
client = pymongo.MongoClient(uri)
db = client.get_default_database()