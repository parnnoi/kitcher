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
#64070501088 – Modified 2023-11-20 – edit sql and add data format about datetime
@search.route("/api/menu/all")
def SearchALL():
    #connect to database
    mydb = mysql.connector.connect(host=host, user=user, password=password, db=db)
    mycursor = mydb.cursor(dictionary=True)
    
    #get ALL recipe
    sql = "SELECT COUNT(*) AS myCount FROM menu m LEFT JOIN public p ON m.menuid = p.menuid WHERE p.publicstatus = True"
    mycursor.execute(sql)
    result = mycursor.fetchall()
    isExists  = result[0]['myCount']
    
    if(isExists): #Have recipe in database
        sql = "SELECT m.*, p.*, IF(ISNULL(f.favoriteStatus),FALSE ,TRUE) AS favoriteStatus FROM menu m LEFT JOIN public p ON m.menuid = p.menuid LEFT JOIN userinfo u ON m.createruid = u.uid LEFT JOIN favorite f ON f.menuid = m.menuid WHERE p.publicstatus = True ORDER BY avgVote DESC,menuName ASC"
        mycursor.execute(sql)
        result = mycursor.fetchall()
        
        for i in range(isExists):
            result[i]['createdDate'] = str(result[i]['createdDate'])
            result[i]['estimateTime'] = str(result[i]['estimateTime'])
            result[i]['updateDate'] = str(result[i]['updateDate'])
        return make_response(jsonify(result), 200)
    
    else: #don't have recipe in database
        return make_response(jsonify({"status": "not found"}), 404)

#64070501095 – Modified 2023-11-14 – edit condition and change data format about datetime
#64070501088 – Modified 2023-11-20 – edit sql and add data format about datetime
@search.route("/api/menu/name/<menuName>")
def SearchByName(menuName):
    #connect to database
    mydb = mysql.connector.connect(host=host, user=user, password=password, db=db)
    mycursor = mydb.cursor(dictionary=True)
    
    #get recipe by name
    sql = "SELECT COUNT(*) AS myCount FROM menu m LEFT JOIN public p ON m.menuid = p.menuid WHERE p.publicstatus = True AND m.menuName LIKE %s"
    menuName = '%' + menuName + '%'
    val = (menuName,)
    mycursor.execute(sql, val)
    result = mycursor.fetchall()
    isExists  = result[0]['myCount']

    if(isExists): #Have recipe in database
        sql = "SELECT m.*,p.*, IF(ISNULL(f.favoriteStatus),FALSE ,TRUE) AS favoriteStatus FROM menu m LEFT JOIN public p ON m.menuid = p.menuid LEFT JOIN favorite f ON f.menuid = m.menuid WHERE p.publicstatus = TRUE AND m.menuName LIKE %s ORDER BY avgVote DESC, m.menuName ASC"
        val = (menuName,)
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
#64070501088 – Modified 2023-11-20 – edit sql and add data format about datetime
@search.route("/api/menu/category/<categoryid>")
def SearchBycategory(categoryid):
    #connect to database
    mydb = mysql.connector.connect(host=host, user=user, password=password, db=db)
    mycursor = mydb.cursor(dictionary=True)
    
    #get recipe by category
    sql = "SELECT COUNT(*) AS myCount FROM menu m LEFT JOIN public p ON m.menuid = p.menuid WHERE p.publicstatus = True AND m.categoryid = %s"
    val = (categoryid,)
    mycursor.execute(sql,val)
    result = mycursor.fetchall()
    isExists  = result[0]['myCount']
    
    if(isExists): #Have recipe in database
        sql = "SELECT m.*, p.*, c.categoryName, IF(ISNULL(f.favoriteStatus),FALSE ,TRUE) AS favoriteStatus FROM menu m LEFT JOIN public p ON m.menuid = p.menuid LEFT JOIN favorite f ON f.menuid = m.menuid LEFT JOIN category c ON c.categoryid = m.categoryid WHERE p.publicstatus = TRUE AND c.categoryid = %s ORDER BY avgVote DESC, m.menuName ASC"
        val = (categoryid,)
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
#64070501088 – Modified 2023-11-20 – edit sql
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
        sql = "SELECT m.*, f.favoriteid, f.favoriteStatus, f.favoriteDate FROM menu m, favorite f WHERE f.favoriteStatus = True AND m.menuid = f.menuid AND f.uid = %s ORDER BY avgVote DESC,menuName ASC"
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
#64070501095 – Modified 2023-11-14 – edit sql and add data format about datetime 
@search.route("/api/menu/creater/<uid>") #I think this function not required but I also do it in case of use
def SearchBycreater(uid):
    #connect to database
    mydb = mysql.connector.connect(host=host, user=user, password=password, db=db)
    mycursor = mydb.cursor(dictionary=True)
    
    #get recipe by category
    sql = "SELECT COUNT(*) AS myCount FROM menu m, favorite f WHERE f.favoriteStatus = True AND m.menuid = f.menuid AND m.createruid = %s"
    val = (uid,)
    mycursor.execute(sql,val)
    result = mycursor.fetchall()
    isExists  = result[0]['myCount']
    
    if(isExists): #Have recipe in database
        sql = "SELECT m.*,p.*, IF(ISNULL(f.favoriteStatus),FALSE ,TRUE) AS favoriteStatus FROM menu m LEFT JOIN public p ON m.menuid = p.menuid LEFT JOIN favorite f ON f.menuid = m.menuid WHERE p.publicstatus = TRUE AND m.createruid = %s ORDER BY avgVote DESC, m.menuName ASC"
        val = (uid,)
        mycursor.execute(sql,val)
        result = mycursor.fetchall()

        for i in range(isExists):
            result[i]['createdDate'] = str(result[i]['createdDate'])
            result[i]['estimateTime'] = str(result[i]['estimateTime'])
            result[i]['updateDate'] = str(result[i]['updateDate'])
        return make_response(jsonify(result), 200)

    else: #don't have recipe in database
        return make_response(jsonify({"status": "not found"}), 404)