from flask import Flask, session, flash, redirect, render_template, jsonify, request, url_for
from dotenv import load_dotenv
from pymongo import MongoClient
import speech_recognition as sr
from shutil import copyfile
import gridfs
import cognitive_face as CF
from PIL import Image, ImageDraw
import sqlite3 as sql
import nexmo
import json
import sys
import os
sys.path.insert(0, 'src/modules/')
from WatsonAPI import *
from PatientManager import *
from Grapher import *
from JsonManager import *
from NotificationManager import *
from conditionUtil import *
from ValueEditor import *

load_dotenv('conf.env')

app = Flask(__name__)
app.secret_key = env_var('FLASK_SECRET_KEY')

NEXMO_API_KEY = env_var('NEXMO_API_KEY')
NEXMO_API_SECRET = env_var('NEXMO_API_SECRET')
NEXMO_NUMBER = env_var('NEXMO_NUMBER')
nexmo_client = nexmo.Client(api_key=NEXMO_API_KEY, api_secret=NEXMO_API_SECRET)

PROJECT_HOME = os.path.dirname(os.path.realpath(__file__))
UPLOAD_FOLDER = '{}/uploads/'.format(PROJECT_HOME)
MOD_FOLDER = '{}/modified/'.format(PROJECT_HOME)
DOWNLOAD_FOLDER = '{}/static/downloads/'.format(PROJECT_HOME)
IMG_URL = os.path.join('static', 'downloads')
app.config['UPLOAD_FOLDER'] = UPLOAD_FOLDER
app.config['DOWNLOAD_FOLDER'] = DOWNLOAD_FOLDER
app.config['MOD_FOLDER'] = MOD_FOLDER
app.config['SEND_FILE_MAX_AGE_DEFAULT'] = 0

typeList = ["admin","doctor","patient"]
optionList = ['All', 'Checked', 'Unchecked']
paramList = ["recordLimit","CriticalCount"]
notifTable = None
dbPath = "src/database/"
modulesPath = "src/modules/"
textInputPath = "input/textinput/"
jsonOutputPath = "output/jsonoutput/"
mcqPathFile = modulesPath + "question.json"
tempMcqPathFile = modulesPath + "tempquestion.json"
constantsPathFile = modulesPath + "Constants.py"

RECORD = "record"
AVAILABLE_COMMANDS = {
    'Record': RECORD,
}

def getSessionData():
    if 'username' in session:
        return session['username'], session['password'], session['accType']
    else:
        return None, None, None

def sendSMS(contactNum, message, nexmo_client, NEXMO_NUMBER):
    result = nexmo_client.send_message({
        'from': NEXMO_NUMBER,
        'to': contactNum,
        'text': message,
    })
    err = extract_error(result)
    if err is not None:
        print("There was a problem sending your message: " + err, 'error')

def recordResponse():
    r = sr.Recognizer()
    with sr.Microphone() as source:
        print("Say something!")
        audio = r.listen(source)
        msg = ""
    try:
        msg += r.recognize_google(audio)
        print("Recognized speech: " + msg)
    except sr.UnknownValueError:
        print("Audio is incoherent")
        msg += "Check if your mic is working properly!"
    except sr.RequestError as e:
        print("Failed to fetch results from Google Speech Recognition service; {0}".format(e))
        msg += "***[[ Check if your mic is working properly! ]]***"
    msg+=".\n"
    return msg

########### WebApp Routing & Functionality ###########
@app.route("/", methods=["GET"])
def index():
    username, password, accType = getSessionData()
    return render_template('index.html', username = username, accType = accType)

@app.route("/help", methods=["GET"])
def help():
    username, password, accType = getSessionData()
    return render_template("help.html", username = username, accType = accType)

@app.route("/login", methods = ['GET', 'POST'])
def login():
    username, password, accType = getSessionData()
    error = None
    if request.method == 'POST':
        try:
            usr = request.form['username']
            pwd = request.form['password']
            conn = sql.connect(dbPath+"psyheal.db")
            cur = conn.cursor()
            cur.execute("SELECT * FROM user WHERE username=? AND password=?",(usr,pwd))
            query = cur.fetchall()

            if len(query) != 1 :
                error = 'Invalid username or password. Please try again!'
            else:
                session['username'] = usr
                session['password'] = pwd
                session['accType'] = query[0][2]
                flash('logged in!')
                return redirect(url_for('index'))
        except:
            error = "DB error occured."
        finally:
            conn.close()
    return render_template('login.html',  username = username, accType = accType, error = error)

