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
rangeReadPage = 20

#64070501095 – Modified 2023-11-14 – edit change data format about datetime
#64070501088 – Modified 2023-11-20 – edit sql and add data format about datetime and change url path
@search.route("/api/menu/all/<pageNum>", methods = ['POST'])
def SearchALL(pageNum):
    #connect to database
    data = request.get_json()
    mydb = mysql.connector.connect(host=host, user=user, password=password, db=db)
    mycursor = mydb.cursor(dictionary=True)

    #Set the amount of each data set.
    pageNum = int(pageNum) * rangeReadPage
    if(pageNum == 0): #if page is 0
        return make_response(jsonify({"status": "not found"}), 404)
    
    #get ALL recipe that available
    sql = "SELECT COUNT(*) AS myCount FROM menu m LEFT JOIN public p ON m.menuid = p.menuid WHERE p.publicstatus = True LIMIT %s, %s"
    val = (pageNum - rangeReadPage, pageNum)
    mycursor.execute(sql,val)
    result = mycursor.fetchall()
    isExists  = result[0]['myCount']
    
    if(isExists): #Have recipe in database
        sql = "SELECT m.*, p.*, u.fName, u.lName, IF(ISNULL(f.favoriteStatus),FALSE ,TRUE) AS favoriteStatus, f.favoriteid FROM menu m LEFT JOIN public p ON m.menuid = p.menuid LEFT JOIN userinfo u ON m.createruid = u.uid LEFT JOIN (SELECT * FROM favorite WHERE uid = %s) f ON f.menuid = m.menuid WHERE p.publicstatus = True ORDER BY avgVote DESC,menuName ASC LIMIT %s, %s"
        val = (data["uid"], pageNum - rangeReadPage, pageNum)
        mycursor.execute(sql,val)
        result = mycursor.fetchall()
        
        for i in range(isExists):
            result[i]['createdDate'] = str(result[i]['createdDate'])
            result[i]['estimateTime'] = str(result[i]['estimateTime'])
            result[i]['updateDate'] = str(result[i]['updateDate'])
        return make_response(jsonify(result), 200)
    
    else: #don't have recipe in database
        return make_response(jsonify({"status": "not found"}), 404)

#64070501095 – Modified 2023-11-14 – edit condition and change data format about datetime
#64070501088 – Modified 2023-11-20 – edit sql and add data format about datetime and change url path
@search.route("/api/menu/name/<menuName>/<pageNum>", methods = ['POST'])
def SearchByName(menuName,pageNum):
    #connect to database
    data = request.get_json()
    mydb = mysql.connector.connect(host=host, user=user, password=password, db=db)
    mycursor = mydb.cursor(dictionary=True)
    
    #Set the amount of each data set.
    pageNum = int(pageNum) * rangeReadPage
    if(pageNum == 0): #if number of page is 0
        return make_response(jsonify({"status": "not found"}), 404)
    
    #get recipe by name
    sql = "SELECT COUNT(*) AS myCount FROM menu m LEFT JOIN public p ON m.menuid = p.menuid WHERE p.publicstatus = True AND m.menuName LIKE %s LIMIT %s, %s"
    menuName = '%' + menuName + '%'
    val = (menuName, pageNum - rangeReadPage, pageNum)
    mycursor.execute(sql, val)
    result = mycursor.fetchall()
    isExists  = result[0]['myCount']

    if(isExists): #Have recipe in database
        sql = "SELECT m.*, p.*, u.fName, u.lName, IF(ISNULL(f.favoriteStatus),FALSE ,TRUE) AS favoriteStatus, f.favoriteid FROM menu m LEFT JOIN public p ON m.menuid = p.menuid LEFT JOIN userinfo u ON m.createruid = u.uid LEFT JOIN (SELECT * FROM favorite WHERE uid = %s) f ON f.menuid = m.menuid WHERE p.publicstatus = True AND m.menuName LIKE %s ORDER BY avgVote DESC,menuName ASC LIMIT %s, %s"
        val = (data['uid'], menuName, pageNum - rangeReadPage, pageNum)
        mycursor.execute(sql, val)
        result = mycursor.fetchall()

        for i in range(isExists):
            result[i]['createdDate'] = str(result[i]['createdDate'])
            result[i]['estimateTime'] = str(result[i]['estimateTime'])
            result[i]['updateDate'] = str(result[i]['updateDate'])
        return make_response(jsonify(result), 200)

    else: #don't have recipe in database
        return make_response(jsonify({"status": "not found"}), 404)
    
#64070501095 – Modified 2023-11-14 – edit change data format about datetime
#64070501088 – Modified 2023-11-20 – edit sql and add data format about datetime and change url path
@search.route("/api/menu/category/<categoryid>/<pageNum>", methods = ['POST'])
def SearchBycategory(categoryid, pageNum):
    #connect to database
    data = request.get_json()
    mydb = mysql.connector.connect(host=host, user=user, password=password, db=db)
    mycursor = mydb.cursor(dictionary=True)
    
    #Set the amount of each data set.
    pageNum = int(pageNum) * rangeReadPage
    if(pageNum == 0): #if page is 0
        return make_response(jsonify({"status": "not found"}), 404)
    
    #get recipe by category
    sql = "SELECT COUNT(*) AS myCount FROM menu m LEFT JOIN public p ON m.menuid = p.menuid WHERE p.publicstatus = True AND m.categoryid = %s LIMIT %s, %s"
    val = (categoryid, pageNum - rangeReadPage, pageNum)
    mycursor.execute(sql,val)
    result = mycursor.fetchall()
    isExists  = result[0]['myCount']
    
    if(isExists): #Have recipe in database
        sql = "SELECT m.*, p.*, u.fName, u.lName, IF(ISNULL(f.favoriteStatus),FALSE ,TRUE) AS favoriteStatus, f.favoriteid FROM menu m LEFT JOIN public p ON m.menuid = p.menuid LEFT JOIN userinfo u ON m.createruid = u.uid LEFT JOIN (SELECT * FROM favorite WHERE uid = %s) f ON f.menuid = m.menuid WHERE p.publicstatus = True AND m.categoryid = %s ORDER BY avgVote DESC,menuName ASC LIMIT %s, %s"
        val = (data['uid'], categoryid, pageNum - rangeReadPage, pageNum)
        mycursor.execute(sql,val)
        result = mycursor.fetchall()

        for i in range(isExists):
            result[i]['createdDate'] = str(result[i]['createdDate'])
            result[i]['estimateTime'] = str(result[i]['estimateTime'])
            result[i]['updateDate'] = str(result[i]['updateDate'])
        return make_response(jsonify(result), 200)

    else: #don't have recipe in database
        return make_response(jsonify({"status": "not found"}), 404)

