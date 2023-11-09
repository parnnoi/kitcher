from flask import Flask, request, jsonify, make_response, Blueprint, render_template
from flask_cors import CORS
import json
import mysql.connector

#set " set FLASK_ENV=development "
#set " $env:FLASK_APP = "example.py" "
#run " flask --debug run "
second = Blueprint("second", __name__)
#second.config['JSON_AS_ASCII'] = False
CORS(second)
host = "localhost"
user = "root"
password = ""
db = "kitcher"

@second.route("/api/attractions")
def read():
    #data = request.get_json()
    mydb = mysql.connector.connect(host=host, user=user, password=password, db=db)
    mycursor = mydb.cursor(dictionary=True) #return ข้อมูลแบบ dictionary ซึ่งมันเหมาะกับการส่งออกแบบ JSON อยู่แล้ว
    return "test return"
