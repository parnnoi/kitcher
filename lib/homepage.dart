// ignore_for_file: avoid_print

import 'package:flutter/material.dart';
import 'package:flutter_svg/flutter_svg.dart';
import 'package:google_fonts/google_fonts.dart';
import 'package:kitcher/category.dart';
import 'package:kitcher/search_result_page.dart';
import 'add.dart';
import 'profile.dart';
import 'detail.dart';
import 'dart:convert';
import 'package:http/http.dart' as http;

class MyHome extends StatelessWidget {
  final List<Map<String, dynamic>> info;
  const MyHome({Key? key, required this.info}) : super(key: key);

  @override
  Widget build(BuildContext context) {
    final List<Map<String, dynamic>> userData = info;
    return MaterialApp(
      title: 'Flutter Demo',
      theme: ThemeData(
        scaffoldBackgroundColor: const Color.fromARGB(255, 255, 251, 193),
      ),
      home: MyHomePage(
        info: userData,
      ),
    );
  }
}

class MyHomePage extends StatefulWidget {
  final List<Map<String, dynamic>> info;
  const MyHomePage({Key? key, required this.info}) : super(key: key);

  @override
  // ignore: no_logic_in_create_state
  State<MyHomePage> createState() => _MyHomePageState(info: info);
}

class _MyHomePageState extends State<MyHomePage> {
  List<Map<String, dynamic>> recipes = [];
  List<Map<String, dynamic>> recommended = [];
  List<Map<String, dynamic>> categoryRecipes = [];
  List<Map<String, dynamic>> info;
  int currentPage = 1;
  bool isLoading = true;

  _MyHomePageState({required this.info});
  @override
  void initState() {
    super.initState();
    // Fetch recommended menu data when the widget is initialized
    _fetchRecommendedMenu(getUID());
  }

  int getUID() {
    return info.isNotEmpty ? info[0]['uid'] : 0;
  }

  Future<void> _fetchRecommendedMenu(int userID) async {
    final Uri uri =
        Uri.parse('https://kitcherfromlocal.vercel.app/api/menu/all/1');

    final Map<String, dynamic> user = {
      "uid": userID,
    };

    final http.Response response = await http.post(
      uri,
      headers: {'Content-Type': 'application/json'},
      body: jsonEncode(user),
    );

    if (response.statusCode == 200) {
      final List<dynamic> recommendedMenu = jsonDecode(response.body);
      setState(() {
        recommended = recommendedMenu.cast<Map<String, dynamic>>();
        isLoading = false;
      });
    } else {
      // Handle error
      isLoading = false;
      print(
          'Failed to fetch recommended menu. Status code: ${response.statusCode}');
    }
  }

  Future<void> _loadMoreData() async {
    // Increment the page number
    currentPage++;

    final Uri uri = Uri.parse(
        'https://kitcherfromlocal.vercel.app/api/menu/all/$currentPage');

    final Map<String, dynamic> user = {
      "uid": getUID(),
    };

    final http.Response response = await http.post(
      uri,
      headers: {'Content-Type': 'application/json'},
      body: jsonEncode(user),
    );

    if (response.statusCode == 200) {
      final List<dynamic> additionalData = jsonDecode(response.body);
      setState(() {
        recommended.addAll(additionalData.cast<Map<String, dynamic>>());
      });
    } else {
      // Handle error
      print('Failed to load more data. Status code: ${response.statusCode}');
    }
  }