@app.route('/logout')
def logout():
   session.pop('username', None)
   session.pop('password', None)
   session.pop('accType', None)
   flash('logged out!')
   return redirect(url_for('index'))

@app.route('/newuser')
def newuser():
    username, password, accType = getSessionData()
    error = None
    msg = None
    if accType != 'admin':
        error = 'You are not authorized to add more users! Contact admin.'
    return render_template('newuser.html', username = username, accType = accType, typeList=typeList, error = error, msg = msg)

@app.route('/adduser', methods = ['GET', 'POST'])
def adduser():
    username, password, accType = getSessionData()
    error = None
    msg = None

    if accType != 'admin':
        error = 'You are not authorized to add more users! Contact admin.'
    elif request.method == 'POST':
        try:
            usr = request.form['username']
            pwd = request.form['password']
            accType = request.form['accType']
            contactNum = request.form['contactNum']
            conn = sql.connect(dbPath+"psyheal.db")
            cur = conn.cursor()
            cur.execute("SELECT * FROM user WHERE username=?",(usr,))
            query = cur.fetchall()
            if len(query) > 0:
                error = "username already exists."
            else:
                cur.execute("INSERT INTO user(username,password,accType) VALUES (?,?,?)",(usr,pwd,accType))
                conn.commit()
                msg = "new user created."
        except:
            conn.rollback()
            error = "internal DB error."
        finally:
            conn.close()
        try:
            sms = formMessage(usr, accType, 1)
            sendSMS(contactNum, sms, nexmo_client, NEXMO_NUMBER)
        except:
            error = "couldn't send out SMS."
    return render_template('newuser.html', username = username, accType = accType, typeList=typeList, error = error, msg = msg)

@app.route('/removeuser')
def removeuser():
    username, password, accType = getSessionData()
    error = None
    msg = None
    if accType != 'admin':
        error = 'You are not authorized to add more users! Contact admin.'
    return render_template('removeuser.html', username = username, accType = accType, error = error, msg = msg)

@app.route('/deleteuser', methods = ['GET', 'POST'])
def deleteuser():
    username, password, accType = getSessionData()
    error = None
    msg = None

    if accType != 'admin':
        error = 'You are not authorized to add more users! Contact admin.'
    elif request.method == 'POST':
        try:
            usr = request.form['username']
            conn = sql.connect(dbPath+"psyheal.db")
            if usr == "rootadmin":
                error = "can't remove rootadmin."
            else:
                cur = conn.cursor()
                cur.execute("DELETE FROM user WHERE username=?",(usr,))
                conn.commit()
                msg = "user removed."
        except:
            conn.rollback()
            error = "internal DB error."
        finally:
            conn.close()
    return render_template('removeuser.html', username = username, accType = accType, error = error, msg = msg)

@app.route('/showaccdata')
def showaccdata():
    username, password, accType = getSessionData()
    error = None
    query = None

    if accType != 'admin':
        error = 'You are not authorized to view this page!'
    else:
        try:
            conn = sql.connect(dbPath+"psyheal.db")
            cur = conn.cursor()
            cur.execute("SELECT * FROM user ORDER BY accType")
            query = cur.fetchall()
        except:
            error = "internal DB error."
        finally:
            conn.close()
   
    return render_template("showaccdata.html", username = username, accType = accType, query = query, error = error)

@app.route('/editconstants', methods = ['GET', 'POST'])
def editconstants():
    username, password, accType = getSessionData()
    error = None
    msg = None
    if accType != 'admin':
        error = 'You are not authorized for editing threshold constants.'
    elif request.method == 'POST':
        try:
            replaceParam = request.form['replaceParam']
            if replaceParam == "recordLimit":
                replaceValue = request.form['replaceValue1']
            elif replaceParam == "CriticalCount":
                replaceValue = request.form['replaceValue2']
            editValues(constantsPathFile, replaceParam, replaceValue)
        except:
            error = "failed to change threshold constants."
        msg = "successfully changed threshold constants."
    return render_template('editconstants.html', username = username, accType = accType, error = error, msg = msg, paramList = paramList)

