from flask import Flask, request, jsonify, make_response, Blueprint, render_template
from flask_cors import CORS
import dbsettings
import json
import mysql.connector
import datetime

favorite = Blueprint("favorite", __name__)
CORS(favorite)
host = dbsettings.host
user = dbsettings.user
password = dbsettings.password
db = dbsettings.db

@favorite.route("/api/menu/favorite", methods = ["POST"])
def CreateFavorite():
    #connect to database
    data = request.get_json()
    mydb = mysql.connector.connect(host=host, user=user, password=password, db=db)
    mycursor = mydb.cursor(dictionary=True)
    
    sql = "SELECT COUNT(*) as myCount FROM favorite WHERE uid = %s AND menuid = %s"
    val = (data['uid'],data['menuid'])
    mycursor.execute(sql,val)
    result = mycursor.fetchall()
    isExists  = result[0]['myCount']

    if(isExists):
        sql = "UPDATE favorite SET favoriteStatus = True WHERE uid = %s AND menuid = %s"     
        val = (data['uid'],data['menuid'])
        mycursor.execute(sql,val)    
        mydb.commit()

        # #get current favorite status
        # sql = "SELECT favoriteStatus FROM favorite WHERE uid = %s AND menuid = %s"
        # val = (data['uid'], data['menuid'],)
        # mycursor.execute(sql, val)
        # status = mycursor.fetchall()[0]['favoriteStatus']
        # newStatus = 0 if status == 1 else 1

        # #change status
        # sql = "UPDATE favorite SET favoriteStatus = %s WHERE uid = %s AND menuid = %d"
        # val = (newStatus, data['uid'],data['menuid'])
        # mycursor.execute(sql,val)    
        # mydb.commit()

        return make_response(jsonify({"status": "favoriteStatus is setted to True for all case"}), 200)
    
    else:
        #get lastest favoriteid
        sql = "SELECT MAX(favoriteid) AS myMax FROM favorite"
        mycursor.execute(sql)
        result = mycursor.fetchall()

        if(result[0]['myMax'] == None):
            newfavoriteId = 1
        else:
            newfavoriteId = int(result[0]['myMax']) + 1 
    
        #Like the recipe
        sql = "INSERT INTO favorite VALUES(%s, %s, %s, True, CURRENT_TIMESTAMP)"
        val = (newfavoriteId, data['uid'], data['menuid'],)
        mycursor.execute(sql, val)
        mydb.commit()
    
        return make_response(jsonify({"status": "Successes", "count": mycursor.rowcount}), 201)

@favorite.route("/api/menu/delete/<favoriteid>", methods = ["DELETE"])
def DeleteFavorite(favoriteid):
    #connect to database
    mydb = mysql.connector.connect(host=host, user=user, password=password, db=db)
    mycursor = mydb.cursor(dictionary=True)
    
    #Like the recipe
    sql = "UPDATE favorite SET favoriteStatus = False WHERE favoriteid = %s"
    val = (favoriteid,)
    mycursor.execute(sql, val)
    mydb.commit()
    
    return make_response(jsonify({"Message": "Successes"}), 201)
    
    