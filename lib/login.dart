// ignore_for_file: avoid_print, use_build_context_synchronously, unnecessary_string_interpolations

import 'package:flutter/material.dart';
import 'package:flutter_svg/flutter_svg.dart';
import 'package:google_fonts/google_fonts.dart';
import 'HomePage.dart';
import 'dart:convert';
import 'package:http/http.dart' as http;
import 'register.dart';

class MyApp extends StatelessWidget {
  const MyApp({super.key});

  @override
  Widget build(BuildContext context) {
    return const MaterialApp(
      debugShowCheckedModeBanner: false,
      home: LoginDemo(),
    );
  }
}

class LoginDemo extends StatefulWidget {
  const LoginDemo({super.key});

  @override
  State<LoginDemo> createState() => _LoginDemoState();
}

class _LoginDemoState extends State<LoginDemo> {
  final TextEditingController _usernameController = TextEditingController();
  final TextEditingController _passwordController = TextEditingController();
  List<Map<String, dynamic>> userInfo = [];

  Future<void> _fetchUserInfo(int uID) async {
    final Uri uri =
        Uri.parse('https://kitcherfromlocal.vercel.app/api/login/$uID');

    try {
      final http.Response response = await http.get(uri);

      if (response.statusCode == 200) {
        final List<dynamic> user = jsonDecode(response.body);
        setState(() {
          userInfo = user.cast<Map<String, dynamic>>();
        });
        Navigator.pushReplacement(
          context,
          MaterialPageRoute(
            builder: (_) => MyHome(info: userInfo),
          ),
        );
      } else {
        // Handle error
        print(
            'Failed to fetch user information. Status code: ${response.statusCode}');
      }
    } catch (error) {
      // Handle error
      print('Error fetching user information: $error');
    }
  }