@app.route('/newmcq')
def newmcq():
    username, password, accType = getSessionData()
    error = None
    msg = None
    if accType != 'patient':
        error = 'You are not authorized for questionnaire.'
    qList, optionList = getQuestions(mcqPathFile)
    return render_template('newmcq.html', username = username, accType = accType, error = error, msg = msg, qList = qList, optionList = optionList, qsz = len(qList), osz = len(optionList))

@app.route('/addmcqentry', methods = ['GET', 'POST'])
def addmcqentry():
    username, password, accType = getSessionData()
    error = None
    msg = None

    if accType != 'patient':
        error = 'You are not authorized for adding text entries.'
    elif request.method == 'POST':
        try:
            qList, optionList = getQuestions(mcqPathFile)
            responseList = []
            for i in range(len(qList)):
               responseList.append(request.form['q'+str(i)])
            entry = ""
            for i in range(len(responseList)):
                entry += "I "
                entry += optionList[ int(responseList[i]) ]
                entry += " that "+qList[i]+" "
            ctr = -19
            with open(textInputPath+'txtEntryCounter.json') as json_data:
                ctrs = json.load(json_data)
            if username not in ctrs.keys():
                ctrs[username] = 0
            ctrs[username] += 1
            ctr = ctrs[username]
            inputFilePath = textInputPath+username+"_entry"+str(ctr)+".txt"
            outputFilePath = jsonOutputPath+username+"_report"+str(ctr)+".json"
            with open(inputFilePath, "w+") as entryFile:
                entryFile.write(entry)
            with open(textInputPath+'txtEntryCounter.json', 'w+') as fp:
                json.dump(ctrs, fp)
            try:
                callWatsonAPI(inputFilePath, outputFilePath)
            except:
                error = "failed to call Watson API."
            try:
                UploadFile(username, outputFilePath)
            except:
                error = "failed to upload report to MongoDB."
            try:
                conditionalNotification(username)
            except:
                error = "failed to check for critical conditions."
            msg = "entry added."
        except:
            error = "internal write error."
    return render_template('newmcq.html', username = username, accType = accType, error = error, msg = msg, qList = qList, optionList = optionList, qsz = len(qList), osz = len(optionList))

@app.route('/newentry')
def newentry():
    username, password, accType = getSessionData()
    error = None
    msg = None
    if accType != 'patient':
        error = 'You are not authorized for adding text entries.'
    return render_template('addentry.html', username = username, accType = accType, error = error, msg = msg, commands=AVAILABLE_COMMANDS)

@app.route('/addentry', methods = ['GET', 'POST'])
def addentry():
    username, password, accType = getSessionData()
    error = None
    msg = None

    if accType != 'patient':
        error = 'You are not authorized for adding text entries.'
    elif request.method == 'POST':
        try:
            entry = request.form['entry']
            ctr = -19
            with open(textInputPath+'txtEntryCounter.json') as json_data:
                ctrs = json.load(json_data)
            if username not in ctrs.keys():
                ctrs[username] = 0
            ctrs[username] += 1
            ctr = ctrs[username]
            inputFilePath = textInputPath+username+"_entry"+str(ctr)+".txt"
            outputFilePath = jsonOutputPath+username+"_report"+str(ctr)+".json"
            with open(inputFilePath, "w+") as entryFile:
                entryFile.write(entry)
            with open(textInputPath+'txtEntryCounter.json', 'w+') as fp:
                json.dump(ctrs, fp)
            try:
                callWatsonAPI(inputFilePath, outputFilePath)
            except:
                error = "failed to call Watson API."
            try:
                UploadFile(username, outputFilePath)
            except:
                error = "failed to upload report to MongoDB."
            try:
                conditionalNotification(username)
            except:
                error = "failed to check for critical conditions."
            msg = "entry added."
        except:
            error = "internal write error."
    return render_template('addentry.html', username = username, accType = accType, error = error, msg = msg, commands=AVAILABLE_COMMANDS)

