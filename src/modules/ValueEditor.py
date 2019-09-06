def editValues(filename, key, newvalue, splitter='='):
    with open(filename, "r") as values:
        lines = values.readlines()
        for i, line in enumerate(lines):
            if line.split(splitter)[0].strip(' \n') == key:
                lines[i] = line.split(splitter)[0] + splitter + ' ' + newvalue + '\n'
    with open(filename, "w") as values:
        values.write("".join(lines))

def formMCQ(desc):
    return '{"description": "'+desc+'",\n "options":[{"1":"Strongly Disagree"}, {"2": "Disagree"}, {"3": "Neither Agree nor disagree"}, {"4": "Agree"}, {"5": "Strongly agree"}]\n}\n\n'

def addMCQ(filename, desc):
    mcqstring = formMCQ(desc)
    with open(filename, "r") as mcqfile:
        lines = mcqfile.readlines()
        sz = len(lines)
        if lines[2][0] != '{':
            lines[sz-2] = mcqstring           
        else:
            lines[sz-2] = ',\n' + mcqstring

    with open(filename, "w") as mcqfile:
        mcqfile.write("".join(lines))

def removeMCQ(filename, index, qsize):
    lines = []
    with open(filename, "r") as mcqfile:
        lines = mcqfile.readlines()

    if index > qsize:
        return
    with open(filename, "w") as mcqfile:
        if qsize == 1:
            lbound = 2
            ubound = 4
        elif index == qsize:
            lbound = 4*(index-1) + 1
            ubound = lbound + 3
        else:
            lbound = 4*(index-1) + 2
            ubound = lbound + 3

        for i in range(len(lines)):
            if i<lbound or i>ubound:
                mcqfile.write(lines[i])
