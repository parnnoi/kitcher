### This file is the portal for using every api and setting for database
from flask import Flask, request, jsonify, make_response, Blueprint, render_template
from flask_cors import CORS
import json
import mysql.connector
import dbsettings

#import every file in project
from backend.login import login
from backend.register import register
from backend.watch import watch
from backend.category import category
from backend.search import search
from backend.menu import menu
from backend.favorite import favorite
from backend.public import public
from backend.vote import vote

### using for dev only ### 
#from backend.test import test

###########################################
#to running
#--> set FLASK_ENV=development
#--> flask --debug run
###########################################

app = Flask(__name__)

#use for multiple file flask running
app.register_blueprint(login)
app.register_blueprint(register)
app.register_blueprint(watch)
app.register_blueprint(category)
app.register_blueprint(search)
app.register_blueprint(menu)
app.register_blueprint(favorite)
app.register_blueprint(public)
app.register_blueprint(vote)

host = dbsettings.host
user = dbsettings.user
password = dbsettings.password
db = dbsettings.db

### using for dev only ### 
#app.register_blueprint(test)

app.config['JSON_AS_ASCII'] = False
CORS(app)

@app.route("/")
def welcome():
    return "welcome to api"

# @app.route("/upload", methods=["GET"])
# def upload():
#     mydb = mysql.connector.connect(host=host, user=user, password=password, db=db)
#     mycursor = mydb.cursor(dictionary=True)

#     #file = request.files['file']
#     url = "https://images.immediate.co.uk/production/volatile/sites/3/2021/09/Minecraft-Eye-of-Ender-guide-645c9c0.jpg"
#     response = requests.get(url)
#     with open("Minecraft-Eye-of-Ender-guide-645c9c0.jpg", "wb") as f:
#         f.write(response.content)

#     # with open("C:\myinfo\mario.png", 'rb') as file:
#     #     image_data = file.read()
#     sql =  "INSERT INTO image (imageid, imageinfo, linkid, linktotable) VALUES (4, %s, 123,'ExampleTable')"
#     val = (response.content,)
    
#     mycursor.execute(sql, val)
#     mydb.commit()

#     return make_response("pass", 200)

@app.route('/image/<int:id>')
def show_image(id):
    mydb = mysql.connector.connect(host=host, user=user, password=password, db=db)
    mycursor = mydb.cursor(dictionary=True)

    mycursor.execute("SELECT imageinfo FROM image WHERE imageid = %s", (id,))
    response = mycursor.fetchall()[0]['imageinfo']

    # response = requests.get(url)
    # with open("Minecraft-Eye-of-Ender-guide-645c9c0.jpg", "wb") as f:
    #     f.write(response.content)

    responses = make_response(response)
    responses.headers['Content-Type'] = 'image/jpeg'

    return responses, 200