@app.route('/suggestmcq', methods = ['GET', 'POST'])
def suggestmcq():
    username, password, accType = getSessionData()
    error = None
    msg = None
    if accType != 'patient':
        error = 'You are not authorized for suggesting new MCQs.'
    elif request.method == 'POST':
        try:
            mcq = request.form['mcq']
            addMCQ(tempMcqPathFile, mcq)
        except:
            error = "failed to add MCQ to suggestions!"
        msg = "successfully added MCQ to suggestions."
    return render_template('suggestmcq.html', username = username, accType = accType, error = error, msg = msg)

@app.route('/approvemcq', methods = ['GET', 'POST'])
def approvemcq():
    qList, optionList = getQuestions(tempMcqPathFile)
    qSize = len(qList)
    username, password, accType = getSessionData()
    error = None
    msg = None
    status = 0;
    if accType != 'doctor':
        error = 'You are not authorized for approving MCQs.'
    elif qSize == 0:
        msg = "No new MCQ suggestions."
    elif request.method == 'POST':
        try:
            mode = request.form['submit']
            index = int(request.form['index']);
            if mode == "Approve":
                msg = "Approved selected MCQ."
                addMCQ(mcqPathFile, qList[index-1])
            elif mode == "Reject":
                msg = "Rejected selected MCQ."
            removeMCQ(tempMcqPathFile,index,qSize)
            qList, optionList = getQuestions(tempMcqPathFile)
            qSize = len(qList)
        except:
            error = "Failed to make any changes!"
    return render_template('approvemcq.html', username = username, accType = accType, error = error, msg = msg, qList = qList, qSize = qSize)

@app.route('/notification')
def notification():
    username, password, accType = getSessionData()
    error = None
    msg = None
    filterOption = request.args.get("filterOption")
    if filterOption == None:
        filterOption = 'All'
    if accType != 'doctor':
        error = 'You are not authorized for viewing notification reports.'
    global notifTable
    notifTable = getNotifications(username, filterOption)
    if len(notifTable) == 0:
        msg = "No crticial report notifications."
    return render_template('notification.html', username = username, accType = accType, error = error, msg = msg, notifTable = notifTable, sz = len(notifTable), optionList = optionList, filterOption = filterOption)

@app.route('/viewreport', methods = ['GET', 'POST'])
def viewreport():
    username, password, accType = getSessionData()
    error = None
    msg = None
    if accType != 'doctor':
        error = 'You are not authorized for viewing patient reports.'
    elif request.method == 'POST':
        recordIdx = int(request.form['report'])
        global notifTable
        patientID = notifTable[recordIdx][0]
        count = notifTable[recordIdx][3]
        criticalList = notifTable[recordIdx][4]
        notifTable = None

        try:
            setViewed(username, patientID, count)
            pDF = getDataFrame(patientID, count, 5)
            plot = generateGraphReport(pDF, criticalList, patientID)
            patientImage = downloadpic(patientID)
        except:
            error = "failed to generate graphical report."
    return render_template('viewreport.html', username = username, accType = accType, error = error, msg = msg, plot = plot, criticalList = criticalList, patientID=patientID, patientImage=patientImage)

@app.route('/newuploadpic')
def newuploadpic():
    username, password, accType = getSessionData()
    error = None
    msg = None
    if accType != 'patient':
        error = 'You are not authorized for uploading photo.'
    patientImage = downloadpic(username)
    return render_template('uploadpic.html', username = username, accType = accType, error = error, msg = msg, patientImage = patientImage)

@app.route('/adduploadpic', methods = ['GET', 'POST'])
def adduploadpic():
    username, password, accType = getSessionData()
    error = None
    msg = None

    if accType != 'patient':
        error = 'You are not authorized for uploading photo.'
    elif request.method == 'POST':
        try:
            file = request.files['image']   
            fpath = os.path.join(app.config['UPLOAD_FOLDER'], file.filename)
            file.save(fpath)
            insert_rec(username,fpath)
            msg = "Successfully uploaded your profile photo."
        except:
            error = "upload error."
    patientImage = downloadpic(username)
    return render_template('uploadpic.html', username = username, accType = accType, error = error, msg = msg, patientImage = patientImage)

