from flask import Flask, session, flash, redirect, render_template, jsonify, request, url_for

app = Flask(__name__)
app.secret_key = '\x03\x04\xec\x18"\x06\xfd]\x0cK\xf1\x97\xe0y\x1ba\xfa\xb8-\xdb\xdb\xa8\x96%'
typeList = ["Admin","Doctor","Patient"]

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
        if request.form['username'] != 'admin' or request.form['password'] != 'admin':
            error = 'Invalid username or password. Please try again!'
        else:
            session['username'] = request.form['username']
            session['password'] = request.form['password']
            session['accType'] = request.form['accType']
            flash('logged in!')
            return redirect(url_for('index'))
    return render_template('login.html',  username = username, accType = accType, error = error, typeList=typeList)

@app.route('/logout')
def logout():
   session.pop('username', None)
   session.pop('password', None)
   session.pop('accType', None)
   flash('logged out!')
   return redirect(url_for('index'))

if __name__ == "__main__":
    app.run(debug=True, port=5000)
