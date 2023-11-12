from flask import Flask, request, jsonify, make_response, Blueprint, render_template
from flask_cors import CORS
import json
import mysql.connector

search = Blueprint("search", __name__)
CORS(search)
host = "localhost"
user = "root"
password = ""
db = "kitcher"

@search.route("/api/recipe/all")
def SearchALL():
    #connect to database
    mydb = mysql.connector.connect(host=host, user=user, password=password, db=db)
    mycursor = mydb.cursor(dictionary=True)
    
    #get ALL recipe
    sql = "SELECT * FROM menu"
    mycursor.execute(sql)
    result = mycursor.fetchall()
    mydb.close()
    
    if(int(len(result)) > 0): #Have recipe in database
        return make_response(jsonify(result), 200)
    
    else: #don't have recipe in database
        return make_response(jsonify({"status": "not found"}), 404)

@search.route("/api/recipe/name/<menuName>")
def SearchByName(menuName):
    #connect to database
    mydb = mysql.connector.connect(host=host, user=user, password=password, db=db)
    mycursor = mydb.cursor(dictionary=True)
    
    #get recipe by name
    sql = "SELECT * FROM menu WHERE menuName LIKE %s"
    val = (menuName,)
    mycursor.execute(sql, val)
    result = mycursor.fetchall()
    mydb.close()
    
    if(int(len(result)) > 0): #Have recipe in database
        return make_response(jsonify(result), 200)

    else: #don't have recipe in database
        return make_response(jsonify({"status": "not found"}), 404)
    
@search.route("/api/recipe/category/<categoryid>")
def SearchBycategory(categoryid):
    #connect to database
    mydb = mysql.connector.connect(host=host, user=user, password=password, db=db)
    mycursor = mydb.cursor(dictionary=True)
    
    #get recipe by category
    sql = "SELECT * FROM menu WHERE categoryid = %s"
    val = (categoryid,)
    mycursor.execute(sql,val)
    result = mycursor.fetchall()
    mydb.close()
    
    if(int(len(result)) > 0): #Have recipe in database
        return make_response(jsonify(result), 200)

    else: #don't have recipe in database
        return make_response(jsonify({"status": "not found"}), 404)


@search.route("/api/recipe/favorite/<uid>")
def SearchByfavorite(uid):
    #connect to database
    mydb = mysql.connector.connect(host=host, user=user, password=password, db=db)
    mycursor = mydb.cursor(dictionary=True)
    
    #get recipe by category
    sql = "SELECT m.*, f.favoriteid, f.favoriteStatus, f.favoriteDate FROM menu m, favorite f WHERE f.favoriteStatus = True AND m.menuid = f.menuid AND f.uid = %s"
    val = (uid,)
    mycursor.execute(sql,val)
    result = mycursor.fetchall()
    mydb.close()
    
    if(int(len(result)) > 0): #Have recipe in database
        return make_response(jsonify(result), 200)

    else: #don't have recipe in database
        return make_response(jsonify({"status": "not found"}), 404)

@search.route("/api/recipe/create/<uid>")
def SearchByfavorite(uid):
    #connect to database
    mydb = mysql.connector.connect(host=host, user=user, password=password, db=db)
    mycursor = mydb.cursor(dictionary=True)
    
    #get recipe by category
    sql = "SELECT * FROM menu WHERE uid = %s"
    val = (uid,)
    mycursor.execute(sql,val)
    result = mycursor.fetchall()
    mydb.close()
    
    if(int(len(result)) > 0): #Have recipe in database
        return make_response(jsonify(result), 200)

    else: #don't have recipe in database
        return make_response(jsonify({"status": "not found"}), 404)