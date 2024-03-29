import 'package:flutter/material.dart';
import 'package:google_fonts/google_fonts.dart';
import 'detailmymenu.dart';
import 'dart:convert';
import 'package:http/http.dart' as http;

class MyMenuPage extends StatefulWidget {
  final int userID;
  const MyMenuPage({
    Key? key,
    required this.userID,
  }) : super(key: key);
  @override
  // ignore: library_private_types_in_public_api
  _MyMenuPageState createState() => _MyMenuPageState();
}

class _MyMenuPageState extends State<MyMenuPage> {
  int currentPage = 1;
  String statusMessage = '';
  bool isLoading = true;
  List<Map<String, dynamic>> myMenu = [];
  final ScrollController _scrollController = ScrollController();

  @override
  void initState() {
    super.initState();
    _searchMyMenu(widget.userID);
    // Attach the listener to the ScrollController
    _scrollController.addListener(_scrollListener);
  }

  @override
  void dispose() {
    // Dispose of the ScrollController
    _scrollController.dispose();
    super.dispose();
  }

  // Listener function to check for scroll position
  void _scrollListener() {
    if (_scrollController.position.pixels ==
        _scrollController.position.maxScrollExtent) {
      // User reached the end of the list, load more data
      _loadMoreData();
    }
  }

  Future<void> _searchMyMenu(int createrID) async {
    final Uri uri =
        Uri.parse('https://kitcherfromlocal.vercel.app/api/menu/creater/1');
    final Map<String, dynamic> user = {
      "uid": createrID,
    };

    final http.Response response = await http.post(
      uri,
      headers: {'Content-Type': 'application/json'},
      body: jsonEncode(user),
    );
    print('$uri');
    print("${jsonEncode(response.body)}");
    if (response.statusCode == 200) {
      final List<dynamic> searchResults = jsonDecode(response.body);
      setState(() {
        myMenu = searchResults.cast<Map<String, dynamic>>();
        isLoading = false;
      });
      // Navigate to the search results page
    } else {
      setState(
        () {
          statusMessage = 'There is no menu yet. Try to add menu.';
          isLoading = false;
        },
      );
    }
  }

  Future<void> _loadMoreData() async {
    // Increment the page number
    currentPage++;

    final Uri uri = Uri.parse(
        'https://kitcherfromlocal.vercel.app/api/menu/creater/$currentPage');

    final Map<String, dynamic> user = {
      "uid": widget.userID,
    };

    final http.Response response = await http.post(
      uri,
      headers: {'Content-Type': 'application/json'},
      body: jsonEncode(user),
    );

    if (response.statusCode == 200) {
      final List<dynamic> additionalData = jsonDecode(response.body);

      setState(() {
        myMenu.addAll(additionalData.cast<Map<String, dynamic>>());
      });
    } else {
      // Handle error
      print('Failed to load more data. Status code: ${response.statusCode}');
    }
  }

  @override
  Widget build(BuildContext context) {
    double screenWidth = MediaQuery.of(context).size.width;
    if (myMenu.isEmpty) {
      return Scaffold(
        appBar: AppBar(
          title: Text(
            'My Menu',
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
            : Center(
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
      );
    }
    return Scaffold(
      appBar: AppBar(
        title: Text(
          'My Menu',
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
          : GridView.builder(
              controller: _scrollController,
              gridDelegate: const SliverGridDelegateWithFixedCrossAxisCount(
                crossAxisCount: 2,
                crossAxisSpacing: 8.0,
                mainAxisSpacing: 8.0,
              ),
              itemCount: myMenu.length,
              itemBuilder: (context, index) {
                var recipe = myMenu[index];
                return GestureDetector(
                  onTap: () {
                    print("${myMenu[0]}");
                    Navigator.push(
                      context,
                      MaterialPageRoute(
                        builder: (context) => DetailMyMenuPage(
                          recipe: recipe,
                          userID: widget.userID,
                        ),
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
                          Text(
                            recipe['menuName'],
                            style: GoogleFonts.mali(
                              fontSize: 16,
                              fontWeight: FontWeight.bold,
                              color: Colors.black,
                            ),
                            textAlign: TextAlign.center,
                          ),
                          const SizedBox(height: 8.0),
                          Text(
                            'public Status: ${recipe['publicStatus']}',
                            style: GoogleFonts.mali(
                              fontSize: 12,
                              color: Colors.black,
                            ),
                            textAlign: TextAlign.center,
                          ),
                        ],
                      ),
                    ),
                  ),
                );
              },
            ),
    );
  }
}