def getval(k,l):
    for d in l:
        if k in d:
             return d[k]

def face_recog(img_url,username):
    KEY = '60228c30ff494e188cac455517af5a50'  # Replace with a valid Subscription Key here.
    CF.Key.set(KEY)
    BASE_URL = 'https://westcentralus.api.cognitive.microsoft.com/face/v1.0/'  # Replace with your regional Base URL
    CF.BaseUrl.set(BASE_URL)
    # img_url = join('../py/images',imgname)
    #img_url='img.png'
    result = CF.face.detect(img_url)
    y=getval('faceRectangle',result)
    t=y['top']
    l=y['left']
    h=y['height']
    w=y['width']
    r=t+w
    b=l+h
    pic=Image.open(img_url)
    pict=pic.crop((l,t,b,r))
    pictname = username+".jpeg"
    modFpath = os.path.join(app.config['MOD_FOLDER'], pictname)
    pict.save(modFpath)
    return modFpath


def insert_rec(username,img_url):
    mongodb_uri="mongodb://test:test@ds012178.mlab.com:12178/mydb"
    client= MongoClient(mongodb_uri, connectTimeoutMS=30000)
    db=client.get_database("mydb")
    ##filename=join('../py/images',imgname)
    url=face_recog(img_url,username)
    with open(url,'rb') as p:
        thedata=p.read()
    fs=gridfs.GridFS(db)
    stored=fs.put(thedata,filename=username)
    pi=db.patient_info
    rec={"name":username, "age":"-1"}
    pi.insert_one(rec)

def downloadpic(repname):
    dummyImageURL = os.path.join(app.config['MOD_FOLDER'], "profile-placeholder.jpeg")
    mongodb_uri="mongodb://test:test@ds012178.mlab.com:12178/mydb"
    client= MongoClient(mongodb_uri, connectTimeoutMS=30000)
    db=client.get_database("mydb")
    outfilename = os.path.join(app.config['DOWNLOAD_FOLDER'], repname+'.jpeg')
    val=db.patient_info.find({"name":repname}).count()>0
    if val:
        fs=gridfs.GridFS(db)
        outputdata=fs.get_version(filename=repname).read()
        # outfilename=join('../py/imagesoutput/',repname)
        output=open(outfilename,'wb')
        output.write(outputdata)    
        output.close()
    else:
        copyfile(dummyImageURL, outfilename)
    return (IMG_URL+"/"+repname+'.jpeg?q=1280549780')

@app.route('/rec',methods=['GET','POST'])
def rec():
    if request.method=='POST':
        repname=request.form['repname']
        mongodb_uri="mongodb://test:test@ds012178.mlab.com:12178/mydb"
        client= MongoClient(mongodb_uri, connectTimeoutMS=30000)
        db=client.get_database("mydb")
        val=db.patient_info.find({"name":repname}).count()>0
        if val:
            fs=gridfs.GridFS(db)
            outputdata=fs.get_version(filename=repname).read()
            repname=repname+'.jpeg'
            # outfilename=join('../py/imagesoutput/',repname)
            outfilename = os.path.join(app.config['DOWNLOAD_FOLDER'], repname)
            output=open(outfilename,'wb')
            output.write(outputdata)    
            return render_template('success.html')
        
            output.close()
        else:
            return render_template('fail.html') 
    return render_template('test_cred.html')

@app.after_request
def add_header(response):
    # response.cache_control.no_store = True
    response.headers['Cache-Control'] = 'no-store, no-cache, must-revalidate, post-check=0, pre-check=0, max-age=0'
    response.headers['Pragma'] = 'no-cache'
    response.headers['Expires'] = '-1'
    return response

@app.route('/<cmd>')
def command(cmd=None):
    if cmd == RECORD:
        response = recordResponse()
    else:
        response = "Invalid action!"
    return response, 200, {'Content-Type': 'text/plain'}

if __name__ == "__main__":
    app.run(debug=True, port=5000)
