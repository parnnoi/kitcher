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
# !64070501076 - Modified 2023-11-20 - change form exist from loop to tuple
def ingredient_exists_bulk(menuid, ingredient_names, mycursor):
    query = "SELECT ingredientname FROM ingredient WHERE menuid = %s AND ingredientname IN ({})".format(', '.join(['%s'] * len(ingredient_names)))
    mycursor.execute(query, [menuid] + ingredient_names)
    existing_ingredients = [row[0] for row in mycursor.fetchall()]
    return existing_ingredients


def add_ingredients(menuid, data):
    try:
        mydb = mysql.connector.connect(host=host, user=user, password=password, database=db)
        mycursor = mydb.cursor()

        mycursor.execute("SELECT MAX(ingredientid) FROM ingredient")
        result = mycursor.fetchone()
        next_id = result[0] + 1 if result and result[0] is not None else 1

        norder_query = "SELECT MAX(norder) FROM ingredient WHERE menuid = %s"
        mycursor.execute(norder_query, (menuid,))
        result = mycursor.fetchone()
        next_norder = result[0] + 1 if result and result[0] is not None else 1

        query = "INSERT INTO ingredient (ingredientid, menuid, norder, ingredientname, quantity) VALUES (%s, %s, %s, %s, %s)"

        # Store warnings
        warnings = []

        ingredient_names = [item['ingredientname'] for item in data['ingredients']]
        existing_ingredients = ingredient_exists_bulk(menuid, ingredient_names, mycursor)

        for item in data['ingredients']:
            ingredientname = item['ingredientname']
            quantity = item['quantity']

            if ingredientname in existing_ingredients:
                warnings.append(f"Ingredient '{ingredientname}' already exists. Skipped.")

            else:
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
# !64070501076 - Modified 2023-11-20 - change form exist from loop to tuple
def existing_tools(menuid, tool_names, mycursor):
    # Check if the tools with the given names already exist for the given menuid
    query = "SELECT toolname FROM tool WHERE menuid = %s AND toolname IN ({})".format(', '.join(['%s'] * len(tool_names)))
    mycursor.execute(query, [menuid] + tool_names)
    existing_tools = [row[0] for row in mycursor.fetchall()]
    return existing_tools

def add_tools(menuid, data):
    try:
        mydb = mysql.connector.connect(host=host, user=user, password=password, database=db)
        mycursor = mydb.cursor()

        # Check menuid and toolname

        # Get the maximum existing toolid
        mycursor.execute("SELECT MAX(toolid) FROM tool")
        result = mycursor.fetchone()
        next_id = result[0] + 1 if result and result[0] is not None else 1

        # Get the maximum existing norder for each menu
        norder_query = "SELECT MAX(norder) FROM tool WHERE menuid = %s"
        mycursor.execute(norder_query, (menuid,))
        result = mycursor.fetchone()
        next_norder = result[0] + 1 if result and result[0] is not None else 1

        # Store warnings
        warnings = []

        tool_names = data.get('kitchentools', [])  # Ensure the key exists and handle an empty list
        existing_tools_db = existing_tools(menuid, tool_names, mycursor)  # Call existing_tools here

        for tool in tool_names:
            # Get the next available toolid
            toolid = next_id
            norder = next_norder

            if tool in existing_tools_db:
                # If tool already exists, add a warning message
                warnings.append(f"Tool '{tool}' already exists. Skipped.")
            else:
                # If tool doesn't exist, insert a new record
                query = "INSERT INTO tool (toolid, menuid, norder, toolname) VALUES (%s, %s, %s, %s)"
                values = (toolid, menuid, norder, tool)
                mycursor.execute(query, values)

                # Increment counters for the next available toolid and norder
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


# !64070501076 - Modified 2023-11-20 - change md.commit() from all loop be out of loop
def renumber_norder_ingredient(menuid, mycursor, mydb):
    try:
        sql = "SELECT norder FROM ingredient WHERE menuid = %s ORDER BY norder"
        sq_nor = "UPDATE ingredient SET norder = %s WHERE menuid = %s AND norder = %s"
        val = (menuid,)
        mycursor.execute(sql, val)
        current_norders = [row[0] for row in mycursor.fetchall()]

        for i, norder in enumerate(current_norders, start=1):
            if norder != i:
                va_nor = (i, menuid, norder)
                mycursor.execute(sq_nor, va_nor)

        mydb.commit()

    except mysql.connector.Error as err:
        return {"error": f"MySQL Error: {err}"}, 500

