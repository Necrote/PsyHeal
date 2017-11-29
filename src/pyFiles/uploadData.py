import json
from pprint import pprint
import sys
import pymongo
import urllib
import datetime
import sys,traceback
import time
from bson.json_util import dumps


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

		Openness = ['Adventurousness','Artistic interests','Emotionality','Imagination','Intellect','Authority-challenging']
		Conscientiousness = ['Achievement striving','Cautiousness','Dutifulness','Orderliness','Self-discipline','Self-efficacy']
		Extraversion = ['Activity level','Assertiveness','Cheerfulness','Excitement-seeking','Outgoing','Gregariousness']
		Agreeableness = ['Altruism','Cooperation','Modesty','Uncompromising','Sympathy','Trust']
		EmotionalRange = ['Fiery','Prone to worry','Melancholy','Immoderation','Self-consciousness','Susceptible to stress']

		OpAttri = [ Openness[0] , Openness[2] , Openness[3]]
		ConAttri = [ Conscientiousness[0] , Conscientiousness[1] , Conscientiousness[2]]
		ExtraAttri = [ Extraversion[0] , Extraversion[1] , Extraversion[3]]
		AgreeAttri = [ Agreeableness[1] , Agreeableness[2] , Agreeableness[4]]
		EmoAttri = [ EmotionalRange[2] , EmotionalRange[4] , EmotionalRange[5]] 

		persondata = json_data["personality"]

		uri = "mongodb://csubhedar:"+urllib.parse.quote_plus("showoff@123")+"@ds241055.mlab.com:41055/patient_details"

		date = datetime.datetime.now()

		client = pymongo.MongoClient(uri)
		db = client.get_default_database()
		PDetails = db['patient_details']
		count = 0

		#Selecting for Openness
		persondata[0] = selectAttributes(persondata[0],OpAttri)

		#Selecting for Conscientiousness
		persondata[1] = selectAttributes(persondata[1],ConAttri)

		#Selecting for Extraversion
		persondata[2] = selectAttributes(persondata[2],ExtraAttri)

		#Selecting for Agreeableness
		persondata[3] = selectAttributes(persondata[3],AgreeAttri)

		#Selecting for Emotional Range
		persondata[4] = selectAttributes(persondata[4],EmoAttri)


		if (ifExsists(PDetails,patientName) ):
			cursor = PDetails.find_one({'_id':patientName})
			# print(cursor)
			for key,value in cursor.items():
			 	if 'count' in key:
			 		count = value;

			count+=1
			recordID = patientName+ str(count)

			SEED_DATA = 
			{'Rid':recordID,
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



# file = "en_v3.json"
# result=UploadFile("NameA",file)