  Future<void> login() async {
    final Uri loginUri =
        Uri.parse('https://kitcherfromlocal.vercel.app/api/login');
    final Map<String, dynamic> loginData = {
      "username": _usernameController.text,
      "password": _passwordController.text,
    };

    try {
      final http.Response loginResponse = await http.post(
        loginUri,
        headers: {'Content-Type': 'application/json'},
        body: jsonEncode(loginData),
      );
      print('${jsonEncode(loginData)}');
      print('response : ${jsonDecode(loginResponse.body)}');
      print('${loginResponse.statusCode}');
      if (loginResponse.statusCode == 200) {
        // Login successful, get user info
        final List<dynamic> userDataList = jsonDecode(loginResponse.body);
        if (userDataList.isNotEmpty) {
          final Map<String, dynamic> userData = userDataList.first;
          // Check if 'uid' is present and not null
          if (userData.containsKey('uid') && userData['uid'] != null) {
            // Convert 'uid' to int before passing to _fetchUserInfo
            final int uid = userData['uid'];
            print("$uid");
            // Call fetchUserInfo with the user ID
            await _fetchUserInfo(uid);
          } else {
            print('Invalid response format: Missing or null uid');
          }
        } else {
          print('Invalid response format: Empty user data');
        }
      } else {
        // Login failed, handle the error
        showDialog(
            context: context,
            builder: (BuildContext context) {
              return AlertDialog(
                title: Text(
                  'Login Failed',
                  style: GoogleFonts.mali(
                    fontWeight: FontWeight.bold,
                    color: Colors.black,
                  ),
                ),
                content: Text(
                  'Invalid username or password',
                  style: GoogleFonts.mali(
                    fontWeight: FontWeight.normal,
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
                        fontSize: 16,
                        fontWeight: FontWeight.bold,
                        color: Colors.black,
                      ),
                    ),
                  ),
                ],
              );
            });
        print('Login failed. Status code: ${loginResponse.statusCode}');
      }
    } catch (error) {
      print('Error during login: $error');
    }
  }

  @override
  Widget build(BuildContext context) {
    return Scaffold(
      backgroundColor: const Color.fromARGB(255, 255, 251, 193),
      body: SingleChildScrollView(
        child: Padding(
          padding: const EdgeInsets.only(top: 60),
          child: Column(
            children: <Widget>[
              Padding(
                padding: const EdgeInsets.only(top: 70.0),
                child: Center(
                  child: ClipOval(
                    child: Container(
                      width: 390,
                      height: 200,
                      color: const Color.fromARGB(255, 255, 254, 235),
                      child: SvgPicture.asset(
                        'assets/kitcher_icon_login.svg',
                        fit: BoxFit.scaleDown,
                      ),
                    ),
                  ),
                ),
              ),
              Padding(
                padding: const EdgeInsets.only(left: 15, right: 15, top: 30),
                child: TextField(
                  controller: _usernameController,
                  cursorColor: Colors.black,
                  style: GoogleFonts.mali(
                    fontSize: 16,
                    fontWeight: FontWeight.normal,
                    color: Colors.black,
                  ),
                  decoration: const InputDecoration(
                    border: OutlineInputBorder(
                      borderRadius: BorderRadius.all(Radius.circular(30)),
                      borderSide: BorderSide(color: Colors.black),
                    ),
                    focusedBorder: OutlineInputBorder(
                      borderRadius: BorderRadius.all(Radius.circular(30)),
                      borderSide: BorderSide(
                          color: Colors.black), // Border color when focused
                    ),
                    labelText: 'Username',
                    labelStyle: TextStyle(color: Colors.black),
                    hintStyle: TextStyle(color: Colors.black),
                    hintText: 'Enter your username',
                  ),
                ),
              ),
              Padding(
                padding: const EdgeInsets.only(left: 15, right: 15, top: 10),
                child: TextField(
                  controller: _passwordController,
                  cursorColor: Colors.black,
                  obscureText: true,
                  style: GoogleFonts.mali(
                    fontSize: 16,
                    fontWeight: FontWeight.normal,
                    color: Colors.black,
                  ),
                  decoration: const InputDecoration(
                    border: OutlineInputBorder(
                      borderRadius: BorderRadius.all(Radius.circular(30)),
                      borderSide: BorderSide(color: Colors.black),
                    ),
                    focusedBorder: OutlineInputBorder(
                      borderRadius: BorderRadius.all(Radius.circular(30)),
                      borderSide: BorderSide(
                          color: Colors.black), // Border color when focused
                    ),
                    labelText: 'Password',
                    labelStyle: TextStyle(color: Colors.black),
                    hintStyle: TextStyle(color: Colors.black),
                    hintText: 'Enter your password',
                  ),
                ),
              ),
              Padding(
                padding: const EdgeInsets.only(top: 20),
                child: Container(
                  height: 50,
                  width: 250,
                  decoration: BoxDecoration(
                    color: const Color.fromARGB(255, 255, 225, 136),
                    borderRadius: BorderRadius.circular(20),
                  ),
                  child: TextButton(
                    onPressed: login,
                    child: Text(
                      'Log In',
                      style: GoogleFonts.mali(
                        fontSize: 24,
                        fontWeight: FontWeight.bold,
                        color: Colors.black,
                      ),
                    ),
                  ),
                ),
              ),
              Padding(
                padding: const EdgeInsets.only(left: 15, right: 15, top: 10),
                child: TextButton(
                  onPressed: () {
                    Navigator.push(
                      context,
                      MaterialPageRoute(
                        builder: (_) => const RegisterPage(),
                      ),
                    );
                    showDialog(
                      context: context,
                      builder: (BuildContext context) {
                        return AlertDialog(
                          title: Text(
                            'Notice for new user',
                            style: GoogleFonts.mali(
                              fontWeight: FontWeight.bold,
                              color: Colors.black,
                            ),
                          ),
                          content: Text(
                            'Don\'t use the real information.',
                            style: GoogleFonts.mali(
                              fontWeight: FontWeight.normal,
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
                                  fontSize: 16,
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
                  child: Text(
                    'New User? Create Account',
                    style: GoogleFonts.mali(
                      fontSize: 16,
                      fontWeight: FontWeight.normal,
                      color: Colors.black,
                    ),
                  ),
                ),
              ),
              Padding(
                padding: const EdgeInsets.only(left: 15, right: 15, top: 30),
                child: SvgPicture.asset('assets/kitcher_element_login.svg'),
              )
            ],
          ),
        ),
      ),
    );
  }
}
