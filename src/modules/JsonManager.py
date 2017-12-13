def getQuestions(file):
	import json

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

	return questions, options