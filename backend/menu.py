from flask import Flask, request, jsonify, make_response, Blueprint, render_template
from flask_cors import CORS
import dbsettings
import json
import mysql.connector
import datetime

menu = Blueprint("menu", __name__)
CORS(menu)
host = dbsettings.host
user = dbsettings.user
password = dbsettings.password
db = dbsettings.db

@menu.route("/api/menu/addread")
def ReadMenu():
    mydb = mysql.connector.connect(host=host, user=user, password=password, database=db)
    mycursor = mydb.cursor(dictionary=True)  # Return data as dictionaries

    sql = "SELECT * FROM menu"

    mycursor.execute(sql)
    menu = mycursor.fetchall()

    # Convert date and estimateTime to strings
    for menu_item in menu:
        menu_item['createdDate'] = str(menu_item['createdDate'])
        menu_item['estimateTime'] = str(menu_item['estimateTime'])

    mydb.close()

    return make_response(jsonify(menu), 200)

############################################## CREATE PART ##############################################

############ Create  menu ############

@menu.route("/api/menu/add", methods = ['POST'])
def CreateMenu():
    data = request.get_json()
    mydb = mysql.connector.connect(host=host, user=user, password=password, db=db)
    mycursor = mydb.cursor(dictionary=True) #return ข้อมูลแบบ dictionary ซึ่งมันเหมาะกับการส่งออกแบบ JSON อยู่แล้ว

    #Count createMenu by UID
    sql = "INSERT INTO menu (createruid, menuid, menuName, createdDate, estimateTime, categoryid) VALUES (%s, %s, %s, CURRENT_TIMESTAMP, %s, %s)"

    #dynamic generate
    menuid_query = "SELECT COALESCE(MAX(menuid), 0) + 1 AS count FROM menu"
    mycursor.execute(menuid_query)
    menuid = mycursor.fetchall()[0]['count']

    data['createdDate'] = 'CURRENT_TIMESTAMP'

    val = (data['createruid'], menuid, data['menuName'],  data['estimateTime'], data['categoryid'])

    mycursor.execute(sql, val)
    mydb.commit()

    # Fetch the generated menuid
    return_menuid_query = "SELECT MAX(menuid) AS menuid FROM menu WHERE createruid = %s"
    mycursor.execute(return_menuid_query, (data['createruid'],))
    returned_menuid = mycursor.fetchone()

    if returned_menuid:
        return make_response(jsonify({"message": "Menu created successfully", "menuid": returned_menuid['menuid']}), 200)
    else:
        return make_response(jsonify({"message": "Error fetching menuid"}), 500)



############ Create  ingredient ############

def ingredient_exists(menuid, ingredientname, mycursor):
    # Check if the ingredient with the same name already exists for the given menuid
    query = "SELECT COUNT(*) FROM ingredient WHERE menuid = %s AND ingredientname = %s"
    val = (menuid, ingredientname,)
    mycursor.execute(query, val)
    count = mycursor.fetchone()[0]
    return count > 0

def add_ingredients(menuid, data):
    #Use for check it's can run or not
    try:
        mydb = mysql.connector.connect(host=host, user=user, password=password, database=db)
        mycursor = mydb.cursor()

        #Check menuid and ingredientname

        # Get the maximum existing ingredientid
        sql = "SELECT MAX(ingredientid) FROM ingredient"
        mycursor.execute(sql)
        result = mycursor.fetchone()
        if result[0] is not None:
            next_id = result[0] + 1
        else:
            # If there are no existing records for this menuid, start with 1
            next_id = 1

        # Get the maximum existing norder for each menu
        sql = "SELECT MAX(norder) FROM ingredient WHERE menuid = %s"
        val = (menuid,)
        mycursor.execute(sql,val)
        norder = mycursor.fetchone()
        if norder[0] is not None:
            next_norder = norder[0] + 1
        else:
            # If there are no existing records for this menuid, start with 1
            next_norder = 1

        query = "INSERT INTO ingredient (ingredientid, menuid, norder, ingredientname, quantity) VALUES (%s, %s, %s, %s, %s)"

        #Store warnings
        warnings = []

        for item in data['ingredients']:
            # Get the next available ingredientid
            ingredientname = item['ingredientname']
            quantity = item['quantity']
            
            if ingredient_exists(menuid, ingredientname, mycursor):
                # If ingredient already exists, add a warning message
                warnings.append(f"Ingredient '{ingredientname}' already exists.")

            else:
                # If ingredient doesn't exist, insert a new record
                ingredientid = next_id
                norder = next_norder

                values = (ingredientid, menuid, norder, ingredientname, quantity)
                mycursor.execute(query, values)

                next_norder += 1
                next_id += 1

        mydb.commit()

        if warnings:
            return {"message": "Ingredients added with warnings", "warnings": warnings}
        else:
            return {"message": "Ingredients added successfully"}

    except Exception as e:
        return {"error": str(e)}, 500

