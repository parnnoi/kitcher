### This file is the portal for using every api and setting for database
from flask import Flask, request, jsonify, make_response, Blueprint, render_template
from flask_cors import CORS
import json
import mysql.connector

#import every file in project
from login import login
from register import register
from watch import watch
from category import category
#from search import search
#from recipe import recipe
#from favorite import favorite
#from publish import publish
from vote import vote

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
#app.register_blueprint(search)
#app.register_blueprint(recipe)
#app.register_blueprint(favorite)
#app.register_blueprint(publish)
app.register_blueprint(vote)

app.config['JSON_AS_ASCII'] = False
CORS(app)

@app.route("/")
def welcome():
    return make_response("welcome to api", 200)