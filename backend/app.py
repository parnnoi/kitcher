from flask import Flask, request, jsonify, make_response, Blueprint, render_template
from flask_cors import CORS

from login import login
from register import register
from watch import watch
from category import category

import json
import mysql.connector

#to running
#--> set FLASK_ENV=development
#--> flask --debug run

app = Flask(__name__)

#use for multiple file flask running
app.register_blueprint(login)
app.register_blueprint(register)
app.register_blueprint(watch)
app.register_blueprint(category)

app.config['JSON_AS_ASCII'] = False
CORS(app)

@app.route("/")
def welcome():
    return "welcome to API"