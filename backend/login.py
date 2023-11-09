from flask import Flask, request, jsonify, make_response
from flask_cors import CORS
import json
import mysql.connector

#set " set FLASK_ENV=development "
#set " $env:FLASK_APP = "example.py" "
#run " flask --debug run "

app = Flask(__name__)
app.config['JSON_AS_ASCII'] = False
CORS(app)
host = "localhost"
user = "root"
password = ""
db = "kitcher"

@app.route("/api/login/<uid>")
def readuserinfo(uid):
    mydb = mysql.connector.connect(host=host, user=user, password=password, db=db)
    mycursor = mydb.cursor(dictionary=True)

    #check if user is exist or not
    sql = "SELECT uid, fName, lName, email, telno FROM userinfo WHERE uid = %s"
    val = (uid,)
    mycursor.execute(sql, val)
    userInfo = mycursor.fetchall()

    if(int(len(userInfo)) > 0): #can add to new user
        userInfo[0]['status'] = "found"
        return make_response(jsonify(userInfo), 200)

    else: #user is already exists
        return make_response(jsonify({"status": "not found"}), 200)
    
@app.route("/api/login", methods = ['POST'])
def login():
    data = request.get_json()
    mydb = mysql.connector.connect(host=host, user=user, password=password, db=db)
    mycursor = mydb.cursor(dictionary=True)

    #check if user is exist or not
    sql = "SELECT uid FROM login WHERE BINARY username = %s AND BINARY password = %s"
    val = (data['username'], data['password'],)
    mycursor.execute(sql, val)
    userInfo = mycursor.fetchall()

    if(int(len(userInfo)) > 0): #found user
        userInfo[0]['status'] = "found"
        return make_response(jsonify(userInfo), 200)

    else: #user is not found
        return make_response(jsonify({"status": "not found"}), 200)
    
@app.route("/api/login/cookie", methods = ['POST'])
def createcookie():
    data = request.get_json()
    mydb = mysql.connector.connect(host=host, user=user, password=password, db=db)
    mycursor = mydb.cursor(dictionary=True)

    sql = "SELECT count(*) as myCount FROM logincookie WHERE uid = %s AND cookiestatus = True"
    val = (data['uid'],)
    mycursor.execute(sql, val)
    result = mycursor.fetchall()
    isExists = result[0]['myCount']

    if isExists:
        #update cookie
        sql = "UPDATE logincookie SET lastestLoginDate = CURRENT_TIMESTAMP, expiredDate = CURRENT_TIMESTAMP + INTERVAL 3 DAY"
        mycursor.execute(sql, val)
        mydb.commit()

        response = {"status":"already exists"}
        return make_response(jsonify(response), 200)
    else:
        #get max cookie number
        sql = "SELECT MAX(cookieid) as myMax FROM logincookie"
        mycursor.execute(sql)
        maxId = mycursor.fetchall()
        print(maxId)
        if(maxId[0]['myMax'] == None):
            maxId[0]['myMax'] = 0
        newId = int(maxId[0]['myMax']) + 1

        #if cookie status are expired
        sql = "INSERT INTO logincookie VALUE (%s, %s, %s, %s, CURRENT_TIMESTAMP, CURRENT_TIMESTAMP + INTERVAL 3 DAY)"
        val = (newId, data['uid'], True, data['computerid'],)
        mycursor.execute(sql, val)
        mydb.commit()

        response = {"status":"complete"}
        return make_response(jsonify(response), 200)
    
@app.route("/api/login/cookie/bypass", methods = ['POST'])
def loginbypass():
    data = request.get_json()
    mydb = mysql.connector.connect(host=host, user=user, password=password, db=db)
    mycursor = mydb.cursor(dictionary=True)

    sql = "SELECT count(*) as myCount FROM logincookie WHERE uid = %s AND cookiestatus = True"
    val = (data['uid'],)
    mycursor.execute(sql, val)
    result = mycursor.fetchall()
    isExists = result[0]['myCount']

    if isExists:
        #update expired date
        sql = "UPDATE logincookie SET lastestLoginDate = CURRENT_TIMESTAMP, expiredDate = CURRENT_TIMESTAMP + INTERVAL 3 DAY"
        mycursor.execute(sql, val)

        #get uid
        sql = "SELECT uid from logincookie WHERE cookieid = %s AND computerid = %s"
        val = (data['cookieid'], data['computerid'],)
        mycursor.execute(sql, val)
        result = mycursor.fetchall()
        mydb.commit()

        response = {"uid": result[0]['uid'], "status": "bypass"}
        return make_response(jsonify(response), 200)
    else:
        response = {"status": "can't access"}
        return make_response(jsonify(response), 200)