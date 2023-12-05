from flask import Flask, request, jsonify, make_response, Blueprint, render_template, Response
from flask_cors import CORS
import dbsettings
import json
import mysql.connector

watch = Blueprint("watch", __name__)
CORS(watch)
host = dbsettings.host
user = dbsettings.user
password = dbsettings.password
db = dbsettings.db

#user click to the menu
@watch.route("/api/menu/<menuid>", methods = ['POST'])
def watchmenu(menuid):
    data = request.get_json()
    mydb = mysql.connector.connect(host=host, user=user, password=password, db=db)
    mycursor = mydb.cursor(dictionary=True)

    #check if menu is exist or not
    sql = "SELECT m.createruid, p.publicstatus FROM menu m LEFT JOIN public p ON m.menuid = p.menuid WHERE m.menuid = %s"
    val = (menuid,)
    mycursor.execute(sql, val)
    menuInfo = mycursor.fetchone()
    print(menuInfo)
    isExists = menuInfo['publicstatus'] or menuInfo['createruid'] == data['uid']

    #check public status of manu
    if(isExists): #have menu in database
        #add to visitmenu
        #get max visitid
        sql = "SELECT MAX(visitid) as myMax FROM visitmenu"
        mycursor.execute(sql)
        maxId = mycursor.fetchall()
        print(maxId)
        if(maxId[0]['myMax'] == None):
            newId = 1
        else:
            newId = int(maxId[0]['myMax']) + 1

        #create new visit
        sql = "INSERT INTO visitmenu VALUES (%s, %s, %s, CURRENT_TIMESTAMP)"
        val = (newId, data['uid'], int(menuid),)
        mycursor.execute(sql, val)
        mydb.commit()

        #initial data to response
        menuData = {}

        #get menu description
        sql = "SELECT m.*, c.*, u.fName, u.lName, p.publicStatus, f.favoriteStatus  FROM menu m LEFT JOIN category c ON m.categoryid = c.categoryid LEFT JOIN userinfo u ON u.uid = m.createruid LEFT JOIN favorite f ON f.menuid = m.menuid LEFT JOIN public p ON p.menuid = m.menuid WHERE m.menuid = %s"
        val = (menuid,)
        mycursor.execute(sql, val)
        menu = mycursor.fetchall()

        #add to data
        menuData['menuDescription'] = menu[0]
        menuData['menuDescription']['createdDate'] = str(menuData['menuDescription']['createdDate'])
        menuData['menuDescription']['estimateTime'] = str(menuData['menuDescription']['estimateTime'])

        #get ingredients
        sql = "SELECT ingredientname, norder, quantity FROM ingredient WHERE menuid = %s"
        val = (menuid,)
        mycursor.execute(sql, val)
        ingredient = mycursor.fetchall()

        #add to ingredient
        menuData['ingredient'] = ingredient

        #get tool
        sql = "SELECT toolname, norder FROM tool WHERE menuid = %s"
        val = (menuid,)
        mycursor.execute(sql, val)
        tool = mycursor.fetchall()

        #add to tool
        menuData['tool'] = tool

        #find number of step
        sql = "SELECT stepname, norder FROM step WHERE menuid = %s"
        val = (menuid,)
        mycursor.execute(sql, val)
        result = mycursor.fetchall()

        # add to step
        menuData['step'] = result

        menuData['numTool'] = len(menuData['tool'])

        menuData['status'] = "found"
        json_string = json.dumps(menuData,ensure_ascii = False)
        response = Response(json_string, status=200, content_type="application/json; charset=utf-8")
        return response

    else: #menu is not exists
        if menuInfo['publicstatus'] == 0:
            return make_response(jsonify({"status": "this menu is private, access denied"}), 403)
        return make_response(jsonify({"status": "menu not found"}), 404)
    
