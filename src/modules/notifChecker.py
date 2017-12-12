# from NotificationManager import *
# info = getNotifications("d1", None)
# notifList = info[0]['Notifications'][:]
# # print(notifList[0])
# # for i in range(len(notifList)):
# #     print(notifList[i]['PatientId'])
# #     print(notifList[i]['Date'].date().strftime('%d-%m-%Y'))
# #     print(notifList[i]['Status'])
# notifTable = []
# for i in range(len(notifList)):
#     tmpList = []
#     tmpList.append(notifList[i]['PatientId'])
#     tmpList.append( getIsoDate(notifList[0]['Date']['$date']) )
#     tmpList.append(notifList[i]['Status'])
#     tmpList.append(notifList[i]['Count'])
#     tmpList.append(notifList[i]['CriticalList'])
#     notifTable.append(tmpList)

# for row in notifTable:
#     print(row[1], row[0], row[2], row[4])
from PatientManager import *
from Grapher import *

criticalList = ['Melancholy', 'Self-consciousness', 'Susceptible to stress']
pDF = getDataFrame("p2", 6, 5)
plot = generateGraphReport(pDF, criticalList)