def update_ingredients(menuid, data, mycursor, mydb):
    try:
        update_query = "UPDATE ingredient SET ingredientname = %s, quantity = %s WHERE menuid = %s AND norder = %s"
        delete_query = "DELETE FROM ingredient WHERE menuid = %s AND norder > %s"
        create_query = "INSERT INTO ingredient (ingredientid, menuid, norder, ingredientname, quantity) VALUES (%s, %s, %s, %s, %s)"

        # Get the maximum existing ingredientid
        sql_max = "SELECT MAX(ingredientid) FROM ingredient"
        mycursor.execute(sql_max)
        result = mycursor.fetchone()
        next_id = (result[0] + 1) if result[0] is not None else 1

        # Get the count of existing ingredients for the given menuid
        sql_count = "SELECT COUNT(*) FROM ingredient WHERE menuid = %s"
        val_count = (menuid,)
        mycursor.execute(sql_count, val_count)
        old_data = mycursor.fetchone()[0]

        # Determine the number of new ingredients
        new_data = len(data['ingredients'])

        # Update existing ingredients
        for i, ingredient in enumerate(data['ingredients'], start=1):
            update_data = (ingredient['ingredientname'], ingredient['quantity'], menuid, i)
            mycursor.execute(update_query, update_data)

        # Delete redundant ingredients
        delete_data = (menuid, new_data)
        mycursor.execute(delete_query, delete_data)

        # Insert new ingredients
        for i, ingredient in enumerate(data['ingredients'][old_data:], start=old_data):
            create_data = (next_id, menuid, i + 1, ingredient['ingredientname'], ingredient['quantity'])
            mycursor.execute(create_query, create_data)
            next_id += 1  # incrementing next_id for each new ingredient

        mydb.commit()
        renumber_norder_ingredient(menuid, mycursor, mydb)

        return {"message": "ingredients updated successfully"}

    except mysql.connector.Error as err:
        return {"error": f"MySQL Error: {err}"}, 500
    

@menu.route("/api/menu/update/ingredient/<menuid>", methods=['PUT'])
def route_update_ingredient(menuid):
    data = request.get_json()
    mydb = mysql.connector.connect(host=host, user=user, password=password, database=db)
    mycursor = mydb.cursor()
    result = update_ingredients(menuid, data, mycursor, mydb)
    return make_response(jsonify(result), 200)

############ Update  tools ############
# !64070501076 - Modified 2023-11-20 - change md.commit() from all loop be out of loop
def renumber_norder_tool(menuid, mycursor, mydb):
    try:
        # Get the current norder values
        sql = "SELECT norder FROM tool WHERE menuid = %s ORDER BY norder"
        sq_nor = "UPDATE tool SET norder = %s WHERE menuid = %s AND norder = %s"
        val = (menuid,)
        mycursor.execute(sql, val)
        current_norders = [row[0] for row in mycursor.fetchall()]

        # Update norder values to be consecutive
        for i, norder in enumerate(current_norders, start=1):
            if norder != i:       
                va_nor = (i, menuid, norder)
                mycursor.execute(sq_nor, va_nor)
                mydb.commit()

        return {"message": "Norder values renumbered successfully"}

    except mysql.connector.Error as err:
        return {"error": f"MySQL Error: {err}"}, 500

