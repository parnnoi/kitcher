from flask import Flask, request, jsonify, make_response, Blueprint, render_template
from flask_cors import CORS
import dbsettings
import json
import mysql.connector
import datetime

#set " set FLASK_ENV=development "
#set " $env:FLASK_APP = "example.py" "
#run " flask --debug run "

public = Blueprint("public", __name__)
CORS(public)
host = dbsettings.host
user = dbsettings.user
password = dbsettings.password
db = dbsettings.db

def public_exists(menuid, mycursor):
    # Check if the ingredient with the same name already exists for the given menuid
    query = "SELECT COUNT(*) AS cou FROM public WHERE menuid = %s"
    val = (menuid,)
    mycursor.execute(query, val)
    count = mycursor.fetchone()['cou']
    return count > 0

@public.route("/api/menu/public", methods = ['POST'])
def CreatePublic():
    data = request.get_json()
    mydb = mysql.connector.connect(host=host, user=user, password=password, db=db)
    mycursor = mydb.cursor(dictionary=True) #return ข้อมูลแบบ dictionary ซึ่งมันเหมาะกับการส่งออกแบบ JSON อยู่แล้ว
    
    #Count createMenu by UID
    sql = "INSERT INTO public (publicid, menuid, norder, publicStatus, updateDate) VALUES (%s, %s, %s, %s, CURRENT_TIMESTAMP)"

    if public_exists(data['menuid'], mycursor):
        return make_response(jsonify({"message": "Error fetching pubblicid"}), 404)

    else:

        #dynamic generate
        publicid_query = "SELECT COALESCE(MAX(publicid), 0) + 1 AS count FROM public"
        mycursor.execute(publicid_query)
        publicid = mycursor.fetchall()[0]['count']

        norder_query = "SELECT MAX(norder) as countnor FROM public WHERE publicid = %s"
        val = (publicid,)
        mycursor.execute(norder_query, val)
        norder_result = mycursor.fetchone()

        if norder_result['countnor'] is not None:
            next_norder = norder_result['countnor'] + 1
        else:# If there are no existing records for this publicid, start with 1
            next_norder = 1

        val = (publicid, data['menuid'], next_norder,  data['publicStatus'],)

        mycursor.execute(sql, val)
        mydb.commit()

    # Fetch the generated menuid
    return_menuid_query = "SELECT MAX(publicid) AS publicid FROM public WHERE menuid = %s"
    mycursor.execute(return_menuid_query, (data['menuid'],))
    returned_menuid = mycursor.fetchone()

    if returned_menuid:
        return make_response(jsonify({"message": "Public setting successfully", "Publicid": returned_menuid['publicid']}), 200)
    else:
        return make_response(jsonify({"message": "Error fetching pubblicid"}), 500)
    


def update_public(data):
    try:
        mydb = mysql.connector.connect(host=host, user=user, password=password, database=db)
        mycursor = mydb.cursor()
        
        update_query = "UPDATE public SET publicStatus = %s WHERE menuid = %s"
        
        update_data = (data['publicStatus'], data['menuid'],)
        mycursor.execute(update_query, update_data)
            
        # Fetch the results after executing all queries
        mydb.commit()

        return {"message": "Detail updated successfully"}

    except mysql.connector.Error as err:
        return {"error": f"MySQL Error: {err}"}, 500

@public.route("/api/menu/public/update", methods = ['PUT'])
def route_update_public():
    data = request.get_json()
    data = request.get_data
    result = update_public(data)
    return make_response(jsonify(result), 200)