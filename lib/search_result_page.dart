import 'package:flutter/material.dart';
import 'package:google_fonts/google_fonts.dart';
import 'detail.dart';
import 'dart:convert';
import 'package:http/http.dart' as http;

class SearchResultsPage extends StatefulWidget {
  final List<Map<String, dynamic>> searchResults;
  final int userID;
  final String searchTerms;
  const SearchResultsPage({
    Key? key,
    required this.searchTerms,
    required this.searchResults,
    required this.userID,
  }) : super(key: key);

  @override
  // ignore: library_private_types_in_public_api
  _SearchResultsPageState createState() => _SearchResultsPageState();
}

class _SearchResultsPageState extends State<SearchResultsPage> {
  int currentPage = 1;
  String statusMessage = '';
  bool isLoading = true;
  List<Map<String, dynamic>> recipes = [];
  final ScrollController _scrollController = ScrollController();

  @override
  void initState() {
    super.initState();
    _searchRecipes(widget.searchTerms, widget.userID);
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
      _loadMoreData(widget.searchTerms);
    }
  }

  Future<void> _searchRecipes(String searchTerm, int uID) async {
    final Uri uri = Uri.parse(
        'https://kitcherfromlocal.vercel.app/api/menu/name/$searchTerm/1');

    final Map<String, dynamic> user = {
      "uid": uID,
    };

    final http.Response response = await http.post(
      uri,
      headers: {'Content-Type': 'application/json'},
      body: jsonEncode(user),
    );

    if (response.statusCode == 200) {
      final List<dynamic> searchResults = jsonDecode(response.body);
      setState(() {
        recipes = searchResults.cast<Map<String, dynamic>>();
        isLoading = false;
      });
      // Navigate to the search results page
    } else if (response.statusCode == 404) {
      setState(() {
        statusMessage = 'Not found';
        isLoading = false;
      });
    } else {
      // Handle error
      isLoading = false;
      print('Failed to fetch recipes. Status code: ${response.statusCode}');
    }
  }

  Future<void> _loadMoreData(String searchTerm) async {
    // Increment the page number
    currentPage++;

    final Uri uri = Uri.parse(
        'https://kitcherfromlocal.vercel.app/api/menu/name/$searchTerm/$currentPage');

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
        widget.searchResults
            .addAll(additionalData.cast<Map<String, dynamic>>());
      });
    } else {
      // Handle error
      print('Failed to load more data. Status code: ${response.statusCode}');
    }
  }

  @override
  Widget build(BuildContext context) {
    double screenWidth = MediaQuery.of(context).size.width;

    print('${widget.searchResults}');
    return Scaffold(
      appBar: AppBar(
        title: Text(
          widget.searchTerms,
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
          : statusMessage.isNotEmpty
              ? Center(
                  child: Text(
                    statusMessage,
                    textAlign: TextAlign.center,
                    style: GoogleFonts.mali(
                      fontSize: 18,
                      fontWeight: FontWeight.bold,
                      color: Colors.black,
                    ),
                  ),
                )
              : Column(
                  children: [
                    Expanded(
                      child: GridView.builder(
                        controller:
                            _scrollController, // Assign the controller to the GridView
                        gridDelegate:
                            const SliverGridDelegateWithFixedCrossAxisCount(
                          crossAxisCount: 2,
                          crossAxisSpacing: 8.0,
                          mainAxisSpacing: 8.0,
                        ),
                        itemCount: widget.searchResults.length,
                        itemBuilder: (context, index) {
                          var recipe = widget.searchResults[index];
                          return GestureDetector(
                            onTap: () {
                              Navigator.push(
                                context,
                                MaterialPageRoute(
                                  builder: (context) => DetailPage(
                                      recipe: recipe, userID: widget.userID),
                                ),
                              );
                            },
                            child: Padding(
                              padding: const EdgeInsets.all(16),
                              child: Container(
                                decoration: BoxDecoration(
                                  borderRadius: BorderRadius.circular(20),
                                  color:
                                      const Color.fromARGB(255, 255, 254, 235),
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
                                    )
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
    );
  }
}