@menu.route("/api/menu/add/ingredient/<menuid>", methods=['POST'])
def route_add_ingredient(menuid):
   
    data = request.get_json()
    result = add_ingredients(menuid, data)
    return make_response(jsonify(result), 200)



############ Create  tool ############
#fix version 1

def tools_exists(menuid, toolname, mycursor):
    # Check if the ingredient with the same name already exists for the given menuid
    query = "SELECT COUNT(*) FROM tool WHERE menuid = %s AND toolname = %s"
    val = (menuid, toolname,)
    mycursor.execute(query, val)
    count = mycursor.fetchone()[0]
    return count > 0

def add_tools(menuid, data):
    #Use for check it's can run or not
    try:
        mydb = mysql.connector.connect(host=host, user=user, password=password, database=db)
        mycursor = mydb.cursor()

        #Check menuid and ingredientname

        # Get the maximum existing ingredientid
        sql = "SELECT MAX(toolid) FROM tool"
        mycursor.execute(sql)
        result = mycursor.fetchone()
        if result[0] is not None:
            next_id = result[0] + 1
        else:
            # If there are no existing records for this menuid, start with 1
            next_id = 1

        # Get the maximum existing norder for each menu
        norder_query = "SELECT MAX(norder) FROM tool WHERE menuid = %s"
        val = (menuid,)
        mycursor.execute(norder_query, val)
        norder = mycursor.fetchone()
        if norder[0] is not None:
            next_norder = norder[0] + 1
        else:
            # If there are no existing records for this menuid, start with 1
            next_norder = 1

        query = "INSERT INTO tool (toolid, menuid, norder, toolname) VALUES (%s, %s, %s, %s)"

        #Store warnings
        warnings = []

        for item in data['kitchentools']:
            # Get the next available ingredientid
            #quantity = item['quantity']
            
            if tools_exists(menuid, item, mycursor):
                # If ingredient already exists, add a warning message
                warnings.append(f"Tool '{item}' already exists.")

            else:
                # If ingredient doesn't exist, insert a new record
                toolid = next_id
                norder = next_norder

                values = (toolid, menuid, norder, item)
                mycursor.execute(query, values)

                next_norder += 1
                next_id += 1

        mydb.commit()

        if warnings:
            return {"message": "Tools added with warnings", "warnings": warnings}
        else:
            return {"message": "Tools added successfully"}

    except Exception as e:
        return {"error": str(e)}, 500

@menu.route("/api/menu/add/tool/<menuid>", methods=['POST'])
def route_add_tool(menuid):
   
    data = request.get_json()
    result = add_tools(menuid, data)
    return make_response(jsonify(result), 200)

#11 0
############ Create  step&process version.1 ############
##form
##Step 1 prepare ingre
##pro 1 cut ingre
##pro 2 boilling water
##Step 2 cooking
##pro 1 mix-together

# def add_step_process(menuid, data):
#     #Use for check it's can run or not
#     try:
#         mydb = mysql.connector.connect(host=host, user=user, password=password, database=db)
#         mycursor = mydb.cursor()

#         #Check menuid and ingredientname

#         # Get the maximum existing ingredientid
#         mycursor.execute("SELECT MAX(stepid) FROM step")
#         result = mycursor.fetchone()
#         if result[0] is not None:
#             next_id = result[0] + 1
#         else:
#             # If there are no existing records for this menuid, start with 1
#             next_id = 1

#         # Get the maximum existing ingredientid
#         mycursor.execute("SELECT MAX(processid) FROM process")
#         result_pro = mycursor.fetchone()
#         if result[0] is not None:
#             next_id_pro = result_pro[0] + 1
#         else:
#             # If there are no existing records for this menuid, start with 1
#             next_id_pro = 1

