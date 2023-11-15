from flask import Flask, request, jsonify, make_response, Blueprint, render_template
from flask_cors import CORS
import dbsettings
import json
import mysql.connector

#64070501095 – Modified 2023-11-14 – edit db format
search = Blueprint("search", __name__)
CORS(search)
host = dbsettings.host
user = dbsettings.user
password = dbsettings.password
db = dbsettings.db

#64070501095 – Modified 2023-11-14 – edit change data format about datetime
@search.route("/api/menu/all")
def SearchALL():
    #connect to database
    mydb = mysql.connector.connect(host=host, user=user, password=password, db=db)
    mycursor = mydb.cursor(dictionary=True)
    
    #get ALL recipe
    sql = "SELECT COUNT(*) AS myCount FROM menu"
    mycursor.execute(sql)
    result = mycursor.fetchall()
    isExists  = result[0]['myCount']
    
    if(isExists): #Have recipe in database
        sql = "SELECT * FROM menu"
        mycursor.execute(sql)
        result = mycursor.fetchall()
        
        for i in range(isExists):
            result[i]['createdDate'] = str(result[i]['createdDate'])
            result[i]['estimateTime'] = str(result[i]['estimateTime'])
        return make_response(jsonify(result), 200)
    
    else: #don't have recipe in database
        return make_response(jsonify({"status": "not found"}), 404)

#64070501095 – Modified 2023-11-14 – edit condition and change data format about datetime
@search.route("/api/menu/name/<menuName>")
def SearchByName(menuName):
    #connect to database
    mydb = mysql.connector.connect(host=host, user=user, password=password, db=db)
    mycursor = mydb.cursor(dictionary=True)
    
    #get recipe by name
    sql = "SELECT COUNT(*) AS myCount FROM menu WHERE menuName LIKE %s"
    menuName = '%' + menuName + '%'
    val = (menuName,)
    mycursor.execute(sql, val)
    result = mycursor.fetchall()
    isExists  = result[0]['myCount']

    if(isExists): #Have recipe in database
        sql = "SELECT *FROM menu WHERE menuName LIKE %s"
        val = (menuName,)
        mycursor.execute(sql, val)
        result = mycursor.fetchall()

        for i in range(isExists):
            result[i]['createdDate'] = str(result[i]['createdDate'])
            result[i]['estimateTime'] = str(result[i]['estimateTime'])
        return make_response(jsonify(result), 200)

    else: #don't have recipe in database
        return make_response(jsonify({"status": "not found"}), 404)
    
#64070501095 – Modified 2023-11-14 – edit change data format about datetime
@search.route("/api/menu/category/<categoryid>")
def SearchBycategory(categoryid):
    #connect to database
    mydb = mysql.connector.connect(host=host, user=user, password=password, db=db)
    mycursor = mydb.cursor(dictionary=True)
    
    #get recipe by category
    sql = "SELECT COUNT(*) AS myCount FROM menu WHERE categoryid = %s"
    val = (categoryid,)
    mycursor.execute(sql,val)
    result = mycursor.fetchall()
    isExists  = result[0]['myCount']
    
    if(isExists): #Have recipe in database
        sql = "SELECT * FROM menu WHERE categoryid = %s"
        val = (categoryid,)
        mycursor.execute(sql,val)
        result = mycursor.fetchall()

        for i in range(isExists):
            result[i]['createdDate'] = str(result[i]['createdDate'])
            result[i]['estimateTime'] = str(result[i]['estimateTime'])
        return make_response(jsonify(result), 200)

    else: #don't have recipe in database
        return make_response(jsonify({"status": "not found"}), 404)

#64070501095 – Modified 2023-11-14 – edit change data format about datetime
@search.route("/api/menu/favorite/<uid>")
def SearchByfavorite(uid):
    #connect to database
    mydb = mysql.connector.connect(host=host, user=user, password=password, db=db)
    mycursor = mydb.cursor(dictionary=True)
    
    #get recipe by category
    sql = "SELECT COUNT(*) AS myCount FROM menu m, favorite f WHERE f.favoriteStatus = True AND m.menuid = f.menuid AND f.uid = %s"
    val = (uid,)
    mycursor.execute(sql,val)
    result = mycursor.fetchall()
    isExists  = result[0]['myCount']
    
    if(isExists): #Have recipe in database
        sql = "SELECT m.*, f.favoriteid, f.favoriteStatus, f.favoriteDate FROM menu m, favorite f WHERE f.favoriteStatus = True AND m.menuid = f.menuid AND f.uid = %s"
        val = (uid,)
        mycursor.execute(sql,val)
        result = mycursor.fetchall()
    
        for i in range(isExists):
            result[i]['createdDate'] = str(result[i]['createdDate'])
            result[i]['estimateTime'] = str(result[i]['estimateTime'])
        return make_response(jsonify(result), 200)

    else: #don't have recipe in database
        return make_response(jsonify({"status": "not found"}), 404)

#64070501095 – Modified 2023-11-14 – edit change data format about datetime
@search.route("/api/menu/creater/<uid>")
def SearchBycreater(uid):
    #connect to database
    mydb = mysql.connector.connect(host=host, user=user, password=password, db=db)
    mycursor = mydb.cursor(dictionary=True)
    
    #get recipe by category
    sql = "SELECT COUNT(*) AS myCount FROM menu WHERE createruid = %s"
    val = (uid,)
    mycursor.execute(sql,val)
    result = mycursor.fetchall()
    isExists  = result[0]['myCount']
    
    if(isExists): #Have recipe in database
        sql = "SELECT * FROM menu WHERE createruid = %s"
        val = (uid,)
        mycursor.execute(sql,val)
        result = mycursor.fetchall()

        for i in range(isExists):
            result[i]['createdDate'] = str(result[i]['createdDate'])
            result[i]['estimateTime'] = str(result[i]['estimateTime'])
        return make_response(jsonify(result), 200)

    else: #don't have recipe in database
        return make_response(jsonify({"status": "not found"}), 404)