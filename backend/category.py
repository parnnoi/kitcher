from flask import Flask, request, jsonify, make_response, Blueprint, render_template
from flask_cors import CORS
import dbsettings
import json
import mysql.connector

category = Blueprint("category", __name__)
CORS(category)
host = dbsettings.host
user = dbsettings.user
password = dbsettings.password
db = dbsettings.db

#add new category
@category.route("/api/category", methods = ['POST'])
def addnewcategory():
    data = request.get_json()
    mydb = mysql.connector.connect(host=host, user=user, password=password, db=db)
    mycursor = mydb.cursor(dictionary=True)

    #get lastest categoryid
    sql = "SELECT MAX(categoryid) AS myMax FROM category"
    mycursor.execute(sql)
    result = mycursor.fetchall()
    if(result[0]['myMax'] == None):
        newCategoryId = 1
    else:
        newCategoryId = int(result[0]['myMax']) + 1 

    #add new category
    sql = "INSERT INTO category VALUES (%s, %s, %s)"
    val = (newCategoryId, data['categoryName'], data['detail'],)
    mycursor.execute(sql, val)
    mydb.commit()
    
    return make_response(jsonify({"status": "complete"}), 201)

#change something in category by id
@category.route("/api/category/update", methods = ['PUT'])
def editcategory():
    data = request.get_json()
    mydb = mysql.connector.connect(host=host, user=user, password=password, db=db)
    mycursor = mydb.cursor(dictionary=True)

    #check category that want to update
    sql = "SELECT COUNT(*) AS myCount FROM category WHERE categoryid = %s"
    val = (data['categoryid'],)
    mycursor.execute(sql, val)
    result = mycursor.fetchall()
    isExists = result[0]['myCount']

    if(isExists):
        #update data
        sql = "UPDATE category SET detail = %s, categoryName = %s WHERE categoryid = %s"
        val = (data['detail'], data['categoryName'], data['categoryid'],)
        mycursor.execute(sql, val)
        mydb.commit()
        return make_response(jsonify({"status": "complete"}), 200)
    else:
        return make_response(jsonify({"status": "not exists"}), 404)
    
#get everything from category
@category.route("/api/category/all")
def getcategoryid():
    mydb = mysql.connector.connect(host=host, user=user, password=password, db=db)
    mycursor = mydb.cursor(dictionary=True)

    #check category have any rows?
    sql = "SELECT COUNT(*) AS myCount FROM category"
    mycursor.execute(sql)
    result = mycursor.fetchall()
    isExists = result[0]['myCount']

    if isExists:#have at least 1 row in table
        #get every category
        sql = "SELECT * from category"
        mycursor.execute(sql)
        result = mycursor.fetchall()

        result[0]['status'] = "succuss"
        return make_response(jsonify(result), 200)
    else:
        return make_response(jsonify({"status": "not found"}), 404)