#         # Get the maximum existing norder for each menu
#         norder_query = "SELECT MAX(norder) FROM step WHERE menuid = %s"
#         mycursor.execute(norder_query,(menuid,))
#         norder = mycursor.fetchone()
#         if norder[0] is not None:
#             next_norder = norder[0] + 1
#         else:
#             # If there are no existing records for this menuid, start with 1
#             next_norder = 1


#         query_step = "INSERT INTO step (stepid, menuid, norder, stepname) VALUES (%s, %s, %s, %s)"
#         query_process = "INSERT INTO process (processid, stepid, menuid, norder, detail) VALUES (%s, %s, %s, %s, %s)"

#         #Store warnings
#         warnings = []

#         for step in data['steps']:
            
#             # If ingredient doesn't exist, insert a new record
#             stepid = next_id
#             norder = next_norder

#             values = (stepid, menuid, norder, step['stepname'])
#             mycursor.execute(query_step, values)

#             next_norder += 1
#             next_id += 1

#              # Get the maximum existing norder for each menu
#             norder_query_pro = "SELECT MAX(norder) FROM process WHERE stepid = %s"
#             mycursor.execute(norder_query_pro,(stepid,))
#             norder_pro = mycursor.fetchone()
#             if norder_pro[0] is not None:
#                 next_norder_pro = norder_pro[0] + 1
#             else:
#                 # If there are no existing records for this menuid, start with 1
#                 next_norder_pro = 1

#             for process in step['processes']:
                
#                 processid = next_id_pro
#                 norder_process = next_norder_pro

#                 val = (processid, stepid, menuid, norder_process, process['detail'])
#                 mycursor.execute(query_process, val)

#                 next_norder_pro += 1   
#                 next_id_pro += 1             

#         mydb.commit()

#         if warnings:
#             return {"message": "Tools added with warnings", "warnings": warnings}
#         else:
#             return {"message": "Tools added successfully"}

#     except Exception as e:
#         return {"error": str(e)}, 500

# @app.route("/api/menu/add/step/process/<menuid>", methods=['POST'])
# def route_add_process_step(menuid):
   
#     data = request.get_json()
#     result = add_step_process(menuid, data)
#     return make_response(jsonify(result), 200)

############ Create  step&process version.2 ############

def add_step_processv2(menuid, data):
    #Use for check it's can run or not
    try:
        mydb = mysql.connector.connect(host=host, user=user, password=password, database=db)
        mycursor = mydb.cursor()

        #Check menuid and ingredientname

        # Get the maximum existing ingredientid
        sql = "SELECT MAX(stepid) FROM step"
        mycursor.execute(sql)
        result = mycursor.fetchone()

        if result[0] is not None:
            next_id = result[0] + 1
        else:# If there are no existing records for this menuid, start with 1
            next_id = 1

        # Get the maximum existing norder for each menu
        norder_query = "SELECT MAX(norder) FROM step WHERE menuid = %s"
        val = (menuid,)
        mycursor.execute(norder_query, val)
        norder = mycursor.fetchone()

        if norder[0] is not None:
            next_norder = norder[0] + 1
        else:# If there are no existing records for this menuid, start with 1
            next_norder = 1

        query = "INSERT INTO step (stepid, menuid, norder, detail) VALUES (%s, %s, %s, %s)"

        #Store warnings
        warnings = []

        for item in data['stepsdetail']:
            # Get the next available ingredientid
            stepid = next_id
            norder = next_norder

            values = (stepid, menuid, norder, item)
            mycursor.execute(query, values)

            next_norder += 1
            next_id += 1

        mydb.commit()

        return {"message": "Stepdetail added successfully"}

    except Exception as e:
        return {"error": str(e)}, 500

@menu.route("/api/menu/add/stepdetail/<menuid>", methods=['POST'])
def route_add_process_step(menuid):
   
    data = request.get_json()
    result = add_step_processv2(menuid, data)
    return make_response(jsonify(result), 200)

############################################## UPDATE PART ##############################################

############ Update  menu ############

