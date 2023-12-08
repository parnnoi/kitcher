import 'package:flutter/material.dart';
import 'package:google_fonts/google_fonts.dart';
import 'detail.dart';

class CategoryPage extends StatelessWidget {
  final String category;
  final List<Map<String, dynamic>> searchResults;
  final int userID;
  final String statusMessage;

  const CategoryPage(
      {Key? key,
      required this.category,
      required this.searchResults,
      required this.userID,
      required this.statusMessage})
      : super(key: key);

  @override
  Widget build(BuildContext context) {
    double screenWidth = MediaQuery.of(context).size.width;
    return Scaffold(
      appBar: AppBar(
        title: Text(
          category,
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
      body: statusMessage.isNotEmpty
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
          : GridView.builder(
              gridDelegate: const SliverGridDelegateWithFixedCrossAxisCount(
                crossAxisCount: 2,
                crossAxisSpacing: 8.0,
                mainAxisSpacing: 8.0,
              ),
              itemCount: searchResults.length,
              itemBuilder: (context, index) {
                var recipe = searchResults[index];
                return GestureDetector(
                  onTap: () {
                    Navigator.push(
                      context,
                      MaterialPageRoute(
                        builder: (context) =>
                            DetailPage(recipe: recipe, userID: userID),
                      ),
                    );
                  },
                  child: Padding(
                      padding: const EdgeInsets.all(16),
                      child: Stack(children: [
                        Container(
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
                      ])),
                );
              },
            ),
    );
  }
}
