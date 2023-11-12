### This file is the portal for using every api and setting for database
from flask import Flask, request, jsonify, make_response, Blueprint, render_template
from flask_cors import CORS
import json
import mysql.connector

from backend.search import search
#from backend.favorite import favorite

app = Flask(__name__)

app.register_blueprint(search)
#app.register_blueprint(favorite)

app.config['JSON_AS_ASCII'] = False
CORS(app)

@app.route("/")
def welcome():
    return make_response("welcome to api", 200)