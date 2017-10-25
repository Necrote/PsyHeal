import json
from pprint import pprint

with open("en_v3.json") as json_file:
	json_data = json.load(json_file)

persondata = json_data["personality"]

for j in xrange(0,len(persondata[4])+1):
	print(persondata[4]["children"][j]["name"])


