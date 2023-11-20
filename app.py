### This file is the portal for using every api and setting for database
from flask import Flask, request, jsonify, make_response, Blueprint, render_template
from flask_cors import CORS
import json
import mysql.connector

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

### using for dev only ### 
#app.register_blueprint(test)

app.config['JSON_AS_ASCII'] = False
CORS(app)

@app.route("/")
def welcome():
    return "welcome to api"