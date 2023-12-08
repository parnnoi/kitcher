import 'package:flutter/material.dart';
import 'package:flutter/services.dart';
import 'package:google_fonts/google_fonts.dart';
import 'dart:convert';
import 'package:http/http.dart' as http;

class Ingredient {
  String name;
  String quantity;

  Ingredient({required this.name, required this.quantity});
}

class EditPage extends StatefulWidget {
  final Map<String, dynamic> recipe;
  final int userID;

  const EditPage({Key? key, required this.userID, required this.recipe})
      : super(key: key);

  @override
  State<EditPage> createState() => _EditPageState();
}

class _EditPageState extends State<EditPage> {
  TextEditingController menuNameController = TextEditingController();
  TextEditingController hourController = TextEditingController();
  TextEditingController minuteController = TextEditingController();
  TextEditingController secondController = TextEditingController();
  int menuID = 0;
  int selectedCategoryId = 1; // Set the default category ID
  List<Ingredient> ingredients = [];
  List<String> tools = [];
  List<String> steps = [];
  bool isLoading = true;

  String estimateTime() {
    final hour = hourController.text.padLeft(2, '0');
    final minute = minuteController.text.padLeft(2, '0');
    final second = secondController.text.padLeft(2, '0');
    return '$hour:$minute:$second';
  }

  @override
  void initState() {
    super.initState();
    fetchMenuDetails(widget.recipe['menuid']);
  }

  Future<void> fetchMenuDetails(int menuID) async {
    final Uri uri =
        Uri.parse('https://kitcherfromlocal.vercel.app/api/menu/$menuID');
    Map<String, dynamic> requestID = {'uid': widget.userID};
    final http.Response response = await http.post(
      uri,
      headers: {'Content-Type': 'application/json'},
      body: jsonEncode(requestID),
    );

    if (response.statusCode == 200) {
      final Map<String, dynamic> detail = jsonDecode(response.body);
      List<String> timeComponents =
          detail['menuDescription']['estimateTime'].split(':');
      setState(() {
        // Populate controllers with data
        menuNameController.text = detail['menuDescription']['menuName'];
        hourController.text = timeComponents[0];
        minuteController.text = timeComponents[1];
        secondController.text = timeComponents[2];
        selectedCategoryId = detail['menuDescription']['categoryid'];
        ingredients = (detail['ingredient'] as List)
            .map((ingredientMap) => Ingredient(
                  name: ingredientMap['ingredientname'],
                  quantity: ingredientMap['quantity'].toString(),
                ))
            .toList();
        tools = (detail['tool'] as List)
            .map((tool) => tool['toolname'].toString())
            .toList();
        steps = (detail['step'] as List)
            .map((step) => step['stepname'].toString())
            .toList();
        // Populate other controllers as needed
        isLoading = false;
      });
    } else if (response.statusCode == 404) {
      isLoading = false;
      // Handle not found
    } else {
      isLoading = false;
      // Handle error
    }
  }

  Future<void> updateRecipe(int menuID) async {
    final Uri uri = Uri.parse(
        'https://kitcherfromlocal.vercel.app/api/menu/update/$menuID');

    Map<String, dynamic> requestData = {
      "createruid": widget.userID,
      "menuName": menuNameController.text,
      "estimateTime": estimateTime(),
      "categoryid": selectedCategoryId,
      "ingredients": ingredients
          .map((ingredient) => {
                "ingredientname": ingredient.name,
                "quantity": int.parse(ingredient.quantity),
              })
          .toList(),
      "kitchentools": tools,
      "stepsdetail": steps,
    };
    print("$requestData");

    final http.Response response = await http.put(
      uri,
      headers: {'Content-Type': 'application/json'},
      body: jsonEncode(requestData),
    );
    print("${jsonEncode(requestData)}");
    print("${jsonEncode(response.body)}");
    if (response.statusCode == 200) {
      // Successfully created menu
      print('Menu updated successfully');
      setState(() {
        Navigator.pop(context);
      });
    } else {
      // Handle error
      print('Failed to create menu. Status code: ${response.statusCode}');
    }
  }

  void addIngredient(String name, String quantity) {
    Ingredient ingredient = Ingredient(name: name, quantity: quantity);
    setState(() {
      ingredients.add(ingredient);
    });
  }

