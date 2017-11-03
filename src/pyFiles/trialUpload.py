import sys
import pymongo
import urllib
import datetime

uri = "mongodb://csubhedar:"+urllib.parse.quote_plus("showoff@123")+"@ds241055.mlab.com:41055/patient_details"

pname = "Name1"

date = "date1"
personality = [
	{
        'decade': '1970s',
        'artist': 'Debby Boone',
        'song': 'You Light Up My Life',
        'weeksAtOne': 10
    },
    {
        'decade': '1980s',
        'artist': 'Olivia Newton-John',
        'song': 'Physical',
        'weeksAtOne': 10
    },
    {
        'decade': '1990s',
        'artist': 'Mariah Carey',
        'song': 'One Sweet Day',
        'weeksAtOne': 16
    }

]

SEED_DATA = [
		{
			'pid':pname,
			'record':[
				{'date':datetime.datetime.now(),
				 'analysis': personality}
			]
		}

]


client = pymongo.MongoClient(uri)

db = client.get_default_database()

songs = db['patient_details']


songs.insert_many(SEED_DATA)

client.close()
