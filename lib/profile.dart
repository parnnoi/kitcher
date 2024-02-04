import 'package:flutter/material.dart';
import 'package:google_fonts/google_fonts.dart';
import 'login.dart';
import 'mymenu.dart';
import 'myfav.dart';

class MyProfile extends StatelessWidget {
  const MyProfile({Key? key}) : super(key: key);

  @override
  Widget build(BuildContext context) {
    return MaterialApp(
      title: 'Flutter Demo',
      theme: ThemeData(
        scaffoldBackgroundColor: const Color.fromARGB(255, 255, 251, 193),
      ),
      home: const MyProfilePage(info: []),
    );
  }
}

class MyProfilePage extends StatefulWidget {
  const MyProfilePage({Key? key, required this.info}) : super(key: key);

  final List<Map<String, dynamic>> info;

  @override
  State<MyProfilePage> createState() => _MyProfilePageState(info: info);
}

class _MyProfilePageState extends State<MyProfilePage> {
  List<Map<String, dynamic>> info;
  List<Map<String, dynamic>> myMenu = [];
  List<Map<String, dynamic>> myFav = [];

  // Extract user data from the info list
  String getData(String key) {
    return info.isNotEmpty ? info[0][key] ?? '' : '';
  }

  int getUID() {
    return info.isNotEmpty ? info[0]['uid'] : 0;
  }

  _MyProfilePageState({required this.info});

  @override
  Widget build(BuildContext context) {
    double screenWidth = MediaQuery.of(context).size.width;
    return Scaffold(
      appBar: AppBar(
        iconTheme: const IconThemeData(
          color: Colors.black, // Change the color of the back button
        ),
        backgroundColor: const Color.fromARGB(255, 255, 251, 193),
        elevation: 0,
      ),
      body: SingleChildScrollView(
        child: Column(
          children: <Widget>[
            IconButton(
              icon: const Icon(Icons.account_circle), // Profile icon
              iconSize: 200,
              color: const Color.fromARGB(255, 255, 225, 136), onPressed: () {},
            ),
            Row(
              mainAxisAlignment: MainAxisAlignment.center,
              children: [
                Padding(
                  padding: const EdgeInsets.only(right: 16),
                  child: Text(
                    getData('fName'),
                    style: GoogleFonts.mali(
                      fontSize: 32,
                      fontWeight: FontWeight.bold,
                      color: Colors.black,
                    ),
                  ),
                ),
                Text(
                  getData('lName'),
                  style: GoogleFonts.mali(
                    fontSize: 32,
                    fontWeight: FontWeight.bold,
                    color: Colors.black,
                  ),
                ),
              ],
            ),
            Padding(
              padding: const EdgeInsets.only(top: 10),
              child: Text(
                'Email : ${getData('email')}',
                style: GoogleFonts.mali(
                  fontSize: 18,
                  fontWeight: FontWeight.normal,
                  color: Colors.black,
                ),
              ),
            ),
            Text(
              'Tel No. : ${getData('telno')}',
              style: GoogleFonts.mali(
                fontSize: 18,
                fontWeight: FontWeight.normal,
                color: Colors.black,
              ),
            ),
            Padding(
                padding: const EdgeInsets.only(top: 30),
                child: Container(
                  height: 50,
                  width: screenWidth - 20,
                  decoration: BoxDecoration(
                      color: const Color.fromARGB(100, 255, 225, 136),
                      borderRadius: BorderRadius.circular(20)),
                  child: TextButton(
                    onPressed: () {
                      Navigator.push(
                        context,
                        MaterialPageRoute(
                          builder: (_) => MyMenuPage(
                            userID: getUID(),
                          ),
                        ),
                      );
                    },
                    child: Text(
                      'My Menu',
                      style: GoogleFonts.mali(
                        fontSize: 20,
                        fontWeight: FontWeight.bold,
                        color: Colors.black,
                      ),
                    ),
                  ),
                )),
            Padding(
                padding: const EdgeInsets.only(top: 5),
                child: Container(
                  height: 50,
                  width: screenWidth - 20,
                  decoration: BoxDecoration(
                      color: const Color.fromARGB(100, 255, 225, 136),
                      borderRadius: BorderRadius.circular(20)),
                  child: TextButton(
                    onPressed: () {
                      Navigator.push(
                        context,
                        MaterialPageRoute(
                          builder: (_) => MyFavPage(
                            userID: getUID(),
                          ),
                        ),
                      );
                    },
                    child: Text(
                      'My Favorite',
                      style: GoogleFonts.mali(
                        fontSize: 20,
                        fontWeight: FontWeight.bold,
                        color: Colors.black,
                      ),
                    ),
                  ),
                )),
            Padding(
              padding: const EdgeInsets.only(top: 30),
              child: Container(
                height: 50,
                width: 250,
                decoration: BoxDecoration(
                    color: const Color.fromARGB(255, 255, 225, 136),
                    borderRadius: BorderRadius.circular(20)),
                child: TextButton(
                  onPressed: () {
                    Navigator.pushReplacement(context,
                        MaterialPageRoute(builder: (_) => const LoginDemo()));
                  },
                  child: Text(
                    'Log Out',
                    style: GoogleFonts.mali(
                      fontSize: 24,
                      fontWeight: FontWeight.bold,
                      color: Colors.black,
                    ),
                  ),
                ),
              ),
            )
          ],
        ),
      ),
    );
  }
}
