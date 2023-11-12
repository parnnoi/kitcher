from flask import Flask, request, jsonify, make_response, Blueprint, render_template
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
    sql = "SELECT COUNT(*) as myCount FROM menu WHERE menuid = %s"
    val = (menuid,)
    mycursor.execute(sql, val)
    numMenu = mycursor.fetchall()
    isExists = numMenu[0]['myCount']

    if(isExists): #have menu in database
        #add to visitmenu
        #get max visitid
        sql = "SELECT MAX(visitid) as myMax FROM visitmenu WHERE menuid = %s"
        val = (menuid,)
        mycursor.execute(sql, val)
        maxId = mycursor.fetchall()
        if(int(maxId[0]['myMax']) == None):
            newId = 1
        else:
            newId = int(maxId[0]['myMax']) + 1

        #create new visit
        sql = "INSERT INTO visitmenu VALUE (%s, %s, %s, CURRENT_TIMESTAMP)"
        val = (newId, data['uid'], menuid,)
        mycursor.execute(sql, val)
        mydb.commit()

        #initial data to response
        menuData = [{}]

        #get menu description
        sql = "SELECT * FROM menu m LEFT JOIN category c ON m.categoryid = c.categoryid WHERE m.menuid = %s"
        val = (menuid,)
        mycursor.execute(sql, val)
        menu = mycursor.fetchall()

        #add to data
        menuData[0]['menuDescription'] = menu[0]
        menuData[0]['menuDescription']['createdDate'] = str(menuData[0]['menuDescription']['createdDate'])
        menuData[0]['menuDescription']['estimateTime'] = str(menuData[0]['menuDescription']['estimateTime'])

        #get ingredients
        sql = "SELECT * FROM ingredient WHERE menuid = %s"
        val = (menuid,)
        mycursor.execute(sql, val)
        ingredient = mycursor.fetchall()

        #add to ingredient
        menuData[0]['ingredient'] = ingredient

        #get tool
        sql = "SELECT * FROM tool WHERE menuid = %s"
        val = (menuid,)
        mycursor.execute(sql, val)
        tool = mycursor.fetchall()

        #add to tool
        menuData[0]['tool'] = tool

        #find number of step
        sql = "SELECT MAX(norder) as myMax FROM step WHERE menuid = %s"
        val = (menuid,)
        mycursor.execute(sql, val)
        result = mycursor.fetchall()
        numStep = int(result[0]['myMax'])
        for i in range(numStep):
            #get step id
            n = int(int(i) + int(1))
            sql = "SELECT * FROM step WHERE menuid = %s AND norder = %s"
            val = (menuid, n,)
            mycursor.execute(sql, val)
            result = mycursor.fetchall()
            stepid = int(result[0]['stepid'])

            #add to data
            stepName = 'step' + str(n)
            menuData[0][stepName] = result[0]

            #get every process by using stepid
            sql = "SELECT * FROM process WHERE stepid = %s"
            val = (stepid,)
            mycursor.execute(sql, val)
            result = mycursor.fetchall()

            #add to data
            menuData[0][stepName]['process'] = result

        menuData[0]['status'] = "found"
        return make_response(jsonify(menuData), 200)

    else: #menu is not exists
        return make_response(jsonify({"status": "not found"}), 404)
    
