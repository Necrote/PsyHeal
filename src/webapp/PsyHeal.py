from flask import Flask, session, flash, redirect, render_template, jsonify, request, url_for
import sqlite3 as sql
import json

app = Flask(__name__)
app.secret_key = '\x03\x04\xec\x18"\x06\xfd]\x0cK\xf1\x97\xe0y\x1ba\xfa\xb8-\xdb\xdb\xa8\x96%'
typeList = ["admin","doctor","patient"]
dbPath = "src/database/"
textInputPath = "input/textinput/"

def getSessionData():
    if 'username' in session:
        return session['username'], session['password'], session['accType']
    else:
        return None, None, None

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

@app.route('/newentry')
def newentry():
    username, password, accType = getSessionData()
    error = None
    msg = None
    if accType != 'patient':
        error = 'You are not authorized for adding text entries.'
    return render_template('addentry.html', username = username, accType = accType, error = error, msg = msg)

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
            with open(textInputPath+username+"_output"+str(ctr)+".txt", "w+") as entryFile:
                entryFile.write(entry)
            with open(textInputPath+'txtEntryCounter.json', 'w+') as fp:
                json.dump(ctrs, fp)
            msg = "entry added."
        except:
            error = "internal write error."
    return render_template('addentry.html', username = username, accType = accType, error = error, msg = msg)

if __name__ == "__main__":
    app.run(debug=True, port=5000)
