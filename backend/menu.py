from flask import Flask, request, jsonify, make_response, Blueprint, render_template
from flask_cors import CORS
import dbsettings
import json
import mysql.connector
import datetime
import traceback
import logging

menu = Blueprint("menu", __name__)
CORS(menu)
host = dbsettings.host
user = dbsettings.user
password = dbsettings.password
db = dbsettings.db


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


############################################## POST ##############################################

@menu.route("/api/menu/addss", methods=['POST'])
def CreateMenu():
    try:
        logging.info("CreateMenu: Start")
        data = request.get_json()
        mydb = mysql.connector.connect(host=host, user=user, password=password, db=db)
        mycursor = mydb.cursor(dictionary=True)

        # Insert menu data
        sql_menu = "INSERT INTO menu (createruid, menuid, menuName, createdDate, estimateTime, categoryid) VALUES (%s, %s, %s, CURRENT_TIMESTAMP, %s, %s)"

        # Dynamic generate
        menuid_query = "SELECT COALESCE(MAX(menuid), 0) + 1 AS count FROM menu"
        mycursor.execute(menuid_query)
        menuid = mycursor.fetchall()[0]['count']

        data['createdDate'] = 'CURRENT_TIMESTAMP'
        val_menu = (data['createruid'], menuid, data['menuName'],  data['estimateTime'], data['categoryid'])
        mycursor.execute(sql_menu, val_menu)
        mydb.commit()

        # Fetch the generated menuid
        return_menuid_query = "SELECT MAX(menuid) AS menuid FROM menu WHERE createruid = %s"
        mycursor.execute(return_menuid_query, (data['createruid'],))
        returned_menuid = mycursor.fetchone()

        if not returned_menuid:
            raise Exception("Error fetching menuid")

        # Add ingredients, tools, and steps
        add_ingredients(menuid, data, mycursor, mydb)
        add_tools(menuid, data, mycursor, mydb)
        add_steps(menuid, data, mycursor, mydb)

        return make_response(jsonify({"message": "Menu created successfully", "menuid": returned_menuid['menuid']}), 200)

    except Exception as e:
        logging.error("CreateMenu: Exception occurred")
        logging.error(traceback.format_exc())  # Log the exception traceback
        return make_response(jsonify({"error": str(e)}), 500)
    finally:
        logging.info("CreateMenu: End")

def ingredient_exists_bulk(menuid, ingredient_names, mycursor):
    query = "SELECT ingredientname FROM ingredient WHERE menuid = %s AND ingredientname IN ({})".format(', '.join(['%s'] * len(ingredient_names)))
    mycursor.execute(query, [menuid] + ingredient_names)
    existing_ingredients = [row[0] for row in mycursor.fetchall()]
    return existing_ingredients


def add_ingredients(menuid, data, mycursor, mydb):
    try:
        print(menuid)
        logging.info("add_ingredients: Start")

        mycursor.execute("SELECT MAX(ingredientid) AS maxin FROM ingredient")
        result = mycursor.fetchone()
        next_id = result['maxin'] + 1 if result and result['maxin'] is not None else 1
        print(next_id)
        norder_query = "SELECT MAX(norder) AS maxnor FROM ingredient WHERE menuid = %s"
        mycursor.execute(norder_query, (menuid,))
        result = mycursor.fetchone()
        next_norder = result['maxnor'] + 1 if result and result['maxnor'] is not None else 1
        print(next_norder)
        query = "INSERT INTO ingredient (ingredientid, menuid, norder, ingredientname, quantity) VALUES (%s, %s, %s, %s, %s)"

        # Store warnings
        warnings = []

        ingredient_names = [item['ingredientname'] for item in data['ingredients']]
        existing_ingredients = ingredient_exists_bulk(menuid, ingredient_names, mycursor)

        for item in data['ingredients']:
            print(item)
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
        logging.error("add_ingredients: Exception occurred")
        logging.error(traceback.format_exc())  # Log the exception traceback
        return {"error": str(e)}, 500
    finally:
        logging.info("add_ingredients: End")

