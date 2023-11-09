from flask import Flask, request, jsonify, make_response, Blueprint, render_template
from flask_cors import CORS
import json
import mysql.connector

category = Blueprint("category", __name__)
CORS(category)
host = "localhost"
user = "root"
password = ""
db = "kitcher"

@category.route("/api/category", methods = ['POST'])
def addnewcategory():
    data = request.get_json()
    mydb = mysql.connector.connect(host=host, user=user, password=password, db=db)
    mycursor = mydb.cursor(dictionary=True)

    #get lastest categoryid
    sql = "SELECT COUNT(*) AS myCount FROM category"
    mycursor.execute(sql)
    result = mycursor.fetchall()
    newCategoryId = int(result[0]['myCount']) + 1 

    #add new category
    sql = "INSERT INTO category VALUE (%s, %s, %s)"
    val = (newCategoryId, data['categoryName'], data['detail'],)
    mycursor.execute(sql, val)
    mydb.commit()
    
    return make_response(jsonify({"status": "complete"}), 200)

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
        return make_response(jsonify({"status": "not exists"}), 200)