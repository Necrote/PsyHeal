import json
from pprint import pprint
import sys
import pymongo
import urllib
import datetime

date = datetime.datetime(2017,8,22)
duration = 15

uri = "mongodb://csubhedar:"+urllib.parse.quote_plus("showoff@123")+"@ds241055.mlab.com:41055/patient_details"

client = pymongo.MongoClient(uri)
db = client.get_default_database()
PDetails = db['patient_details']

personality = ["Openness","Conscientiousness","Extraversion","Agreeableness","Emotional range"]