#64070501095 – Modified 2023-11-14 – edit change data format about datetime
#64070501088 – Modified 2023-11-20 – edit sql and change url path
@search.route("/api/menu/favorite/<pageNum>", methods = ['POST'])
def SearchByfavorite(pageNum):
    #connect to database
    data = request.get_json()
    mydb = mysql.connector.connect(host=host, user=user, password=password, db=db)
    mycursor = mydb.cursor(dictionary=True)
    
    #Set the amount of each data set.
    pageNum = int(pageNum) * rangeReadPage
    if(pageNum == 0): #if page is 0
        return make_response(jsonify({"status": "not found"}), 404)
    
    #get recipe by category
    sql = "SELECT COUNT(*) AS myCount FROM menu m LEFT JOIN favorite f ON m.menuid = f.menuid LEFT JOIN public p ON p.menuid = m.menuid WHERE p.publicstatus = True AND f.favoriteStatus = True AND f.uid = %s AND f.favoriteStatus = True LIMIT %s, %s"
    val = (data['uid'], pageNum - rangeReadPage, pageNum)
    mycursor.execute(sql,val)
    result = mycursor.fetchall()
    isExists  = result[0]['myCount']
    
    if(isExists): #Have recipe in database
        sql = "SELECT m.*, p.*, u.fName, u.lName, IF(ISNULL(f.favoriteStatus),FALSE ,TRUE) AS favoriteStatus, f.favoriteid FROM menu m LEFT JOIN public p ON m.menuid = p.menuid LEFT JOIN userinfo u ON m.createruid = u.uid LEFT JOIN (SELECT * FROM favorite WHERE uid = %s) f ON f.menuid = m.menuid WHERE p.publicstatus = True AND f.favoriteStatus = True ORDER BY avgVote DESC,menuName ASC LIMIT %s, %s"
        val = (data['uid'], pageNum - rangeReadPage, pageNum)
        mycursor.execute(sql,val)
        result = mycursor.fetchall()
    
        for i in range(isExists):
            result[i]['createdDate'] = str(result[i]['createdDate'])
            result[i]['estimateTime'] = str(result[i]['estimateTime'])
            result[i]['updateDate'] = str(result[i]['updateDate'])
        return make_response(jsonify(result), 200)

    else: #don't have recipe in database
        return make_response(jsonify({"status": "not found"}), 404)

#64070501095 – Modified 2023-11-14 – edit change data format about datetime
#64070501095 – Modified 2023-11-14 – edit sql and add data format about datetime and change url path
@search.route("/api/menu/creater/<pageNum>", methods = ['POST'])
def SearchBycreater(pageNum):
    #connect to database
    data = request.get_json()
    mydb = mysql.connector.connect(host=host, user=user, password=password, db=db)
    mycursor = mydb.cursor(dictionary=True)
    
    #Set the amount of each data set.  
    pageNum = int(pageNum) * rangeReadPage
    if(pageNum == 0): #if page is 0
        return make_response(jsonify({"status": "not found"}), 404)
    
    #get recipe by category
    sql = "SELECT COUNT(*) AS myCount FROM menu m LEFT JOIN favorite f ON m.menuid = f.menuid WHERE m.createruid = %s LIMIT %s, %s"
    val = (data['uid'], pageNum - rangeReadPage, pageNum)
    mycursor.execute(sql,val)
    result = mycursor.fetchall()
    isExists  = result[0]['myCount']
    
    if(isExists): #Have recipe in database
        sql = "SELECT m.*, p.*, u.fName, u.lName, IF(ISNULL(f.favoriteStatus),FALSE ,TRUE) AS favoriteStatus, f.favoriteid FROM menu m LEFT JOIN public p ON m.menuid = p.menuid LEFT JOIN userinfo u ON m.createruid = u.uid LEFT JOIN (SELECT * FROM favorite WHERE uid = %s) f ON f.menuid = m.menuid WHERE m.createruid = %s ORDER BY avgVote DESC,menuName ASC LIMIT %s, %s"
        val = (data['uid'], data['uid'], pageNum - rangeReadPage, pageNum)
        mycursor.execute(sql,val)
        result = mycursor.fetchall()

        for i in range(isExists):
            result[i]['createdDate'] = str(result[i]['createdDate'])
            result[i]['estimateTime'] = str(result[i]['estimateTime'])
            result[i]['updateDate'] = str(result[i]['updateDate'])
        return make_response(jsonify(result), 200)

    else: #don't have recipe in database
        return make_response(jsonify({"status": "not found"}), 404)