  @override
  Widget build(BuildContext context) {
    double screenWidth = MediaQuery.of(context).size.width;
    return Scaffold(
      appBar: AppBar(
        title: Padding(
          padding: const EdgeInsets.only(left: 0),
          child: SvgPicture.asset('assets/kitcher_icon_top.svg'),
        ),
        backgroundColor: const Color.fromARGB(255, 255, 251, 193),
        elevation: 0,
        actions: <Widget>[
          InkWell(
            child: IconButton(
              icon: const Icon(Icons.account_circle_outlined), // Profile icon
              iconSize: 50,
              color: const Color.fromARGB(255, 255, 225, 136),
              splashRadius: 20,
              onPressed: () {
                Navigator.push(
                    context,
                    MaterialPageRoute(
                        builder: (_) => MyProfilePage(
                              info: info,
                            )));
                // Handle profile icon action
              },
            ),
          )
        ],
      ),
      body: Column(
        crossAxisAlignment: CrossAxisAlignment.start,
        children: <Widget>[
          Padding(
            padding: const EdgeInsets.all(16.0),
            child: ClipRRect(
              borderRadius: BorderRadius.circular(30),
              child: Container(
                padding: const EdgeInsets.symmetric(horizontal: 16),
                color: const Color.fromARGB(255, 255, 254, 235),
                child: TextField(
                  decoration: const InputDecoration(
                    prefixIcon: Icon(
                      Icons.search,
                      size: 30,
                      color: Color.fromARGB(255, 209, 181, 98),
                    ),
                    border: InputBorder.none,
                  ),
                  onSubmitted: (value) {
                    // Handle search input
                    Navigator.push(
                      context,
                      MaterialPageRoute(
                        builder: (_) => SearchResultsPage(
                          searchTerms: value,
                          userID: getUID(),
                        ),
                      ),
                    );
                  },
                ),
              ),
            ),
          ),
          Padding(
            padding: const EdgeInsets.only(left: 16),
            child: Text(
              'Categories',
              style: GoogleFonts.mali(
                fontSize: 18,
                fontWeight: FontWeight.bold,
                color: Colors.black,
              ),
            ),
          ),
          Container(
            margin: const EdgeInsets.symmetric(vertical: 20),
            height: 80,
            child: SingleChildScrollView(
              scrollDirection: Axis.horizontal,
              child: Row(
                children: <Widget>[
                  Padding(
                      padding: const EdgeInsets.only(left: 10, right: 10),
                      child: GestureDetector(
                        onTap: () {
                          // Handle the tap event here
                          Navigator.push(
                            context,
                            MaterialPageRoute(
                              builder: (_) => CategoryPage(
                                searchTerms: '1',
                                category: 'Cake',
                                userID: getUID(),
                              ),
                            ),
                          );
                        },
                        child: Container(
                          width: screenWidth / 5,
                          decoration: BoxDecoration(
                            color: const Color.fromARGB(255, 255, 254, 235),
                            borderRadius: BorderRadius.circular(20),
                          ),
                          child: Column(
                            mainAxisAlignment: MainAxisAlignment.center,
                            children: [
                              Expanded(
                                child: IconButton(
                                  splashRadius: 10,
                                  icon: const Icon(Icons.cake_outlined),
                                  onPressed: () {
                                    Navigator.push(
                                      context,
                                      MaterialPageRoute(
                                        builder: (_) => CategoryPage(
                                          searchTerms: '1',
                                          category: 'Cake',
                                          userID: getUID(),
                                        ),
                                      ),
                                    );
                                  },
                                ),
                              ),
                              const SizedBox(
                                height: 4,
                              ), // Add some space between icon and text
                              Flexible(
                                  child: FittedBox(
                                fit: BoxFit.contain,
                                child: Text(
                                  'Cake',
                                  textAlign: TextAlign.center,
                                  style: GoogleFonts.mali(
                                    fontSize: 12,
                                    fontWeight: FontWeight.bold,
                                    color: Colors.black,
                                  ),
                                ),
                              )),
                            ],
                          ),
                        ),
                      )),
                  Padding(
                      padding: const EdgeInsets.only(left: 10, right: 10),
                      child: GestureDetector(
                        onTap: () {
                          // Handle the tap event here
                          Navigator.push(
                            context,
                            MaterialPageRoute(
                              builder: (_) => CategoryPage(
                                searchTerms: '2',
                                category: 'Beverage',
                                userID: getUID(),
                              ),
                            ),
                          );
                        },
                        child: Container(
                          width: screenWidth / 5,
                          decoration: BoxDecoration(
                            color: const Color.fromARGB(255, 255, 254, 235),
                            borderRadius: BorderRadius.circular(20),
                          ),
                          child: Column(
                            mainAxisAlignment: MainAxisAlignment.center,
                            children: [
                              Expanded(
                                child: IconButton(
                                  splashRadius: 10,
                                  icon: const Icon(
                                      Icons.emoji_food_beverage_outlined),
                                  onPressed: () {
                                    Navigator.push(
                                      context,
                                      MaterialPageRoute(
                                        builder: (_) => CategoryPage(
                                          searchTerms: '2',
                                          category: 'Beverage',
                                          userID: getUID(),
                                        ),
                                      ),
                                    );
                                  },
                                ),
                              ),
                              const SizedBox(
                                  height:
                                      4), // Add some space between icon and text
                              Flexible(
                                  child: FittedBox(
                                fit: BoxFit.contain,
                                child: Text(
                                  'Beverage',
                                  textAlign: TextAlign.center,
                                  style: GoogleFonts.mali(
                                    fontSize: 12,
                                    fontWeight: FontWeight.bold,
                                    color: Colors.black,
                                  ),
                                ),
                              )),
                            ],
                          ),
                        ),
                      )),
                  Padding(
                      padding: const EdgeInsets.only(left: 10, right: 10),
                      child: GestureDetector(
                        onTap: () {
                          // Handle the tap event here
                          Navigator.push(
                            context,
                            MaterialPageRoute(
                              builder: (_) => CategoryPage(
                                searchTerms: '3',
                                category: 'Street Food',
                                userID: getUID(),
                              ),
                            ),
                          );
                        },
                        child: Container(
                          width: screenWidth / 5,
                          decoration: BoxDecoration(
                            color: const Color.fromARGB(255, 255, 254, 235),
                            borderRadius: BorderRadius.circular(20),
                          ),
                          child: Column(
                            mainAxisAlignment: MainAxisAlignment.center,
                            children: [
                              Expanded(
                                child: IconButton(
                                  splashRadius: 10,
                                  icon: const Icon(Icons.fastfood_outlined),
                                  onPressed: () {
                                    Navigator.push(
                                      context,
                                      MaterialPageRoute(
                                        builder: (_) => CategoryPage(
                                          searchTerms: '3',
                                          category: 'Street Food',
                                          userID: getUID(),
                                        ),
                                      ),
                                    );
                                  },
                                ),
                              ),
                              const SizedBox(
                                  height:
                                      4), // Add some space between icon and text
                              Flexible(
                                  child: FittedBox(
                                fit: BoxFit.contain,
                                child: Text(
                                  'Street Food',
                                  textAlign: TextAlign.center,
                                  style: GoogleFonts.mali(
                                    fontSize: 12,
                                    fontWeight: FontWeight.bold,
                                    color: Colors.black,
                                  ),
                                ),
                              )),
                            ],
                          ),
                        ),
                      )),
                  Padding(
                      padding: const EdgeInsets.only(left: 10, right: 10),
                      child: GestureDetector(
                        onTap: () {
                          // Handle the tap event here
                          Navigator.push(
                            context,
                            MaterialPageRoute(
                              builder: (_) => CategoryPage(
                                searchTerms: '4',
                                category: 'Noodle',
                                userID: getUID(),
                              ),
                            ),
                          );
                        },
                        child: Container(
                          width: screenWidth / 5,
                          decoration: BoxDecoration(
                            color: const Color.fromARGB(255, 255, 254, 235),
                            borderRadius: BorderRadius.circular(20),
                          ),
                          child: Column(
                            mainAxisAlignment: MainAxisAlignment.center,
                            children: [
                              Expanded(
                                child: IconButton(
                                  splashRadius: 10,
                                  icon: const Icon(Icons.ramen_dining_outlined),
                                  onPressed: () {
                                    Navigator.push(
                                      context,
                                      MaterialPageRoute(
                                        builder: (_) => CategoryPage(
                                          searchTerms: '4',
                                          category: 'Noodle',
                                          userID: getUID(),
                                        ),
                                      ),
                                    );
                                  },
                                ),
                              ),
                              const SizedBox(
                                  height:
                                      4), // Add some space between icon and text
                              Flexible(
                                  child: FittedBox(
                                fit: BoxFit.contain,
                                child: Text(
                                  'Noodle',
                                  textAlign: TextAlign.center,
                                  style: GoogleFonts.mali(
                                    fontSize: 12,
                                    fontWeight: FontWeight.bold,
                                    color: Colors.black,
                                  ),
                                ),
                              )),
                            ],
                          ),
                        ),
                      )),
                  Padding(
                      padding: const EdgeInsets.only(left: 10, right: 10),
                      child: GestureDetector(
                        onTap: () {
                          // Handle the tap event here
                          Navigator.push(
                            context,
                            MaterialPageRoute(
                              builder: (_) => CategoryPage(
                                searchTerms: '5',
                                category: 'Appetizer',
                                userID: getUID(),
                              ),
                            ),
                          );
                        },
                        child: Container(
                          width: screenWidth / 5,
                          decoration: BoxDecoration(
                            color: const Color.fromARGB(255, 255, 254, 235),
                            borderRadius: BorderRadius.circular(20),
                          ),
                          child: Column(
                            mainAxisAlignment: MainAxisAlignment.center,
                            children: [
                              Expanded(
                                child: IconButton(
                                  splashRadius: 10,
                                  icon: const Icon(Icons.kebab_dining_outlined),
                                  onPressed: () {
                                    Navigator.push(
                                      context,
                                      MaterialPageRoute(
                                        builder: (_) => CategoryPage(
                                          searchTerms: '5',
                                          category: 'Appetizer',
                                          userID: getUID(),
                                        ),
                                      ),
                                    );
                                  },
                                ),
                              ),
                              const SizedBox(
                                  height:
                                      4), // Add some space between icon and text
                              Flexible(
                                  child: FittedBox(
                                fit: BoxFit.contain,
                                child: Text(
                                  'Appetizer',
                                  textAlign: TextAlign.center,
                                  style: GoogleFonts.mali(
                                    fontSize: 12,
                                    fontWeight: FontWeight.bold,
                                    color: Colors.black,
                                  ),
                                ),
                              )),
                            ],
                          ),
                        ),
                      )),
                  Padding(
                      padding: const EdgeInsets.only(left: 10, right: 10),
                      child: GestureDetector(
                        onTap: () {
                          // Handle the tap event here
                          Navigator.push(
                            context,
                            MaterialPageRoute(
                              builder: (_) => CategoryPage(
                                searchTerms: '6',
                                category: 'Bakery',
                                userID: getUID(),
                              ),
                            ),
                          );
                        },
                        child: Container(
                          width: screenWidth / 5,
                          decoration: BoxDecoration(
                            color: const Color.fromARGB(255, 255, 254, 235),
                            borderRadius: BorderRadius.circular(20),
                          ),
                          child: Column(
                            mainAxisAlignment: MainAxisAlignment.center,
                            children: [
                              Expanded(
                                child: IconButton(
                                  splashRadius: 10,
                                  icon:
                                      const Icon(Icons.bakery_dining_outlined),
                                  onPressed: () {
                                    Navigator.push(
                                      context,
                                      MaterialPageRoute(
                                        builder: (_) => CategoryPage(
                                          searchTerms: '5',
                                          category: 'Bakery',
                                          userID: getUID(),
                                        ),
                                      ),
                                    );
                                  },
                                ),
                              ),
                              const SizedBox(
                                  height:
                                      4), // Add some space between icon and text
                              Flexible(
                                  child: FittedBox(
                                fit: BoxFit.contain,
                                child: Text(
                                  'Bakery',
                                  textAlign: TextAlign.center,
                                  style: GoogleFonts.mali(
                                    fontSize: 12,
                                    fontWeight: FontWeight.bold,
                                    color: Colors.black,
                                  ),
                                ),
                              )),
                            ],
                          ),
                        ),
                      )),
                  Padding(
                      padding: const EdgeInsets.only(left: 10, right: 10),
                      child: GestureDetector(
                        onTap: () {
                          // Handle the tap event here
                          Navigator.push(
                            context,
                            MaterialPageRoute(
                              builder: (_) => CategoryPage(
                                searchTerms: '7',
                                category: 'Japan Food',
                                userID: getUID(),
                              ),
                            ),
                          );
                        },
                        child: Container(
                          width: screenWidth / 5,
                          decoration: BoxDecoration(
                            color: const Color.fromARGB(255, 255, 254, 235),
                            borderRadius: BorderRadius.circular(20),
                          ),
                          child: Column(
                            mainAxisAlignment: MainAxisAlignment.center,
                            children: [
                              Expanded(
                                child: IconButton(
                                  splashRadius: 10,
                                  icon: const Icon(
                                      Icons.restaurant_menu_outlined),
                                  onPressed: () {
                                    Navigator.push(
                                      context,
                                      MaterialPageRoute(
                                        builder: (_) => CategoryPage(
                                          searchTerms: '7',
                                          category: 'Japan Food',
                                          userID: getUID(),
                                        ),
                                      ),
                                    );
                                  },
                                ),
                              ),
                              const SizedBox(
                                  height:
                                      4), // Add some space between icon and text
                              Flexible(
                                  child: FittedBox(
                                fit: BoxFit.contain,
                                child: Text(
                                  'Japan Food',
                                  textAlign: TextAlign.center,
                                  style: GoogleFonts.mali(
                                    fontSize: 12,
                                    fontWeight: FontWeight.bold,
                                    color: Colors.black,
                                  ),
                                ),
                              )),
                            ],
                          ),
                        ),
                      )),
                  Padding(
                      padding: const EdgeInsets.only(left: 10, right: 10),
                      child: GestureDetector(
                        onTap: () {
                          // Handle the tap event here
                          Navigator.push(
                            context,
                            MaterialPageRoute(
                              builder: (_) => CategoryPage(
                                searchTerms: '8',
                                category: 'Korea Food',
                                userID: getUID(),
                              ),
                            ),
                          );
                        },
                        child: Container(
                          width: screenWidth / 5,
                          decoration: BoxDecoration(
                            color: const Color.fromARGB(255, 255, 254, 235),
                            borderRadius: BorderRadius.circular(20),
                          ),
                          child: Column(
                            mainAxisAlignment: MainAxisAlignment.center,
                            children: [
                              Expanded(
                                child: IconButton(
                                  splashRadius: 10,
                                  icon: const Icon(
                                      Icons.restaurant_menu_outlined),
                                  onPressed: () {
                                    Navigator.push(
                                      context,
                                      MaterialPageRoute(
                                        builder: (_) => CategoryPage(
                                          searchTerms: '8',
                                          category: 'Korea Food',
                                          userID: getUID(),
                                        ),
                                      ),
                                    );
                                  },
                                ),
                              ),
                              const SizedBox(
                                  height:
                                      4), // Add some space between icon and text
                              Flexible(
                                  child: FittedBox(
                                fit: BoxFit.contain,
                                child: Text(
                                  'Korea Food',
                                  textAlign: TextAlign.center,
                                  style: GoogleFonts.mali(
                                    fontSize: 12,
                                    fontWeight: FontWeight.bold,
                                    color: Colors.black,
                                  ),
                                ),
                              )),
                            ],
                          ),
                        ),
                      )),
                ],
              ),
            ),
          ),
          Padding(
            padding: const EdgeInsets.only(left: 16, bottom: 0),
            child: Row(
              children: [
                Text(
                  'Recommended',
                  style: GoogleFonts.mali(
                    fontSize: 18,
                    fontWeight: FontWeight.bold,
                    color: Colors.black,
                  ),
                ),
                IconButton(
                  icon: const Icon(
                    Icons.refresh_outlined,
                    color: Colors.black,
                  ),
                  onPressed: () {
                    Navigator.pushReplacement(
                      context,
                      MaterialPageRoute(
                        builder: (context) => MyHome(
                          info: info,
                        ),
                      ),
                    );
                  },
                ),
              ],
            ),
          ),
          Padding(
            padding: const EdgeInsets.only(bottom: 10),
            child: Center(
              child: Container(
                height: screenWidth / 12,
                width: screenWidth / 4,
                decoration: BoxDecoration(
                  color: const Color.fromARGB(255, 255, 225, 136),
                  borderRadius: BorderRadius.circular(20),
                ),
                child: TextButton(
                    onPressed: _loadMoreData,
                    child: FittedBox(
                      child: Text(
                        'Load More',
                        style: GoogleFonts.mali(
                          fontSize: 16,
                          fontWeight: FontWeight.bold,
                          color: Colors.black,
                        ),
                      ),
                    )),
              ),
            ),
          ),
          isLoading
              ? const Padding(
                  padding: EdgeInsets.only(top: 150),
                  child: Center(
                    child: CircularProgressIndicator(
                      color: Color.fromARGB(255, 255, 225, 136),
                    ),
                  ),
                )
              : Expanded(
                  child: GridView.builder(
                    gridDelegate:
                        const SliverGridDelegateWithFixedCrossAxisCount(
                      crossAxisCount: 2,
                      crossAxisSpacing: 8.0,
                      mainAxisSpacing: 8.0,
                    ),
                    itemCount: recommended.length,
                    itemBuilder: (BuildContext context, int index) {
                      final recipe = recommended[index];
                      return GestureDetector(
                        onTap: () {
                          Navigator.push(
                            context,
                            MaterialPageRoute(
                              builder: (context) =>
                                  DetailPage(recipe: recipe, userID: getUID()),
                            ),
                          );
                        },
                        child: Padding(
                          padding: const EdgeInsets.all(16),
                          child: Container(
                            decoration: BoxDecoration(
                              borderRadius: BorderRadius.circular(20),
                              color: const Color.fromARGB(255, 255, 254, 235),
                            ),
                            width: screenWidth / 2.5,
                            height: screenWidth / 2.5,
                            child: Column(
                              mainAxisAlignment: MainAxisAlignment.center,
                              children: [
                                FittedBox(
                                  fit: BoxFit.contain,
                                  child: Text(
                                    recipe['menuName'],
                                    style: GoogleFonts.mali(
                                      fontSize: 16,
                                      fontWeight: FontWeight.bold,
                                      color: Colors.black,
                                    ),
                                    textAlign: TextAlign.center,
                                  ),
                                ),
                                const SizedBox(height: 8.0),
                                FittedBox(
                                  fit: BoxFit.contain,
                                  child: Text(
                                    'Created by: ${recipe['createruid']}',
                                    style: GoogleFonts.mali(
                                      fontSize: 12,
                                      color: Colors.black,
                                    ),
                                    textAlign: TextAlign.center,
                                  ),
                                ),
                              ],
                            ),
                          ),
                        ),
                      );
                    },
                  ),
                ),
        ],
      ),
      floatingActionButton: EggFloatingActionButton(userID: getUID()),
      floatingActionButtonLocation: FloatingActionButtonLocation.centerFloat,
    );
  }
}

class EggFloatingActionButton extends StatelessWidget {
  final int userID;
  const EggFloatingActionButton({super.key, required this.userID});

  @override
  Widget build(BuildContext context) {
    return FloatingActionButton(
      onPressed: () {
        Navigator.push(
          context,
          MaterialPageRoute(
            builder: (_) => AddPage(
              userID: userID,
            ),
          ),
        );
      },
      child: Stack(
        children: [
          // White Egg Layer
          Container(
            height: 56,
            width: 56,
            decoration: const BoxDecoration(
              shape: BoxShape.circle,
              color: Colors.white,
            ),
          ),
          // Yolk Layer
          Positioned(
            top: 8,
            left: 8,
            child: Container(
              height: 40,
              width: 40,
              decoration: const BoxDecoration(
                shape: BoxShape.circle,
                color: Color.fromARGB(255, 255, 225, 136), // Yolk color
              ),
              child: const Center(
                child: Icon(
                  Icons.add,
                  color: Colors.white,
                  size: 40,
                ),
              ),
            ),
          ),
        ],
      ),
    );
  }
}