def add_tools(menuid, data, mycursor, mydb):
    try:
        logging.info("add_tools: Start")

        # Check menuid and toolname

        # Get the maximum existing toolid
        mycursor.execute("SELECT MAX(toolid) AS maxtool FROM tool")
        result = mycursor.fetchone()
        next_id = result['maxtool'] + 1 if result and result['maxtool'] is not None else 1

        # Get the maximum existing norder for each menu
        norder_query = "SELECT MAX(norder) AS maxnor FROM tool WHERE menuid = %s"
        mycursor.execute(norder_query, (menuid,))
        result = mycursor.fetchone()
        next_norder = result['maxnor'] + 1 if result and result['maxnor'] is not None else 1

        # Store warnings
        #warnings = []

        tool_names = data.get('kitchentools', [])  # Ensure the key exists and handle an empty list
        # existing_tools_db = existing_tools(menuid, tool_names, mycursor)  # Call existing_tools here

        for tool in tool_names:
            # Get the next available toolid
            toolid = next_id
            norder = next_norder

            # if tool in existing_tools_db:
            #     # If tool already exists, add a warning message
            #     warnings.append(f"Tool '{tool}' already exists. Skipped.")
            #else:
            # If tool doesn't exist, insert a new record
            query = "INSERT INTO tool (toolid, menuid, norder, toolname) VALUES (%s, %s, %s, %s)"
            values = (toolid, menuid, norder, tool)
            mycursor.execute(query, values)

            # Increment counters for the next available toolid and norder
            next_norder += 1
            next_id += 1

        mydb.commit()

        # if warnings:
        #     return {"message": "Tools added with warnings", "warnings": warnings}
        # else:
        return {"message": "Tools added successfully"}

    except Exception as e:
        logging.error("add_tools: Exception occurred")
        logging.error(traceback.format_exc())  # Log the exception traceback
        return {"error": str(e)}, 500
    finally:
        logging.info("add_tools: End")

def add_steps(menuid, data, mycursor, mydb):
    #Use for check it's can run or not
    try:
        logging.info("add_steps: Start")

        #Check menuid and ingredientname

        # Get the maximum existing ingredientid
        sql = "SELECT MAX(stepid) AS maxstep FROM step"
        mycursor.execute(sql)
        result = mycursor.fetchone()

        if result['maxstep'] is not None:
            next_id = result['maxstep'] + 1
        else:# If there are no existing records for this menuid, start with 1
            next_id = 1

        # Get the maximum existing norder for each menu
        norder_query = "SELECT MAX(norder) AS maxnor FROM step WHERE menuid = %s"
        val = (menuid,)
        mycursor.execute(norder_query, val)
        norder = mycursor.fetchone()

        if norder['maxnor'] is not None:
            next_norder = norder['maxnor'] + 1
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
        logging.error("add_steps: Exception occurred")
        logging.error(traceback.format_exc())  # Log the exception traceback
        return {"error": str(e)}, 500
    finally:
        logging.info("add_steps: End")



############################################## UPDATE ##############################################

@menu.route("/api/menu/update/<menuid>", methods=['PUT'])
def UpdateMenu(menuid):
    data = request.get_json()
    mydb = mysql.connector.connect(host=host, user=user, password=password, db=db)
    mycursor = mydb.cursor(dictionary=True)

    # Check if the menuid exists
    check_menu_query = "SELECT * FROM menu WHERE menuid = %s"
    mycursor.execute(check_menu_query, (menuid,))
    existing_menu = mycursor.fetchone()

    if not existing_menu:
        return make_response(jsonify({"message": "Menu not found"}), 404)

    # Update menu data
    sql = "UPDATE menu SET menuName = %s, estimateTime = %s, categoryid = %s WHERE menuid = %s"
    val = (data['menuName'], data['estimateTime'], data['categoryid'], menuid)

    mycursor.execute(sql, val)
    mydb.commit()

    update_ingredients(menuid, data, mycursor, mydb)
    update_tool(menuid, data, mycursor, mydb)
    update_stepdetail(menuid, data, mycursor, mydb)

    return make_response(jsonify({"message": "Menu updated successfully", "menuid": menuid}), 200)