@menu.route("/api/menu/update/<menuid>", methods=['PUT'])
def UpdateMenu(menuid):
    data = request.get_json()
    mydb = mysql.connector.connect(host=host, user=user, password=password, db=db)
    mycursor = mydb.cursor(dictionary=True)

    # Check if the menuid exists
    check_menu_query = "SELECT * FROM menu WHERE menuid = %s"
    val = (menuid,)
    mycursor.execute(check_menu_query, val)
    existing_menu = mycursor.fetchone()

    if not existing_menu:
        return make_response(jsonify({"message": "Menu not found"}), 404)

    # Update menu data
    sql = "UPDATE menu SET menuName = %s, estimateTime = %s, categoryid = %s WHERE menuid = %s"
    val = (data['menuName'], data['estimateTime'], data['categoryid'], menuid)

    mycursor.execute(sql, val)
    mydb.commit()

    return make_response(jsonify({"message": "Menu updated successfully", "menuid": menuid}), 200)

############ Update  ingredient ############

        # sql = "SELECT MAX(norder) as myMax FROM... WHERE..."
        # old = 11

        # new = len(data['ingredients']) # 5

        # # get the lower
        # if(old < new):
        #     lower = old
        # else:
        #     lower = new

        # for i in range(lower)+1:
        #     update_data = (data[i]['ingredientname'], data[i]['quantity'], menuid, i)

        # if(new < old):
        #     #ลบตัวที่เกินทิ้ง จาก lower+1 -> old
        #     lower = new

        # if(new > old):
        #     #ให้ create เพิ่ม จาก lower+1 -> new
        #     lower = old

def renumber_norder_ingredient(menuid):
    try:
        mydb = mysql.connector.connect(host=host, user=user, password=password, database=db)
        mycursor = mydb.cursor()

        sql = "SELECT norder FROM ingredient WHERE menuid = %s ORDER BY norder"
        val = (menuid,)
        # Get the current norder values
        mycursor.execute(sql, val)
        current_norders = [row[0] for row in mycursor.fetchall()]

        # Update norder values to be consecutive
        for i, norder in enumerate(current_norders, start=1):
            if norder != i:
                sq_nor = "UPDATE ingredient SET norder = %s WHERE menuid = %s AND norder = %s"
                va_nor = (i, menuid, norder)
                mycursor.execute(sq_nor, va_nor )
                mydb.commit()

        return {"message": "Norder values renumbered successfully"}

    except mysql.connector.Error as err:
        return {"error": f"MySQL Error: {err}"}, 500

def update_ingredients(menuid, data):
    try:
        mydb = mysql.connector.connect(host=host, user=user, password=password, database=db)
        mycursor = mydb.cursor()
        
        update_query = "UPDATE ingredient SET ingredientname = %s, quantity = %s WHERE menuid = %s AND norder = %s"
        
        delete_query ="DELETE FROM ingredient WHERE menuid = %s AND norder = %s"

        create_query = "INSERT INTO ingredient (ingredientid, menuid, norder, ingredientname, quantity) VALUES (%s, %s, %s, %s, %s)"
        
        # Get the maximum existing ingredientid
        sql_max = "SELECT MAX(ingredientid) FROM ingredient"
        mycursor.execute(sql_max)
        result = mycursor.fetchone()
        next_id = (result[0] + 1) if result[0] is not None else 1

        # Get the count of existing ingredients for the given menuid
        sql_count = "SELECT COUNT(*) FROM ingredient WHERE menuid = %s"
        val_count = (menuid,)
        mycursor.execute(sql_count, val_count )
        old_data = mycursor.fetchone()[0]

        # Determine the number of new ingredients
        new_data = len(data['ingredients'])

        # Update existing ingredients
        for i, ingredient in enumerate(data['ingredients'], start=0):
            update_data = (ingredient['ingredientname'], ingredient['quantity'], menuid, i + 1)
            mycursor.execute(update_query, update_data)
            mydb.commit()

        if new_data < old_data:
            for i in range(new_data + 1, old_data + 1):
                # Delete redundant ingredients
                delete_date =  (menuid, i)
                mycursor.execute(delete_query, delete_date)
                mydb.commit()
        if new_data > old_data:
        # Insert new ingredients
            for i in range(old_data, new_data):
                create_data = (next_id, menuid, i + 1, data['ingredients'][i]['ingredientname'], data['ingredients'][i]['quantity'])
                mycursor.execute(create_query, create_data)
                next_id += 1  # incrementing next_id for each new ingredient
                mydb.commit()

        renumber_norder_ingredient(menuid)

        return {"message": "ingredients updated successfully"}

    except mysql.connector.Error as err:
        return {"error": f"MySQL Error: {err}"}, 500
