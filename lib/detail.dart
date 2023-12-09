// ignore_for_file: use_build_context_synchronously

import 'package:flutter/material.dart';
import 'package:google_fonts/google_fonts.dart';
import 'package:flutter_rating_bar/flutter_rating_bar.dart';
import 'dart:convert';
import 'package:http/http.dart' as http;

class DetailPage extends StatefulWidget {
  final Map<String, dynamic> recipe;
  final int userID;

  const DetailPage({Key? key, required this.recipe, required this.userID})
      : super(key: key);

  @override
  State<DetailPage> createState() => _DetailPageState();
}

class _DetailPageState extends State<DetailPage> {
  List<Map<String, dynamic>> menuDescription = [];
  List<dynamic> menuTool = [];
  List<dynamic> menuIngredient = [];
  List<dynamic> menuStep = [];
  bool isLoading = true;
  String activeSection = 'ingredients';
  String statusMessage = '';
  double score = 0;

  @override
  void initState() {
    super.initState();
    fetchMenuDetails(widget.recipe['menuid']);
  }

  Future<void> fetchMenuDetails(
    int menuID,
  ) async {
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
      setState(() {
        menuDescription = [detail['menuDescription']];
        menuIngredient = detail['ingredient'];
        menuStep = detail['step'];
        menuTool = detail['tool'];
        isLoading = false;
      });
      print("select1 ${menuDescription}");
      print("select2 ${menuIngredient}");
      print("select3 ${menuTool}");
      print("select4 ${menuStep}");
      print("select ${menuDescription[0]['menuid']}");
      print("count ${menuDescription[0]['visitCount']}");
      print("step ${menuStep}");
    } else if (response.statusCode == 404) {
      setState(() {
        isLoading = false;
        statusMessage = 'This menu is private';
      });
    } else {
      // Handle error
      print(
          'Failed to fetch menu details. Status code: ${response.statusCode}');
      isLoading = false;
    }
  }

  Future<void> addFavorite(int userID, int menuID) async {
    final Uri uri =
        Uri.parse('https://kitcherfromlocal.vercel.app/api/menu/favorite');

    Map<String, dynamic> requestData = {
      "uid": userID,
      "menuid": menuID,
    };

    final http.Response response = await http.post(
      uri,
      headers: {'Content-Type': 'application/json'},
      body: jsonEncode(requestData),
    );
    print('$requestData');
    print('${jsonEncode(response.body)}');
    print('${response.statusCode}');
    if (response.statusCode == 200) {
      showDialog(
        context: context,
        builder: (BuildContext context) {
          return AlertDialog(
            title: Text(
              'Added successfully',
              style: GoogleFonts.mali(
                fontWeight: FontWeight.bold,
                color: Colors.black,
              ),
            ),
            actions: <Widget>[
              TextButton(
                onPressed: () {
                  Navigator.of(context).pop();
                },
                child: Text(
                  'OK',
                  style: GoogleFonts.mali(
                    fontWeight: FontWeight.bold,
                    color: Colors.black,
                  ),
                ),
              ),
            ],
          );
        },
      );
      print('Added to favorites successfully');
    } else if (response.statusCode == 400) {
      showDialog(
        context: context,
        builder: (BuildContext context) {
          return AlertDialog(
            title: Text(
              'Already added to favorite',
              style: GoogleFonts.mali(
                fontWeight: FontWeight.bold,
                color: Colors.black,
              ),
            ),
            actions: <Widget>[
              TextButton(
                onPressed: () {
                  Navigator.of(context).pop();
                },
                child: Text(
                  'OK',
                  style: GoogleFonts.mali(
                    fontWeight: FontWeight.bold,
                    color: Colors.black,
                  ),
                ),
              ),
            ],
          );
        },
      );
    } else {
      print('error Status code: ${response.statusCode}');
    }
  }

  Future<void> voteScore(double score) async {
    final Uri uri =
        Uri.parse('https://kitcherfromlocal.vercel.app/api/menu/vote');

    Map<String, dynamic> requestData = {
      "uid": widget.userID,
      "menuid": menuDescription[0]['menuid'],
      "score": score,
      "comment": [],
    };

    final http.Response response = await http.post(
      uri,
      headers: {'Content-Type': 'application/json'},
      body: jsonEncode(requestData),
    );
    print('$requestData');
    print('${jsonEncode(response.body)}');
    print('${response.statusCode}');
    if (response.statusCode == 200) {
      print('voted success');
    } else if (response.statusCode == 429) {
      print('Already voted');
    } else {
      print('error Status code: ${response.statusCode}');
    }
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
      body: SingleChildScrollView(
        child: isLoading
            ? Padding(
                padding: EdgeInsets.only(top: (screenHeight / 2) - 100),
                child: const Center(
                  child: CircularProgressIndicator(
                    color: Color.fromARGB(255, 255, 225, 136),
                  ),
                ),
              )
            : statusMessage.isNotEmpty
                ? Padding(
                    padding: EdgeInsets.only(top: (screenHeight / 2) - 100),
                    child: Center(
                      child: Text(
                        statusMessage,
                        textAlign: TextAlign.center,
                        style: GoogleFonts.mali(
                          fontSize: 18,
                          fontWeight: FontWeight.bold,
                          color: Colors.black,
                        ),
                      ),
                    ),
                  )
                : Column(
                    crossAxisAlignment: CrossAxisAlignment.start,
                    children: [
                      Padding(
                        padding: const EdgeInsets.only(top: 10),
                        child: Center(
                          child: Container(
                            decoration: BoxDecoration(
                              image: const DecorationImage(
                                image: AssetImage("assets/kitcher_icon2.png"),
                              ),
                              borderRadius: BorderRadius.circular(20),
                              color: const Color.fromARGB(255, 255, 254, 235),
                            ),
                            width: screenWidth - 64,
                            height: screenHeight / 4.5,
                          ),
                        ),
                      ),
                      Padding(
                        padding:
                            const EdgeInsets.only(top: 20, left: 16, right: 16),
                        child: Row(
                          children: [
                            Container(
                              height: screenHeight / 26,
                              width: screenWidth / 3.3,
                              decoration: BoxDecoration(
                                color: const Color.fromARGB(255, 255, 225, 136),
                                borderRadius: BorderRadius.circular(20),
                              ),
                              child: TextButton(
                                  onPressed: () {
                                    addFavorite(widget.userID,
                                        menuDescription[0]['menuid']);
                                  },
                                  child: FittedBox(
                                    fit: BoxFit.contain,
                                    child: Text(
                                      'Add Favorite',
                                      style: GoogleFonts.mali(
                                        fontSize: 16,
                                        fontWeight: FontWeight.bold,
                                        color: Colors.black,
                                      ),
                                    ),
                                  )),
                            ),
                            const Spacer(),
                            Container(
                              height: screenHeight / 26,
                              width: screenWidth / 4,
                              decoration: BoxDecoration(
                                color: const Color.fromARGB(255, 255, 225, 136),
                                borderRadius: BorderRadius.circular(20),
                              ),
                              child: TextButton(
                                onPressed: () {
                                  showDialog(
                                    context: context,
                                    builder: (BuildContext context) {
                                      return AlertDialog(
                                        title: Text(
                                          'Vote your score',
                                          style: GoogleFonts.mali(
                                            fontWeight: FontWeight.bold,
                                            color: Colors.black,
                                          ),
                                        ),
                                        content: RatingBar.builder(
                                          initialRating: 0,
                                          minRating: 0,
                                          ignoreGestures: false,
                                          direction: Axis.horizontal,
                                          allowHalfRating: true,
                                          itemCount: 5,
                                          itemSize: 20,
                                          itemPadding:
                                              const EdgeInsets.symmetric(
                                                  horizontal: 1.0),
                                          itemBuilder: (context, _) =>
                                              const Icon(
                                            Icons.star,
                                            color: Colors.amber,
                                          ),
                                          onRatingUpdate: (rating) {
                                            score = rating;
                                          },
                                        ),
                                        actions: <Widget>[
                                          TextButton(
                                            onPressed: () {
                                              voteScore(score);
                                              Navigator.of(context).pop();
                                            },
                                            child: Text(
                                              'OK',
                                              style: GoogleFonts.mali(
                                                fontWeight: FontWeight.bold,
                                                color: Colors.black,
                                              ),
                                            ),
                                          ),
                                          TextButton(
                                            onPressed: () {
                                              Navigator.of(context).pop();
                                            },
                                            child: Text(
                                              'Cancel',
                                              style: GoogleFonts.mali(
                                                fontWeight: FontWeight.bold,
                                                color: Colors.black,
                                              ),
                                            ),
                                          ),
                                        ],
                                      );
                                    },
                                  );
                                },
                                child: FittedBox(
                                  fit: BoxFit.contain,
                                  child: Text(
                                    'Vote Rating',
                                    style: GoogleFonts.mali(
                                      fontSize: 16,
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
                      Padding(
                        padding: const EdgeInsets.only(top: 10),
                        child: Center(
                          child: Container(
                            decoration: BoxDecoration(
                              borderRadius: BorderRadius.circular(20),
                              color: const Color.fromARGB(255, 255, 254, 235),
                            ),
                            width: screenWidth - 32,
                            height: screenHeight / 6,
                            child: Column(
                              crossAxisAlignment: CrossAxisAlignment.start,
                              children: [
                                Row(
                                  children: [
                                    Padding(
                                      padding: const EdgeInsets.only(
                                          top: 10, left: 16, bottom: 10),
                                      child: RatingBar.builder(
                                        initialRating: menuDescription[0]
                                            ['avgVote'],
                                        minRating: 0,
                                        ignoreGestures: true,
                                        direction: Axis.horizontal,
                                        allowHalfRating: true,
                                        itemCount: 5,
                                        itemSize: 20,
                                        itemPadding: const EdgeInsets.symmetric(
                                            horizontal: 1.0),
                                        itemBuilder: (context, _) => const Icon(
                                          Icons.star,
                                          color: Colors.amber,
                                        ),
                                        onRatingUpdate: (rating) {
                                          // You can handle the rating update if needed
                                        },
                                      ),
                                    ),
                                    const Spacer(),
                                    Padding(
                                      padding: const EdgeInsets.only(
                                          top: 10, right: 16),
                                      child: Container(
                                        decoration: BoxDecoration(
                                          borderRadius:
                                              BorderRadius.circular(20),
                                          color: Colors.green,
                                        ),
                                        width: screenWidth / 4,
                                        height: screenHeight / 25,
                                        child: Row(
                                          children: [
                                            const Padding(
                                              padding: EdgeInsets.only(left: 8),
                                              child: Icon(
                                                Icons.av_timer_outlined,
                                                color: Colors.white,
                                              ),
                                            ),
                                            const Spacer(),
                                            Padding(
                                                padding: const EdgeInsets.only(
                                                    right: 8),
                                                child: FittedBox(
                                                  fit: BoxFit.contain,
                                                  child: Text(
                                                    '${menuDescription[0]['estimateTime']}',
                                                    style: GoogleFonts.mali(
                                                      fontSize: 16,
                                                      fontWeight:
                                                          FontWeight.bold,
                                                      color: Colors.white,
                                                    ),
                                                  ),
                                                )),
                                          ],
                                        ),
                                      ),
                                    ),
                                  ],
                                ),
                                Padding(
                                    padding: const EdgeInsets.only(left: 16),
                                    child: FittedBox(
                                      fit: BoxFit.contain,
                                      child: Text(
                                        '${menuDescription[0]['menuName']}',
                                        style: GoogleFonts.mali(
                                          fontSize: 20,
                                          fontWeight: FontWeight.bold,
                                          color: Colors.black,
                                        ),
                                      ),
                                    )),
                                Padding(
                                    padding: const EdgeInsets.only(left: 16),
                                    child: FittedBox(
                                      fit: BoxFit.contain,
                                      child: Text(
                                        'Category : ${menuDescription[0]['categoryName']}',
                                        style: GoogleFonts.mali(
                                          fontSize: 16,
                                          fontWeight: FontWeight.normal,
                                          color: Colors.black,
                                        ),
                                      ),
                                    )),
                                Padding(
                                    padding: const EdgeInsets.only(left: 16),
                                    child: FittedBox(
                                      fit: BoxFit.contain,
                                      child: Text(
                                        'Owner : ${menuDescription[0]['fName']} ${menuDescription[0]['lName']}',
                                        style: GoogleFonts.mali(
                                          fontSize: 16,
                                          fontWeight: FontWeight.normal,
                                          color: Colors.black,
                                        ),
                                      ),
                                    )),
                                Padding(
                                    padding: const EdgeInsets.only(left: 16),
                                    child: FittedBox(
                                      fit: BoxFit.contain,
                                      child: Text(
                                        'Creation Date : ${menuDescription[0]['createdDate']}',
                                        style: GoogleFonts.mali(
                                          fontSize: 16,
                                          fontWeight: FontWeight.normal,
                                          color: Colors.black,
                                        ),
                                      ),
                                    )),
                              ],
                            ),
                          ),
                        ),
                      ),
                      Padding(
                        padding: const EdgeInsets.only(top: 10),
                        child: Center(
                          child: Container(
                            decoration: BoxDecoration(
                              borderRadius: BorderRadius.circular(20),
                              color: const Color.fromARGB(255, 255, 254, 235),
                            ),
                            width: screenWidth - 32,
                            child: Padding(
                              padding: const EdgeInsets.all(10.0),
                              child: Column(
                                children: [
                                  Row(
                                    crossAxisAlignment:
                                        CrossAxisAlignment.start,
                                    children: [
                                      buildSectionButton(
                                        'Ingredients',
                                        screenWidth,
                                        screenHeight,
                                        activeSection == 'ingredients',
                                        () {
                                          setState(() {
                                            activeSection = 'ingredients';
                                          });
                                        },
                                      ),
                                      const Spacer(),
                                      buildSectionButton(
                                        'Tools',
                                        screenWidth,
                                        screenHeight,
                                        activeSection == 'tools',
                                        () {
                                          setState(() {
                                            activeSection = 'tools';
                                          });
                                        },
                                      ),
                                      const Spacer(),
                                      buildSectionButton(
                                        'Steps',
                                        screenWidth,
                                        screenHeight,
                                        activeSection == 'steps',
                                        () {
                                          setState(() {
                                            activeSection = 'steps';
                                          });
                                        },
                                      ),
                                    ],
                                  ),
                                  if (activeSection == 'ingredients')
                                    buildIngredientsSection(screenWidth,
                                        screenHeight, menuIngredient),
                                  if (activeSection == 'tools')
                                    buildToolsSection(
                                        screenWidth, screenHeight, menuTool),
                                  if (activeSection == 'steps')
                                    buildStepsSection(
                                        screenWidth, screenHeight, menuStep),
                                ],
                              ),
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

Widget buildSectionButton(
  String text,
  double screenWidth,
  double screenHeight,
  bool isActive,
  VoidCallback onPressed,
) {
  return AnimatedContainer(
    duration: const Duration(milliseconds: 150),
    alignment: Alignment.center,
    height: screenHeight / 23,
    width: screenWidth / 4,
    decoration: BoxDecoration(
      color: isActive
          ? const Color.fromARGB(255, 255, 225, 136)
          : const Color.fromARGB(255, 255, 251, 193),
      borderRadius: BorderRadius.circular(20),
    ),
    child: TextButton(
        onPressed: onPressed,
        child: FittedBox(
          fit: BoxFit.contain,
          child: Text(
            text,
            style: GoogleFonts.mali(
              fontSize: 14,
              fontWeight: FontWeight.bold,
              color: isActive ? Colors.black : Colors.black,
            ),
          ),
        )),
  );
}

Widget buildIngredientsSection(
  double screenWidth,
  double screenHeight,
  List<dynamic> menuIngredient,
) {
  return AnimatedContainer(
    duration: const Duration(milliseconds: 150),
    width: screenWidth - 32,
    padding: const EdgeInsets.all(16),
    decoration: BoxDecoration(
      borderRadius: BorderRadius.circular(20),
      color: const Color.fromARGB(255, 255, 254, 235),
    ),
    child: Column(
      crossAxisAlignment: CrossAxisAlignment.start,
      children: [
        Center(
          child: Table(
            border: TableBorder.all(
              borderRadius: BorderRadius.circular(20),
              width: 1.5,
            ),
            columnWidths: {
              0: FixedColumnWidth(
                  screenWidth / 1.7), // Width for the 'Ingredient' column
              1: const IntrinsicColumnWidth(),
            },
            children: [
              TableRow(
                children: [
                  TableCell(
                    verticalAlignment: TableCellVerticalAlignment.middle,
                    child: Center(
                      child: Padding(
                          padding: const EdgeInsets.all(8.0),
                          child: FittedBox(
                            fit: BoxFit.contain,
                            child: Text(
                              'Ingredient',
                              style: GoogleFonts.mali(
                                fontSize: 14,
                                fontWeight: FontWeight.bold,
                              ),
                            ),
                          )),
                    ),
                  ),
                  TableCell(
                    verticalAlignment: TableCellVerticalAlignment.middle,
                    child: Center(
                      child: Padding(
                          padding: const EdgeInsets.all(8.0),
                          child: FittedBox(
                            fit: BoxFit.contain,
                            child: Text(
                              'Quantity',
                              style: GoogleFonts.mali(
                                fontSize: 14,
                                fontWeight: FontWeight.bold,
                              ),
                            ),
                          )),
                    ),
                  ),
                ],
              ),
              for (var ingredient in menuIngredient)
                TableRow(
                  children: [
                    TableCell(
                      child: Padding(
                        padding: const EdgeInsets.all(8.0),
                        child: Text(
                          ingredient['ingredientname'],
                          style: GoogleFonts.mali(
                            fontSize: 14,
                            fontWeight: FontWeight.normal,
                          ),
                        ),
                      ),
                    ),
                    TableCell(
                      child: Center(
                        child: Padding(
                          padding: const EdgeInsets.all(8.0),
                          child: Text(
                            '${ingredient['quantity']}',
                            style: GoogleFonts.mali(
                              fontSize: 14,
                              fontWeight: FontWeight.normal,
                            ),
                          ),
                        ),
                      ),
                    ),
                  ],
                ),
            ],
          ),
        ),
      ],
    ),
  );
}

Widget buildToolsSection(
  double screenWidth,
  double screenHeight,
  List<dynamic> menuTools,
) {
  return AnimatedContainer(
    duration: const Duration(milliseconds: 150),
    width: screenWidth - 32,
    padding: const EdgeInsets.all(16),
    decoration: BoxDecoration(
      borderRadius: BorderRadius.circular(20),
      color: const Color.fromARGB(255, 255, 254, 235),
    ),
    child: Column(
      crossAxisAlignment: CrossAxisAlignment.start,
      children: [
        Center(
          child: Column(
            children: [
              for (var tool in menuTools)
                Padding(
                  padding: const EdgeInsets.all(8.0),
                  child: Row(
                    children: [
                      FittedBox(
                        fit: BoxFit.contain,
                        child: Text(
                          '- ${tool['toolname']}',
                          style: GoogleFonts.mali(
                            fontSize: 14,
                            fontWeight: FontWeight.normal,
                          ),
                        ),
                      )
                    ],
                  ),
                ),
            ],
          ),
        ),
      ],
    ),
  );
}

Widget buildStepsSection(
  double screenWidth,
  double screenHeight,
  List<dynamic> menuSteps,
) {
  return AnimatedContainer(
    duration: const Duration(milliseconds: 150),
    width: screenWidth - 32,
    padding: const EdgeInsets.all(16),
    decoration: BoxDecoration(
      borderRadius: BorderRadius.circular(20),
      color: const Color.fromARGB(255, 255, 254, 235),
    ),
    child: Column(
      crossAxisAlignment: CrossAxisAlignment.start,
      children: [
        Center(
          child: Column(
            children: [
              for (var step in menuSteps)
                Padding(
                  padding: const EdgeInsets.all(8.0),
                  child: Row(
                    children: [
                      Text(
                        'Step ${step['norder']} : ',
                        style: GoogleFonts.mali(
                          fontSize: 14,
                          fontWeight: FontWeight.normal,
                        ),
                      ),
                      Text(
                        step['stepname'],
                        style: GoogleFonts.mali(
                          fontSize: 14,
                          fontWeight: FontWeight.normal,
                        ),
                      ),
                    ],
                  ),
                ),
            ],
          ),
        ),
      ],
    ),
  );
}
