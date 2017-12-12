import PatientManager
import datetime
import conditionUtil

date = datetime.datetime(2017,10,13)
df = PatientManager.getDataFrame("p1",date,15)
df1=df[['Authority-challenging','Cautiousness','Sympathy','Trust','Prone to worry','Melancholy','Immoderation','Self-consciousness','Susceptible to stress','Cheerfulness']]
# print(df.loc[:,'Orderliness':'Cooperation'])
# print(df1)

# print(df1.iloc[0:3])
start = 0
end = 5

columnlist = df1.columns.values.tolist()
meanlist = []
# print(columnlist)

# while end<=11:
# 	count = 0
# 	for column in df1:
# 		tempdf = df1.iloc[start:end]	
# 		if(column != 'Date'):
# 			val =	sum(tempdf[column])/5
# 			if column == 'Authority-challenging' and 92.00 <= val <= 100.00:
# 				count+=1
# 			if column == 'Cautiousness' and 93.00 <= val <= 99.00:
# 				count+=1
# 			if column == 'Sympathy' and 0.00 <= val<= 15.00:
# 				count+=1
# 			if column == 'Trust' and 0.00 <= val <= 15.00:
# 				count+=1
# 			if column == 'Prone to worry' and 85.00 <= val <= 100.00:
# 				count+=1
# 			if column == 'Melancholy' and 88.00 <= val <= 100.00:
# 				count+=1
# 			if column == 'Immoderation' and 80.00 <= val <= 100.00:
# 				count+=1
# 			if column == 'Self-consciousness' and 75.00 <= val <= 100.00:
# 				count+=1
# 			if column == 'Susceptible to stress' and 70.00 <= val <= 100.00:
# 				count+=1
# 			if column == 'Cheerfulness' and 0.00 <= val <= 20.00:
# 				count+=1
# 	print(str(start)+"  "+str(end)+" count: "+str(count))
# 	start+=1
# 	end+=1

while end<=11:
	count = 0
	for column in df1:
		tempdf = df1.iloc[start:end]	
		val =	sum(tempdf[column])/5
		meanlist.insert(columnlist.index(column),val/100)
	
	result = conditionUtil.isNotificationRequired(meanlist,columnlist)
	print(result)
	start+=1
	end+=1