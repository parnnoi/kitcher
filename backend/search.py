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
#64070501088 – Modified 2023-11-20 – edit sql and add data format about datetime and change url path
@search.route("/api/menu/all?<pageNum>")
def SearchALL(pageNum):
    #connect to database
    mydb = mysql.connector.connect(host=host, user=user, password=password, db=db)
    mycursor = mydb.cursor(dictionary=True)

    #define number of data
    pageNum = int(pageNum) * 100
    if(pageNum == 0): #if page is 0
        return make_response(jsonify({"status": "not found"}), 404)
    
    #get ALL recipe
    sql = "SELECT COUNT(*) AS myCount FROM menu m LEFT JOIN public p ON m.menuid = p.menuid WHERE p.publicstatus = True LIMIT %s, %s"
    val = (pageNum - 100, pageNum)
    mycursor.execute(sql,val)
    result = mycursor.fetchall()
    isExists  = result[0]['myCount']
    
    if(isExists): #Have recipe in database
        sql = "SELECT m.*, p.*, u.fName, u.lName, IF(ISNULL(f.favoriteStatus),FALSE ,TRUE) AS favoriteStatus FROM menu m LEFT JOIN public p ON m.menuid = p.menuid LEFT JOIN userinfo u ON m.createruid = u.uid LEFT JOIN favorite f ON f.menuid = m.menuid WHERE p.publicstatus = True ORDER BY avgVote DESC,menuName ASC LIMIT %s, %s"
        val = (pageNum - 100, pageNum)
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
@search.route("/api/menu/name/<menuName>?<pageNum>")
def SearchByName(menuName,pageNum):
    #connect to database
    mydb = mysql.connector.connect(host=host, user=user, password=password, db=db)
    mycursor = mydb.cursor(dictionary=True)
    
    #define number of data
    pageNum = int(pageNum) * 100
    if(pageNum == 0): #if number of page is 0
        return make_response(jsonify({"status": "not found"}), 404)
    
    #get recipe by name
    sql = "SELECT COUNT(*) AS myCount FROM menu m LEFT JOIN public p ON m.menuid = p.menuid WHERE p.publicstatus = True AND m.menuName LIKE %s LIMIT %s, %s"
    menuName = '%' + menuName + '%'
    val = (menuName, pageNum - 100, pageNum)
    mycursor.execute(sql, val)
    result = mycursor.fetchall()
    isExists  = result[0]['myCount']

    if(isExists): #Have recipe in database
        sql = "SELECT m.*,p.*, u.fName, u.lName, IF(ISNULL(f.favoriteStatus),FALSE ,TRUE) AS favoriteStatus FROM menu m LEFT JOIN public p ON m.menuid = p.menuid LEFT JOIN favorite f ON f.menuid = m.menuid LEFT JOIN userinfo u ON m.createruid = u.uid WHERE p.publicstatus = TRUE AND m.menuName LIKE %s ORDER BY avgVote DESC, m.menuName ASC LIMIT %s, %s"
        val = (menuName, pageNum - 100, pageNum)
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
@search.route("/api/menu/category/<categoryid>?<pageNum>")
def SearchBycategory(categoryid, pageNum):
    #connect to database
    mydb = mysql.connector.connect(host=host, user=user, password=password, db=db)
    mycursor = mydb.cursor(dictionary=True)
    
    #Set the amount of each data set.
    pageNum = int(pageNum) * 100
    if(pageNum == 0): #if page is 0
        return make_response(jsonify({"status": "not found"}), 404)
    
    #get recipe by category
    sql = "SELECT COUNT(*) AS myCount FROM menu m LEFT JOIN public p ON m.menuid = p.menuid WHERE p.publicstatus = True AND m.categoryid = %s LIMIT %s, %s"
    val = (categoryid, pageNum-100, pageNum)
    mycursor.execute(sql,val)
    result = mycursor.fetchall()
    isExists  = result[0]['myCount']
    
    if(isExists): #Have recipe in database
        sql = "SELECT m.*, p.*, c.categoryName, u.fName, u.lName, IF(ISNULL(f.favoriteStatus),FALSE ,TRUE) AS favoriteStatus FROM menu m LEFT JOIN public p ON m.menuid = p.menuid LEFT JOIN favorite f ON f.menuid = m.menuid LEFT JOIN category c ON c.categoryid = m.categoryid LEFT JOIN userinfo u ON m.createruid = u.uid WHERE p.publicstatus = TRUE AND c.categoryid = %s ORDER BY avgVote DESC, m.menuName ASC LIMIT %s, %s"
        val = (categoryid, pageNum-100, pageNum)
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
@search.route("/api/menu/favorite/<uid>?<pageNum>")
def SearchByfavorite(uid):
    #connect to database
    mydb = mysql.connector.connect(host=host, user=user, password=password, db=db)
    mycursor = mydb.cursor(dictionary=True)
    
    #Set the amount of each data set.
    pageNum = int(pageNum) * 100
    if(pageNum == 0): #if page is 0
        return make_response(jsonify({"status": "not found"}), 404)
    
    #get recipe by category
    sql = "SELECT COUNT(*) AS myCount FROM menu m, favorite f WHERE f.favoriteStatus = True AND m.menuid = f.menuid AND f.uid = %s LIMIT %s, %s"
    val = (uid, pageNum - 100, pageNum)
    mycursor.execute(sql,val)
    result = mycursor.fetchall()
    isExists  = result[0]['myCount']
    
    if(isExists): #Have recipe in database
        sql = "SELECT m.*, f.favoriteid, f.favoriteStatus, f.favoriteDate, u.fName, u.lName FROM menu m, favorite f, userinfo u WHERE m.createruid = u.uid AND f.favoriteStatus = True AND m.menuid = f.menuid AND f.uid = %s ORDER BY f.favoriteDate ASC,menuName ASC LIMIT %s, %s"
        val = (uid, pageNum - 100, pageNum)
        mycursor.execute(sql,val)
        result = mycursor.fetchall()
    
        for i in range(isExists):
            result[i]['createdDate'] = str(result[i]['createdDate'])
            result[i]['estimateTime'] = str(result[i]['estimateTime'])
        return make_response(jsonify(result), 200)

    else: #don't have recipe in database
        return make_response(jsonify({"status": "not found"}), 404)

