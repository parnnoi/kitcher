from flask import Flask, request, jsonify, make_response, Blueprint, render_template
from flask_cors import CORS
import dbsettings
import json
import mysql.connector

vote = Blueprint("vote", __name__)
CORS(vote)
host = dbsettings.host
user = dbsettings.user
password = dbsettings.password
db = dbsettings.db

#add new vote
@vote.route("/api/vote", methods = ['POST'])
def addnewvote():
    data = request.get_json()
    mydb = mysql.connector.connect(host=host, user=user, password=password, db=db)
    mycursor = mydb.cursor(dictionary=True)

    #check if you vote already, or not
    sql = "SELECT COUNT(*) AS myCount FROM vote WHERE uid = %s AND menuid = %s"
    val = (data['uid'], data['menuid'],)
    mycursor.execute(sql, val)
    result = mycursor.fetchall()
    numCount = result[0]['myCount']

    if(numCount > 0 ): #if you already vote this menu
        ### method later thiscuss
        return make_response(jsonify({"status": "you alreay voted"}), 200)
    
    else: #you never vote this menu
        #get new vote id
        sql = "SELECT MAX(voteid) AS myMax FROM vote"
        mycursor.execute(sql)
        result = mycursor.fetchall()
        if(result[0]['myMax'] == None):
            newId = 0
        else:
            newId = result[0]['myMax'] + 1

        #create new vote
        sql = "INSERT INTO vote VALUE (%s, %s, %s, %s, CURRENT_TIMESTAMP, %s)"
        val = (newId, data['uid'], data['menuid'], data['score'], data['comment'],)
        mycursor.execute(sql, val)
        mydb.commit()

        return make_response(jsonify({"status" : "complete"}), 200)