@menu.route("/api/menu/update/ingredient/<menuid>", methods=['PUT'])
def route_update_ingredient(menuid):
    data = request.get_json()
    result = update_ingredients(menuid, data)
    return make_response(jsonify(result), 200)

############ Update  tools ############

def renumber_norder_tool(menuid):
    try:
        mydb = mysql.connector.connect(host=host, user=user, password=password, database=db)
        mycursor = mydb.cursor()

        # Get the current norder values
        sql = "SELECT norder FROM tool WHERE menuid = %s ORDER BY norder"
        val = (menuid,)
        mycursor.execute(sql, val)
        current_norders = [row[0] for row in mycursor.fetchall()]

        # Update norder values to be consecutive
        for i, norder in enumerate(current_norders, start=1):
            if norder != i:
                sq_nor = "UPDATE tool SET norder = %s WHERE menuid = %s AND norder = %s"
                va_nor = (i, menuid, norder)
                mycursor.execute(sq_nor, va_nor)
                mydb.commit()

        return {"message": "Norder values renumbered successfully"}

    except mysql.connector.Error as err:
        return {"error": f"MySQL Error: {err}"}, 500

def update_tool(menuid, data):
    try:
        mydb = mysql.connector.connect(host=host, user=user, password=password, database=db)
        mycursor = mydb.cursor()
        
        update_query = "UPDATE tool SET toolname = %s WHERE menuid = %s AND norder = %s"
        
        delete_query ="DELETE FROM tool WHERE menuid = %s AND norder = %s"

        create_query = "INSERT INTO tool (toolid, menuid, norder, toolname) VALUES (%s, %s, %s, %s)"
        
        # Get the maximum existing toolid
        sql_max = "SELECT MAX(toolid) FROM tool"
        mycursor.execute(sql_max)
        result = mycursor.fetchone()
        next_id = (result[0] + 1) if result[0] is not None else 1

        # Get the count of existing tool for the given menuid
        sql_count = "SELECT COUNT(*) FROM tool WHERE menuid = %s"
        val_count = (menuid,)
        mycursor.execute(sql_count, val_count )
        old_data = mycursor.fetchone()[0]

        # Determine the number of new tool
        new_data = len(data['toolkitchen'])

        # Update existing tool
        for i, tool in enumerate(data['toolkitchen'], start=0):
            update_data = (tool['toolname'], menuid, i + 1)
            mycursor.execute(update_query, update_data)
            mydb.commit()

        if new_data < old_data:
            for i in range(new_data + 1, old_data + 1):
                # Delete redundant tool
                delete_date =  (menuid, i)
                mycursor.execute(delete_query, delete_date)
                mydb.commit()
        if new_data > old_data:
        # Insert new tool
            for i in range(old_data, new_data):
                create_data = (next_id, menuid, i + 1, data['toolkitchen'][i]['toolname'])
                mycursor.execute(create_query, create_data)
                next_id += 1  # incrementing next_id for each new tool
                mydb.commit()

        renumber_norder_tool(menuid)

        return {"message": "Tool updated successfully"}

    except mysql.connector.Error as err:
        return {"error": f"MySQL Error: {err}"}, 500

@menu.route("/api/menu/update/tool/<menuid>", methods=['PUT'])
def route_update_tool(menuid):
    data = request.get_json()
    result = update_tool(menuid, data)
    return make_response(jsonify(result), 200)


############ Update  step-detail ############

def renumber_norder_step(menuid):
    try:
        mydb = mysql.connector.connect(host=host, user=user, password=password, database=db)
        mycursor = mydb.cursor()

        # Get the current norder values
        sql = "SELECT norder FROM step WHERE menuid = %s ORDER BY norder"
        val = (menuid,)
        mycursor.execute(sql, val)
        current_norders = [row[0] for row in mycursor.fetchall()]

        # Update norder values to be consecutive
        for i, norder in enumerate(current_norders, start=1):
            if norder != i:
                sq_nor = "UPDATE step SET norder = %s WHERE menuid = %s AND norder = %s"
                va_nor = (i, menuid, norder)
                mycursor.execute(sq_nor, va_nor)
                mydb.commit()

        return {"message": "Norder values renumbered successfully"}

    except mysql.connector.Error as err:
        return {"error": f"MySQL Error: {err}"}, 500