#64070501095 – Modified 2023-11-14 – edit change data format about datetime
#64070501095 – Modified 2023-11-14 – edit sql and add data format about datetime and change url path
@search.route("/api/menu/creater/<uid>?<pageNum>")
def SearchBycreater(uid, pageNum):
    #connect to database
    mydb = mysql.connector.connect(host=host, user=user, password=password, db=db)
    mycursor = mydb.cursor(dictionary=True)
    
    #Set the amount of each data set.  
    pageNum = int(pageNum) * 100
    if(pageNum == 0): #if page is 0
        return make_response(jsonify({"status": "not found"}), 404)
    
    #get recipe by category
    sql = "SELECT COUNT(*) AS myCount FROM menu m, favorite f WHERE f.favoriteStatus = True AND m.menuid = f.menuid AND m.createruid = %s LIMIT %s, %s"
    val = (uid, pageNum - 100, pageNum)
    mycursor.execute(sql,val)
    result = mycursor.fetchall()
    isExists  = result[0]['myCount']
    
    if(isExists): #Have recipe in database
        sql = "SELECT m.*,p.*, u.fName, u.lName, IF(ISNULL(f.favoriteStatus),FALSE ,TRUE) AS favoriteStatus FROM menu m LEFT JOIN public p ON m.menuid = p.menuid LEFT JOIN favorite f ON f.menuid = m.menuid LEFT JOIN userinfo u ON m.createruid = u.uid WHERE p.publicstatus = TRUE AND m.createruid = %s ORDER BY f.favoriteDate ASC, m.menuName ASC LIMIT %s, %s"
        val = (uid, pageNum - 100, pageNum)
        mycursor.execute(sql,val)
        result = mycursor.fetchall()

        for i in range(isExists):
            result[i]['createdDate'] = str(result[i]['createdDate'])
            result[i]['estimateTime'] = str(result[i]['estimateTime'])
            result[i]['updateDate'] = str(result[i]['updateDate'])
        return make_response(jsonify(result), 200)

    else: #don't have recipe in database
        return make_response(jsonify({"status": "not found"}), 404)