import Constants

def isNotificationRequired(meanList , columnList):

	newColList = []
	newMeanList = []
	for item in columnList:
		if item in Constants.SelectedAttributes:
			newColList.append(item)
			newMeanList.insert(newColList.index(item),meanList[columnList.index(item)])

	AttriList = []

	for item in newColList:

		if Constants.Constraints[item][0] <= newMeanList[newColList.index(item)]*100 <= Constants.Constraints[item][1]:
			AttriList.append(item)

	if(len(AttriList) < Constants.CriticalCount):
		return False
	else :
		return AttriList



# meanList = [	0.12868546390125346, 
# 				0.6300070387454954, 
# 				0.8074990410621257, 
# 				0.24952251786611898, 
# 				0.9109560512245821, 
# 				0.9177452030221138, 
# 				0.4905470058399442, 
# 				0.9334423284785451, 
# 				0.9209115828821041, 
# 				0.0617517715338148,
# 				0.40886027911894834, 
# 				0.32354856593411846, 
# 				0.47960715296176887, 
# 				0.4867575713587311, 
# 				0.24217877689048026, 
# 				0.07069224968719585, 
# 				0.37100904025530745, 
# 				0.13366952668419663, 
# 				0.7529353891874218, 
# 				0.817477650787926, 
# 				0.7783441865005304, 
# 				0.7987728880796996, 
# 				0.93302105164135, 
# 				0.5889386701616677, 
# 				0.2357842063541468, 
# 				0.819072747107493, 
# 				0.755231781455873, 
# 				0.7493334615948752, 
# 				0.668303352931981, 
# 				0.7267445652955833]

# columnList = [  'Adventurousness', 
# 				'Artistic interests', 
# 				'Emotionality', 
# 				'Imagination', 
# 				'Intellect', 
# 				'Authority-challenging', 
# 				'Achievement striving', 
# 				'Cautiousness', 
# 				'Dutifulness', 
# 				'Orderliness', 
# 				'Self-discipline', 
# 				'Self-efficacy', 
# 				'Activity level', 
# 				'Assertiveness', 
# 				'Cheerfulness', 
# 				'Excitement-seeking', 
# 				'Outgoing', 
# 				'Gregariousness', 
# 				'Altruism', 
# 				'Cooperation', 
# 				'Modesty', 
# 				'Uncompromising', 
# 				'Sympathy', 
# 				'Trust', 
# 				'Fiery', 
# 				'Prone to worry', 
# 				'Melancholy', 
# 				'Immoderation', 
# 				'Self-consciousness', 
# 				'Susceptible to stress']

# value =isNotificationRequired(meanList,columnList)
# print(value)

