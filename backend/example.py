from flask import Flask, request, jsonify, make_response
from flask_cors import CORS
import json
import mysql.connector

#set " set FLASK_ENV=development "
#set " $env:FLASK_APP = "example.py" "
#run " flask --debug run "

app = Flask(__name__)
app.config['JSON_AS_ASCII'] = False
CORS(app)
host = "localhost"
user = "root"
password = ""
db = "kitcher"

@app.route("/api/attractions")
def read():
    mydb = mysql.connector.connect(host=host, user=user, password=password, db=db)
    mycursor = mydb.cursor(dictionary=True) #return ข้อมูลแบบ dictionary ซึ่งมันเหมาะกับการส่งออกแบบ JSON อยู่แล้ว
    sql = "SELECT * FROM userinfo WHERE uid<2"
    mycursor.execute(sql)
    myresult = mycursor.fetchall()
    print(myresult)
    return make_response(jsonify(myresult), 200)

@app.route("/")
def welcome():
    return "hello, welcome to first met"