def update_stepdetail(menuid, data):
    try:
        mydb = mysql.connector.connect(host=host, user=user, password=password, database=db)
        mycursor = mydb.cursor()
        
        update_query = "UPDATE step SET detail = %s WHERE menuid = %s AND norder = %s"
        
        delete_query ="DELETE FROM step WHERE menuid = %s AND norder = %s"

        create_query = "INSERT INTO step (stepid, menuid, norder, detail) VALUES (%s, %s, %s, %s)"
        
        # Get the maximum existing stepid
        sql_max = "SELECT MAX(stepid) FROM step"
        mycursor.execute(sql_max)
        result = mycursor.fetchone()
        next_id = (result[0] + 1) if result[0] is not None else 1

        # Get the count of existing step for the given menuid
        sql_count = "SELECT COUNT(*) FROM step WHERE menuid = %s"
        val_count = (menuid,)
        mycursor.execute(sql_count, val_count )
        old_data = mycursor.fetchone()[0]

        # Determine the number of new step
        new_data = len(data['stepdetail'])

        # Update existing step
        for i, step in enumerate(data['stepdetail'], start=0):
            update_data = (step['detail'], menuid, i + 1)
            mycursor.execute(update_query, update_data)
            mydb.commit()

        if new_data < old_data:
            for i in range(new_data + 1, old_data + 1):
                # Delete redundant step
                delete_date =  (menuid, i)
                mycursor.execute(delete_query, delete_date)
                mydb.commit()
        if new_data > old_data:
        # Insert new step
            for i in range(old_data, new_data):
                create_data = (next_id, menuid, i + 1, data['stepdetail'][i]['detail'])
                mycursor.execute(create_query, create_data)
                next_id += 1  # incrementing next_id for each new step
                mydb.commit()

        renumber_norder_step(menuid)


        return {"message": "Detail updated successfully"}

    except mysql.connector.Error as err:
        return {"error": f"MySQL Error: {err}"}, 500

@menu.route("/api/menu/update/stepdetail/<menuid>", methods=['PUT'])
def route_update_stepdetail(menuid):
    data = request.get_json()
    result = update_stepdetail(menuid, data)
    return make_response(jsonify(result), 200)


############################################## DELETE MENU ##############################################

def delete_menu(menuid, createruid):
    try:
        mydb = mysql.connector.connect(host=host, user=user, password=password, database=db)
        mycursor = mydb.cursor()


         # Check if the menu entry exists before proceeding with deletion
        check_menu_query = "SELECT * FROM menu WHERE createruid = %s AND menuid = %s"
        mycursor.execute(check_menu_query, (createruid, menuid))
        existing_menu = mycursor.fetchone()

        if not existing_menu:
            return {"error": "Menu entry not found"}, 404


        # Delete related records from the ingredient table
        delete_ingredient_query = "DELETE FROM ingredient WHERE menuid = %s"
        mycursor.execute(delete_ingredient_query, (menuid,))

        # Delete related records from the tool table
        delete_tool_query = "DELETE FROM tool WHERE menuid = %s"
        mycursor.execute(delete_tool_query, (menuid,))

        # Delete related records from the step table
        delete_step_query = "DELETE FROM step WHERE menuid = %s"
        mycursor.execute(delete_step_query, (menuid,))

        # Delete the record from the menu table
        delete_menu_query = "DELETE FROM menu WHERE createruid = %s AND menuid = %s"
        mycursor.execute(delete_menu_query, (createruid, menuid))

        mydb.commit()

        return {"message": "Deletion successful"}

    except mysql.connector.Error as err:
        return {"error": f"MySQL Error: {err}"}, 500

@menu.route("/api/menu/<createruid>/<menuid>", methods=['DELETE'])
def route_delete_menu(menuid, createruid):
    result = delete_menu(menuid, createruid)
    return make_response(jsonify(result), 200)