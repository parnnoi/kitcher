import 'package:flutter/material.dart';
import 'package:google_fonts/google_fonts.dart';
import 'detailmymenu.dart';

class MyMenuPage extends StatelessWidget {
  final List<Map<String, dynamic>> searchResults;
  final String? notFoundMessage;
  final int userID;
  const MyMenuPage(
      {Key? key,
      required this.searchResults,
      required this.userID,
      this.notFoundMessage})
      : super(key: key);

  @override
  Widget build(BuildContext context) {
    double screenWidth = MediaQuery.of(context).size.width;
    if (searchResults.isEmpty) {
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
        body: Center(
          child: Text(
            notFoundMessage ?? 'There is no menu yet. Try to add menu.',
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
      body: GridView.builder(
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
              print("${searchResults[0]}");
              Navigator.push(
                context,
                MaterialPageRoute(
                  builder: (context) => DetailMyMenuPage(
                    recipe: recipe,
                    userID: userID,
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
