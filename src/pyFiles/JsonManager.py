import json
from pprint import pprint

def getQuestions(file):

	with open(file) as json_file:
		data = json.load(json_file)

	questions = []
	options = []

	for i in range(len(data['questions'])):
		questions.append(data['questions'][i]['description'])
		if len(options) == 0:
			optionlist = data['questions'][i]['options']
			for item in optionlist:
				for key,value in item.items():
					options.insert(int(key),value)

	result = {
				"Questions" : questions,
				"Options" : options
	}

	return result

# val = getQuestions("/home/toshiba/github/Psyheal/question.json")
# l = val["Questions"]
# for i in l:
# 	print(i)