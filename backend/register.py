from flask import Flask, request, jsonify, make_response, Blueprint, render_template
from flask_cors import CORS
import dbsettings
import json
import mysql.connector

register = Blueprint("register", __name__)
CORS(register)
host = dbsettings.host
user = dbsettings.user
password = dbsettings.password
db = dbsettings.db

#create new user to userinfo and login
@register.route("/api/register", methods = ['POST'])
def createuser():
    data = request.get_json()
    mydb = mysql.connector.connect(host=host, user=user, password=password, db=db)
    mycursor = mydb.cursor(dictionary=True)

    #check if user is exist or not
    sql = "SELECT COUNT(uid) AS myCount FROM login WHERE BINARY username = %s"
    val = (data['username'],)
    mycursor.execute(sql, val)
    numUser = mycursor.fetchall()

    if(int(numUser[0]['myCount']) == 0): #can add to new user
        #get max uid from userinfo
        sql = "SELECT MAX(uid) AS myMax FROM userinfo"
        mycursor.execute(sql)
        maxUid = mycursor.fetchall()
        if(int(maxUid[0]['myMax']) == None):
            newUID = 1
        else:
            newUID = int(maxUid[0]['myMax']) + 1

        #add user to userinfo
        sql = "INSERT INTO userinfo VALUES (%s, %s, %s, %s, %s, CURRENT_TIMESTAMP)"
        val = (newUID, data['fName'], data['lName'], data['email'], data['telno'],)
        mycursor.execute(sql, val)

        #add user to login
        sql = "INSERT INTO login VALUES (%s, %s, %s, %s)"
        val = (newUID, data['username'], data['password'], data['role'],)
        mycursor.execute(sql, val)
        mydb.commit()
        return make_response(jsonify({"status": "succuess"}), 200)

    else: #user is already exists
        return make_response(jsonify({"status": "exists"}), 200)

#check user is exist or not, from username
@register.route("/api/register/<username>")
def verify(username): 
    mydb = mysql.connector.connect(host=host, user=user, password=password, db=db)
    mycursor = mydb.cursor(dictionary=True)

    #check if user is exist or not
    sql = "SELECT COUNT(uid) AS myCount FROM login WHERE BINARY username = %s"
    val = (username,)
    mycursor.execute(sql, val)
    numUser = mycursor.fetchall()

    if(numUser[0]['myCount'] > 0): #user is exists
        return make_response(jsonify({"status": "exists"}), 200)

    else: #user is not exists
        return make_response(jsonify({"status": "not exists"}), 200)