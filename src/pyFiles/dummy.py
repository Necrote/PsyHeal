import PatientManager
import datetime
import pygal    

date = datetime.datetime(2017,10,13)
df = PatientManager.getDataFrame("p1",date,15)

criticalFactors = ['Authority-challenging','Cautiousness','Sympathy','Trust','Prone to worry','Melancholy','Immoderation','Self-consciousness','Susceptible to stress','Cheerfulness']
df1=df[['Date','Authority-challenging','Cautiousness','Sympathy','Trust','Prone to worry','Melancholy','Immoderation','Self-consciousness','Susceptible to stress','Cheerfulness']]
# print(df.loc[:,'Orderliness':'Cooperation'])
# print(df1)

dates = [ x.date() for x in df1['Date'][:-1] ]
# print(dates)

chart = pygal.Line(tooltip_fancy_mode=True, title='patient_report', fill=True, x_label_rotation=30, interpolate='hermite', interpolation_parameters={'type': 'kochanek_bartels', 'b': -1, 'c': 1, 't': 1})
chart.x_labels = map(lambda d: d.strftime('%d-%m-%Y'),dates)
chart.value_formatter = lambda x: "%.2f%%" % x

for factor in criticalFactors:
    chart.add(factor, df1[factor][:-1], view=False)

chart.render_to_file('chart.svg')
