def generateGraphReport(pDF, criticalList, patientID):
    import pygal
    import datetime
    import Constants

    colList = ['Date'] + Constants.SelectedAttributes 
    df1 = pDF[colList]
    dates = [ x.date() for x in df1['Date'][:-1] ]

    chart = pygal.Line(title='patient_'+patientID+'_report', dots_size=5, stroke_style={'width': 5},x_label_rotation=30, interpolate='hermite', interpolation_parameters={'type': 'kochanek_bartels', 'b': -1, 'c': 1, 't': 1})
    chart.x_labels = map(lambda d: d.strftime('%d-%m-%Y'),dates)
    chart.value_formatter = lambda x: "%.2f%%" % x

    colList = colList[1:]
    for factor in Constants.SelectedAttributes:
        chart.add(factor, df1[factor][:-1])

    return chart.render_data_uri()