def update_tool(menuid, data, mycursor, mydb):
    try:
        update_query = "UPDATE tool SET toolname = %s WHERE menuid = %s AND norder = %s"
        delete_query = "DELETE FROM tool WHERE menuid = %s AND norder > %s"
        create_query = "INSERT INTO tool (toolid, menuid, norder, toolname) VALUES (%s, %s, %s, %s)"

        # Get the maximum existing toolid
        sql_max = "SELECT MAX(toolid) FROM tool"
        mycursor.execute(sql_max)
        result = mycursor.fetchone()
        next_id = (result[0] + 1) if result[0] is not None else 1

        # Get the count of existing tools for the given menuid
        sql_count = "SELECT COUNT(*) FROM tool WHERE menuid = %s"
        val_count = (menuid,)
        mycursor.execute(sql_count, val_count)
        old_data = mycursor.fetchone()[0]

        # Determine the number of new tools
        new_data = len(data['toolkitchen'])
        # Update existing tools
        for i, tool in enumerate(data['toolkitchen'], start=1):
            update_data = (tool['toolname'], menuid, i)
            mycursor.execute(update_query, update_data)

        # Delete redundant tools
        delete_data = (menuid, new_data)
        mycursor.execute(delete_query, delete_data)

        # Insert new tools
        for i, tool in enumerate(data['toolkitchen'][old_data:], start=old_data):
            create_data = (next_id, menuid, i + 1, tool['toolname'])
            mycursor.execute(create_query, create_data)
            next_id += 1  # incrementing next_id for each new tool

        mydb.commit()
        renumber_norder_tool(menuid, mycursor, mydb)

        return {"message": "Tools updated successfully"}

    except mysql.connector.Error as err:
        return {"error": f"MySQL Error: {err}"}, 500


@menu.route("/api/menu/update/tool/<menuid>", methods=['PUT'])
def route_update_tool(menuid):
    data = request.get_json()
    mydb = mysql.connector.connect(host=host, user=user, password=password, database=db)
    mycursor = mydb.cursor()
    result = update_tool(menuid, data, mycursor, mydb)
    mydb.close()  # Close the database connection
    return make_response(jsonify(result), 200)


############ Update  step-detail ############
# !64070501076 - Modified 2023-11-20 - change md.commit() from all loop be out of loop
def renumber_norder_step(menuid, mycursor, mydb):
    try:
        # Get the current norder values
        sql = "SELECT norder FROM step WHERE menuid = %s ORDER BY norder"
        sq_nor = "UPDATE step SET norder = %s WHERE menuid = %s AND norder = %s"
        val = (menuid,)
        mycursor.execute(sql, val)
        current_norders = [row[0] for row in mycursor.fetchall()]

        # Update norder values to be consecutive
        for i, norder in enumerate(current_norders, start=1):
            if norder != i:
                va_nor = (i, menuid, norder)
                mycursor.execute(sq_nor, va_nor)
                mydb.commit()

        return {"message": "Norder values renumbered successfully"}

    except mysql.connector.Error as err:
        return {"error": f"MySQL Error: {err}"}, 500

def update_stepdetail(menuid, data, mycursor, mydb):
    try:
        update_query = "UPDATE step SET detail = %s WHERE menuid = %s AND norder = %s"
        delete_query = "DELETE FROM step WHERE menuid = %s AND norder > %s"
        create_query = "INSERT INTO step (stepid, menuid, norder, detail) VALUES (%s, %s, %s, %s)"

        # Get the maximum existing stepid
        sql_max = "SELECT MAX(stepid) FROM step"
        mycursor.execute(sql_max)
        result = mycursor.fetchone()
        next_id = (result[0] + 1) if result[0] is not None else 1

        # Get the count of existing steps for the given menuid
        sql_count = "SELECT COUNT(*) FROM step WHERE menuid = %s"
        val_count = (menuid,)
        mycursor.execute(sql_count, val_count)
        old_data = mycursor.fetchone()[0]

        # Determine the number of new steps
        new_data = len(data['stepdetail'])
        # Update existing steps
        for i, step in enumerate(data['stepdetail'], start=1):
            update_data = (step['detail'], menuid, i)
            mycursor.execute(update_query, update_data)

        # Delete redundant steps
        delete_data = (menuid, new_data)
        mycursor.execute(delete_query, delete_data)

        # Insert new steps
        for i, step in enumerate(data['stepdetail'][old_data:], start=old_data):
            create_data = (next_id, menuid, i + 1, step['detail'])
            mycursor.execute(create_query, create_data)
            next_id += 1  # incrementing next_id for each new step

        mydb.commit()
        renumber_norder_step(menuid, mycursor, mydb)

        return {"message": "Detail updated successfully"}

    except mysql.connector.Error as err:
        return {"error": f"MySQL Error: {err}"}, 500

@menu.route("/api/menu/update/step/<menuid>", methods=['PUT'])
def route_update_stepdetail(menuid):
    data = request.get_json()
    mydb = mysql.connector.connect(host=host, user=user, password=password, database=db)
    mycursor = mydb.cursor()
    result = update_stepdetail(menuid, data, mycursor, mydb)
    mydb.close()
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