  void removeIngredient(int index) {
    setState(() {
      ingredients.removeAt(index);
    });
  }

  void addTool(String name) {
    setState(() {
      tools.add(name);
    });
  }

  void removeTool(int index) {
    setState(() {
      tools.removeAt(index);
    });
  }

  void addStep(String name) {
    setState(() {
      steps.add(name);
    });
  }

  void removeStep(int index) {
    setState(() {
      steps.removeAt(index);
    });
  }

  @override
  Widget build(BuildContext context) {
    double screenWidth = MediaQuery.of(context).size.width;
    double screenHeight = MediaQuery.of(context).size.height;
    return Scaffold(
      appBar: AppBar(
        title: Text(
          'Menu',
          style: GoogleFonts.mali(
            fontSize: 20,
            fontWeight: FontWeight.bold,
            color: Colors.black,
          ),
        ),
        iconTheme: const IconThemeData(
          color: Colors.black, // Change the color of the back button
        ),
        backgroundColor: const Color.fromARGB(255, 255, 251, 193),
        elevation: 0,
      ),
      body: isLoading
          ? const Center(
              child: CircularProgressIndicator(
                color: Color.fromARGB(255, 255, 225, 136),
              ),
            )
          : SingleChildScrollView(
              child: Column(
                crossAxisAlignment: CrossAxisAlignment.start,
                children: [
                  Padding(
                    padding: const EdgeInsets.only(top: 10, bottom: 10),
                    child: Center(
                      child: Container(
                        decoration: BoxDecoration(
                          borderRadius: BorderRadius.circular(20),
                          color: const Color.fromARGB(255, 255, 254, 235),
                        ),
                        width: screenWidth - 32,
                        child: Column(
                          crossAxisAlignment: CrossAxisAlignment.start,
                          children: [
                            Padding(
                              padding: const EdgeInsets.all(16.0),
                              child: TextField(
                                cursorColor: Colors.black,
                                controller: menuNameController,
                                decoration: InputDecoration(
                                  focusedBorder: const UnderlineInputBorder(
                                    borderSide: BorderSide(color: Colors.black),
                                  ),
                                  labelText: 'Menu Name',
                                  labelStyle: GoogleFonts.mali(
                                    fontSize: 16,
                                    fontWeight: FontWeight.bold,
                                    color: Colors.black,
                                  ),
                                ),
                              ),
                            ),
                            Padding(
                              padding:
                                  const EdgeInsets.only(left: 16, right: 16),
                              child: Column(
                                children: [
                                  TextField(
                                    cursorColor: Colors.black,
                                    controller: hourController,
                                    keyboardType: TextInputType.number,
                                    inputFormatters: [
                                      FilteringTextInputFormatter.digitsOnly,
                                      LengthLimitingTextInputFormatter(2),
                                    ],
                                    onChanged: (value) {
                                      // Ensure the value is between 0 and 23
                                      if (value.isNotEmpty) {
                                        int intValue = int.parse(value);
                                        if (intValue < 0) {
                                          hourController.text = '00';
                                        } else if (intValue > 23) {
                                          hourController.text = '23';
                                        }
                                      }
                                    },
                                    decoration: InputDecoration(
                                      focusedBorder: const UnderlineInputBorder(
                                        borderSide:
                                            BorderSide(color: Colors.black),
                                      ),
                                      labelText: 'Hour',
                                      labelStyle: GoogleFonts.mali(
                                        fontSize: 16,
                                        fontWeight: FontWeight.bold,
                                        color: Colors.black,
                                      ),
                                    ),
                                  ),
                                  TextField(
                                    cursorColor: Colors.black,
                                    controller: minuteController,
                                    keyboardType: TextInputType.number,
                                    inputFormatters: [
                                      FilteringTextInputFormatter.digitsOnly,
                                      LengthLimitingTextInputFormatter(2),
                                    ],
                                    onChanged: (value) {
                                      // Ensure the value is between 0 and 59
                                      if (value.isNotEmpty) {
                                        int intValue = int.parse(value);
                                        if (intValue < 0) {
                                          minuteController.text = '00';
                                        } else if (intValue > 59) {
                                          minuteController.text = '59';
                                        }
                                      }
                                    },
                                    decoration: InputDecoration(
                                      labelText: 'Minute',
                                      labelStyle: GoogleFonts.mali(
                                        fontSize: 16,
                                        fontWeight: FontWeight.bold,
                                        color: Colors.black,
                                      ),
                                    ),
                                  ),
                                  TextField(
                                    cursorColor: Colors.black,
                                    controller: secondController,
                                    keyboardType: TextInputType.number,
                                    inputFormatters: [
                                      FilteringTextInputFormatter.digitsOnly,
                                      LengthLimitingTextInputFormatter(2),
                                    ],
                                    onChanged: (value) {
                                      // Ensure the value is between 0 and 59
                                      if (value.isNotEmpty) {
                                        int intValue = int.parse(value);
                                        if (intValue < 0) {
                                          secondController.text = '00';
                                        } else if (intValue > 59) {
                                          secondController.text = '59';
                                        }
                                      }
                                    },
                                    decoration: InputDecoration(
                                      focusedBorder: const UnderlineInputBorder(
                                        borderSide:
                                            BorderSide(color: Colors.black),
                                      ),
                                      labelText: 'Second',
                                      labelStyle: GoogleFonts.mali(
                                        fontSize: 16,
                                        fontWeight: FontWeight.bold,
                                        color: Colors.black,
                                      ),
                                    ),
                                  ),
                                ],
                              ),
                            ),
                            Padding(
                              padding: const EdgeInsets.all(16.0),
                              child: Row(
                                children: [
                                  Text(
                                    'Select Category : ',
                                    style: GoogleFonts.mali(
                                      fontSize: 16,
                                      fontWeight: FontWeight.bold,
                                      color: Colors.black,
                                    ),
                                  ),
                                  DropdownButton<int>(
                                    elevation: 1,
                                    alignment: Alignment.center,
                                    borderRadius: BorderRadius.circular(20),
                                    dropdownColor: const Color.fromARGB(
                                        255, 255, 254, 235),
                                    value: selectedCategoryId,
                                    onChanged: (int? value) {
                                      setState(() {
                                        selectedCategoryId = value!;
                                      });
                                    },
                                    items: [
                                      DropdownMenuItem(
                                        value: 1,
                                        child: Text(
                                          'Cake',
                                          style: GoogleFonts.mali(
                                            fontSize: 16,
                                            fontWeight: FontWeight.normal,
                                            color: Colors.black,
                                          ),
                                        ),
                                      ),
                                      DropdownMenuItem(
                                        value: 2,
                                        child: Text(
                                          'Beverage',
                                          style: GoogleFonts.mali(
                                            fontSize: 16,
                                            fontWeight: FontWeight.normal,
                                            color: Colors.black,
                                          ),
                                        ),
                                      ),
                                      DropdownMenuItem(
                                        value: 3,
                                        child: Text(
                                          'Street Food',
                                          style: GoogleFonts.mali(
                                            fontSize: 16,
                                            fontWeight: FontWeight.normal,
                                            color: Colors.black,
                                          ),
                                        ),
                                      ),
                                      DropdownMenuItem(
                                        value: 4,
                                        child: Text(
                                          'Noodle',
                                          style: GoogleFonts.mali(
                                            fontSize: 16,
                                            fontWeight: FontWeight.normal,
                                            color: Colors.black,
                                          ),
                                        ),
                                      ),
                                      DropdownMenuItem(
                                        value: 5,
                                        child: Text(
                                          'Appetizer',
                                          style: GoogleFonts.mali(
                                            fontSize: 16,
                                            fontWeight: FontWeight.normal,
                                            color: Colors.black,
                                          ),
                                        ),
                                      ),
                                      DropdownMenuItem(
                                        value: 6,
                                        child: Text(
                                          'Bread',
                                          style: GoogleFonts.mali(
                                            fontSize: 16,
                                            fontWeight: FontWeight.normal,
                                            color: Colors.black,
                                          ),
                                        ),
                                      ),
                                      DropdownMenuItem(
                                        value: 7,
                                        child: Text(
                                          'Japan Food',
                                          style: GoogleFonts.mali(
                                            fontSize: 16,
                                            fontWeight: FontWeight.normal,
                                            color: Colors.black,
                                          ),
                                        ),
                                      ),
                                      DropdownMenuItem(
                                        value: 8,
                                        child: Text(
                                          'Korea Food',
                                          style: GoogleFonts.mali(
                                            fontSize: 16,
                                            fontWeight: FontWeight.normal,
                                            color: Colors.black,
                                          ),
                                        ),
                                      ),
                                      // Add more DropdownMenuItem for other categories
                                    ],
                                  ),
                                ],
                              ),
                            ),
                            Padding(
                              padding: const EdgeInsets.only(
                                  top: 16, left: 16, right: 16),
                              child: Column(
                                crossAxisAlignment: CrossAxisAlignment.start,
                                children: [
                                  Text(
                                    'Ingredients',
                                    style: GoogleFonts.mali(
                                      fontSize: 16,
                                      fontWeight: FontWeight.bold,
                                      color: Colors.black,
                                    ),
                                  ),
                                  ElevatedButton(
                                    style: ElevatedButton.styleFrom(
                                      elevation: 0,
                                      backgroundColor: const Color.fromARGB(
                                          255,
                                          255,
                                          225,
                                          136), // Change the background color of the button
                                      foregroundColor: Colors
                                          .black, // Change the text color of the button
                                    ),
                                    onPressed: () {
                                      // Call the function to add an ingredient
                                      addIngredient('', '');
                                    },
                                    child: Text(
                                      'Add Ingredient',
                                      style: GoogleFonts.mali(
                                        fontSize: 14,
                                        fontWeight: FontWeight.bold,
                                        color: Colors.black,
                                      ),
                                    ),
                                  ),
                                ],
                              ),
                            ),
                            // Display the list of ingredients dynamically
                            Padding(
                              padding: const EdgeInsets.only(
                                  bottom: 16, left: 16, right: 16),
                              child: Column(
                                children:
                                    ingredients.asMap().entries.map((entry) {
                                  final int index = entry.key;
                                  final Ingredient ingredient = entry.value;
                                  return Row(
                                    children: [
                                      Expanded(
                                        child: TextField(
                                          controller: TextEditingController(
                                              text: ingredient.name),
                                          onChanged: (value) {
                                            ingredient.name = value;
                                          },
                                          decoration: InputDecoration(
                                            labelText: 'Ingredient Name',
                                            labelStyle: GoogleFonts.mali(
                                              fontSize: 14,
                                              fontWeight: FontWeight.bold,
                                              color: Colors.black,
                                            ),
                                          ),
                                        ),
                                      ),
                                      SizedBox(width: 16),
                                      Expanded(
                                        child: TextField(
                                          controller: TextEditingController(
                                              text: ingredient.quantity),
                                          onChanged: (value) {
                                            ingredient.quantity = value;
                                          },
                                          inputFormatters: [
                                            FilteringTextInputFormatter
                                                .digitsOnly,
                                          ],
                                          decoration: InputDecoration(
                                            labelText: 'Quantity',
                                            labelStyle: GoogleFonts.mali(
                                              fontSize: 14,
                                              fontWeight: FontWeight.bold,
                                              color: Colors.black,
                                            ),
                                          ),
                                        ),
                                      ),
                                      IconButton(
                                        icon: const Icon(Icons.delete),
                                        onPressed: () {
                                          // Call the function to remove the ingredient
                                          removeIngredient(index);
                                        },
                                      ),
                                    ],
                                  );
                                }).toList(),
                              ),
                            ),
                            Padding(
                              padding: const EdgeInsets.only(
                                  top: 16, left: 16, right: 16),
                              child: Column(
                                crossAxisAlignment: CrossAxisAlignment.start,
                                children: [
                                  Text(
                                    'Tools',
                                    style: GoogleFonts.mali(
                                      fontSize: 16,
                                      fontWeight: FontWeight.bold,
                                      color: Colors.black,
                                    ),
                                  ),
                                  ElevatedButton(
                                    style: ElevatedButton.styleFrom(
                                      elevation: 0,
                                      backgroundColor: const Color.fromARGB(
                                          255,
                                          255,
                                          225,
                                          136), // Change the background color of the button
                                      foregroundColor: Colors
                                          .black, // Change the text color of the button
                                    ),
                                    onPressed: () {
                                      // Call the function to add an ingredient
                                      addTool('');
                                    },
                                    child: Text(
                                      'Add Tool',
                                      style: GoogleFonts.mali(
                                        fontSize: 14,
                                        fontWeight: FontWeight.bold,
                                        color: Colors.black,
                                      ),
                                    ),
                                  ),
                                ],
                              ),
                            ),
                            // Display the list of ingredients dynamically
                            Padding(
                              padding: const EdgeInsets.only(
                                  bottom: 16, left: 16, right: 16),
                              child: Column(
                                children: tools.asMap().entries.map((entry) {
                                  final int index = entry.key;
                                  final String tool = entry.value;
                                  return Row(
                                    children: [
                                      Expanded(
                                        child: TextField(
                                          controller:
                                              TextEditingController(text: tool),
                                          onChanged: (value) {
                                            tools[index] =
                                                value; // Update the tool name
                                          },
                                          decoration: InputDecoration(
                                            labelText: 'Tool Name',
                                            labelStyle: GoogleFonts.mali(
                                              fontSize: 14,
                                              fontWeight: FontWeight.bold,
                                              color: Colors.black,
                                            ),
                                          ),
                                        ),
                                      ),
                                      IconButton(
                                        icon: const Icon(Icons.delete),
                                        onPressed: () {
                                          // Call the function to remove the ingredient
                                          removeTool(index);
                                        },
                                      ),
                                    ],
                                  );
                                }).toList(),
                              ),
                            ),
                            Padding(
                              padding: const EdgeInsets.only(
                                  top: 16, left: 16, right: 16),
                              child: Column(
                                crossAxisAlignment: CrossAxisAlignment.start,
                                children: [
                                  Text(
                                    'Steps',
                                    style: GoogleFonts.mali(
                                      fontSize: 16,
                                      fontWeight: FontWeight.bold,
                                      color: Colors.black,
                                    ),
                                  ),
                                  ElevatedButton(
                                    style: ElevatedButton.styleFrom(
                                      elevation: 0,
                                      backgroundColor: const Color.fromARGB(
                                          255,
                                          255,
                                          225,
                                          136), // Change the background color of the button
                                      foregroundColor: Colors
                                          .black, // Change the text color of the button
                                    ),
                                    onPressed: () {
                                      // Call the function to add an ingredient
                                      addStep('');
                                    },
                                    child: Text(
                                      'Add Step',
                                      style: GoogleFonts.mali(
                                        fontSize: 14,
                                        fontWeight: FontWeight.bold,
                                        color: Colors.black,
                                      ),
                                    ),
                                  ),
                                ],
                              ),
                            ),
                            // Display the list of ingredients dynamically
                            Padding(
                              padding: const EdgeInsets.only(
                                  bottom: 16, left: 16, right: 16),
                              child: Column(
                                children: steps.asMap().entries.map((entry) {
                                  final int index = entry.key;
                                  final String step = entry.value;
                                  return Row(
                                    children: [
                                      Expanded(
                                        child: TextField(
                                          controller:
                                              TextEditingController(text: step),
                                          onChanged: (value) {
                                            steps[index] =
                                                value; // Update the tool name
                                          },
                                          decoration: InputDecoration(
                                            labelText: 'Step',
                                            labelStyle: GoogleFonts.mali(
                                              fontSize: 14,
                                              fontWeight: FontWeight.bold,
                                              color: Colors.black,
                                            ),
                                          ),
                                        ),
                                      ),
                                      IconButton(
                                        icon: const Icon(Icons.delete),
                                        onPressed: () {
                                          // Call the function to remove the ingredient
                                          removeStep(index);
                                        },
                                      ),
                                    ],
                                  );
                                }).toList(),
                              ),
                            ),
                            Center(
                              child: Padding(
                                padding: const EdgeInsets.all(16.0),
                                child: ElevatedButton(
                                  style: ElevatedButton.styleFrom(
                                    elevation: 0,
                                    backgroundColor: const Color.fromARGB(
                                        255,
                                        255,
                                        225,
                                        136), // Change the background color of the button
                                    foregroundColor: Colors
                                        .black, // Change the text color of the button
                                  ),
                                  onPressed: () {
                                    updateRecipe(widget.recipe['menuid']);
                                    // Call the function to create menu
                                  },
                                  child: Text(
                                    'Update Recipe',
                                    style: GoogleFonts.mali(
                                      fontSize: 18,
                                      fontWeight: FontWeight.bold,
                                      color: Colors.black,
                                    ),
                                  ),
                                ),
                              ),
                            ),
                          ],
                        ),
                      ),
                    ),
                  ),
                ],
              ),
            ),
    );
  }
}