def renumber_norder_ingredient(menuid, mycursor, mydb):
    try:
        sql = "SELECT norder As current FROM ingredient WHERE menuid = %s ORDER BY norder"
        sq_nor = "UPDATE ingredient SET norder = %s WHERE menuid = %s AND norder = %s"
        val = (menuid,)
        mycursor.execute(sql, val)
        current_norders = [row['current'] for row in mycursor.fetchall()]

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
        sql_max = "SELECT MAX(ingredientid) AS maxin FROM ingredient"
        mycursor.execute(sql_max)
        result = mycursor.fetchone()
        next_id = (result['maxin'] + 1) if result['maxin'] is not None else 1

        # Get the count of existing ingredients for the given menuid
        sql_count = "SELECT COUNT(*) AS countin FROM ingredient WHERE menuid = %s"
        val_count = (menuid,)
        mycursor.execute(sql_count, val_count)
        old_data = mycursor.fetchone()['countin']

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


def renumber_norder_tool(menuid, mycursor, mydb):
    try:
        # Get the current norder values
        sql = "SELECT norder AS nortool FROM tool WHERE menuid = %s ORDER BY norder"
        sq_nor = "UPDATE tool SET norder = %s WHERE menuid = %s AND norder = %s"
        val = (menuid,)
        mycursor.execute(sql, val)
        current_norders = [row['nortool'] for row in mycursor.fetchall()]

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
        sql_max = "SELECT MAX(toolid) As tool FROM tool"
        mycursor.execute(sql_max)
        result = mycursor.fetchone()
        next_id = (result['tool'] + 1) if result['tool'] is not None else 1

        # Get the count of existing tools for the given menuid
        sql_count = "SELECT COUNT(*) As nortool FROM tool WHERE menuid = %s"
        val_count = (menuid,)
        mycursor.execute(sql_count, val_count)
        old_data = mycursor.fetchone()['nortool']

        # Determine the number of new tools
        new_data = len(data['kitchentools'])
        # Update existing tools
        for i, toolname in enumerate(data['kitchentools'], start=1):
            update_data = (toolname, menuid, i)
            mycursor.execute(update_query, update_data)

        # Delete redundant tools
        delete_data = (menuid, new_data)
        mycursor.execute(delete_query, delete_data)

        # Insert new tools
        for i, toolname in enumerate(data['kitchentools'][old_data:], start=old_data):
            create_data = (next_id, menuid, i + 1, toolname)
            mycursor.execute(create_query, create_data)
            next_id += 1  # incrementing next_id for each new tool

        mydb.commit()
        renumber_norder_tool(menuid, mycursor, mydb)

        return {"message": "Tools updated successfully"}

    except mysql.connector.Error as err:
        return {"error": f"MySQL Error: {err}"}, 500

    

def renumber_norder_step(menuid, mycursor, mydb):
    try:
        # Get the current norder values
        sql = "SELECT norder As stepp FROM step WHERE menuid = %s ORDER BY norder"
        sq_nor = "UPDATE step SET norder = %s WHERE menuid = %s AND norder = %s"
        val = (menuid,)
        mycursor.execute(sql, val)
        current_norders = [row['stepp'] for row in mycursor.fetchall()]

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
        sql_max = "SELECT MAX(stepid) AS maxstep FROM step"
        mycursor.execute(sql_max)
        result = mycursor.fetchone()
        next_id = (result['maxstep'] + 1) if result and result['maxstep'] is not None else 1

        # Get the count of existing steps for the given menuid
        sql_count = "SELECT COUNT(*) AS stepcount FROM step WHERE menuid = %s"
        val_count = (menuid,)
        mycursor.execute(sql_count, val_count)
        old_data = mycursor.fetchone()['stepcount']

        # Determine the number of new steps
        new_data = len(data['stepsdetail'])
        # Update existing steps
        for i, step in enumerate(data['stepsdetail'], start=1):
            update_data = (step, menuid, i)
            mycursor.execute(update_query, update_data)

        # Delete redundant steps
        delete_data = (menuid, new_data)
        mycursor.execute(delete_query, delete_data)

        # Insert new steps
        for i, step in enumerate(data['stepsdetail'][old_data:], start=old_data):
            create_data = (next_id, menuid, i + 1, step)
            mycursor.execute(create_query, create_data)
            next_id += 1  # incrementing next_id for each new step

        mydb.commit()
        renumber_norder_step(menuid, mycursor, mydb)

        return {"message": "Detail updated successfully"}

    except mysql.connector.Error as err:
        return {"error": f"MySQL Error: {err}"}, 500