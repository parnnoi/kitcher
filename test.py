from flask import Flask, request, jsonify, make_response, Blueprint, render_template
from flask_cors import CORS
import dbsettings
import json
import mysql.connector
import datetime

test = Blueprint("test", __name__)
CORS(test)
host = dbsettings.host
user = dbsettings.user
password = dbsettings.password
db = dbsettings.db

@test.route("/api/admin")
def CreateFavorite():
    #connect to database
    mydb = mysql.connector.connect(host=host, user=user, password=password, db=db)
    mycursor = mydb.cursor(dictionary=True)

    sql = "INSERT INTO favorite VALUES (1, 1, 1, True, CURRENT_TIMESTAMP)"
    mycursor.execute(sql)
    mydb.commit()

    return "complete"