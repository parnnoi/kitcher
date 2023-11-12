from flask import Flask, request, jsonify, make_response, Blueprint, render_template
from flask_cors import CORS
import dbsettings
import json
import mysql.connector

login = Blueprint("login", __name__)
CORS(login)
host = dbsettings.host
user = dbsettings.user
password = dbsettings.password
db = dbsettings.db

#read user information fromm uid
@login.route("/api/login/<uid>")
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
        return make_response(jsonify({"status": "not found"}), 404)
    
#login from username and password
@login.route("/api/login", methods = ['POST'])
def newlogin():
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
        return make_response(jsonify({"status": "not found"}), 404)

#create or update cookie if user login from username and password
@login.route("/api/login/cookie", methods = ['POST'])
def createcookie():
    data = request.get_json()
    mydb = mysql.connector.connect(host=host, user=user, password=password, db=db)
    mycursor = mydb.cursor(dictionary=True)

    #find if user have the available cookie or not
    sql = "SELECT cookieid FROM logincookie WHERE uid = %s AND computerid = %s AND cookiestatus = True"
    val = (data['uid'], data['computerid'])
    mycursor.execute(sql, val)
    result = mycursor.fetchall()
    if(len(result) > 0):
        isExists = result[0]['cookieid']
    else:
        isExists = 0

    if isExists: #already have available cookie
        #update cookie
        sql = "UPDATE logincookie SET lastestLoginDate = CURRENT_TIMESTAMP, expiredDate = CURRENT_TIMESTAMP + INTERVAL 3 DAY WHERE cookieid = %s"
        val = (isExists,)
        mycursor.execute(sql, val)
        mydb.commit()

        response = {"status":"already exists"}
        return make_response(jsonify(response), 200)
    
    else: #not have available cookie
        #get max cookie number
        sql = "SELECT MAX(cookieid) as myMax FROM logincookie"
        mycursor.execute(sql)
        maxId = mycursor.fetchall()
        print(maxId)
        if(maxId[0]['myMax'] == None):
            newId = 1
        else:
            newId = int(maxId[0]['myMax']) + 1

        #create new cookie
        sql = "INSERT INTO logincookie VALUE (%s, %s, %s, %s, CURRENT_TIMESTAMP, CURRENT_TIMESTAMP + INTERVAL 3 DAY)"
        val = (newId, data['uid'], True, data['computerid'],)
        mycursor.execute(sql, val)
        mydb.commit()

        response = {"status":"complete"}
        return make_response(jsonify(response), 201)

#user use cookie for bypass login and update cookie
@login.route("/api/login/cookie/bypass", methods = ['POST'])
def loginbypass():
    data = request.get_json()
    mydb = mysql.connector.connect(host=host, user=user, password=password, db=db)
    mycursor = mydb.cursor(dictionary=True)

    #Check if status is available for bypass
    sql = "SELECT cookiestatus FROM logincookie WHERE cookieid = %s AND computerid = %s AND cookiestatus = True"
    val = (data['cookieid'], data['computerid'],)
    mycursor.execute(sql, val)
    result = mycursor.fetchall()
    if(result[0]['cookiestatus'] == None):
        isAvailable = 0
    else:
        isAvailable = result[0]['cookiestatus']

    if isAvailable: #can bypass
        #update cookie
        sql = "UPDATE logincookie SET lastestLoginDate = CURRENT_TIMESTAMP, expiredDate = CURRENT_TIMESTAMP + INTERVAL 3 DAY WHERE cookieid = %s"
        val = (data['cookieid'],)
        mycursor.execute(sql, val)
        mydb.commit()

        #get uid
        sql = "SELECT uid from logincookie WHERE cookieid = %s AND computerid = %s"
        val = (data['cookieid'], data['computerid'],)
        mycursor.execute(sql, val)
        result = mycursor.fetchall()
        mydb.commit()

        response = {"uid": result[0]['uid'], "status": "bypass"}
        return make_response(jsonify(response), 202)
    
    else: #can't bypass
        response = {"status": "can't access"}
        return make_response(jsonify(response), 406)