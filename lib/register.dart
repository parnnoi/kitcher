// ignore_for_file: use_build_context_synchronously, avoid_print, unnecessary_string_interpolations

import 'package:flutter/material.dart';
import 'package:http/http.dart' as http;
import 'package:google_fonts/google_fonts.dart';
import 'dart:convert';
import 'package:kitcher/login.dart';

class RegisterPage extends StatefulWidget {
  const RegisterPage({Key? key}) : super(key: key);

  @override
  State<RegisterPage> createState() => _RegisterPageState();
}

class _RegisterPageState extends State<RegisterPage> {
  final TextEditingController _fNameController = TextEditingController();
  final TextEditingController _lNameController = TextEditingController();
  final TextEditingController _emailController = TextEditingController();
  final TextEditingController _telnoController = TextEditingController();
  final TextEditingController _usernameController = TextEditingController();
  final TextEditingController _passwordController = TextEditingController();

  @override
  void initState() {
    super.initState();

    // Fetch recommended menu data when the widget is initialized
  }

  Future<void> _registerUser() async {
    final BuildContext currentContext = context;
    final Uri uri =
        Uri.parse('https://kitcherfromlocal.vercel.app/api/register');
    final Map<String, dynamic> requestData = {
      "fName": _fNameController.text,
      "lName": _lNameController.text,
      "email": _emailController.text,
      "telno": _telnoController.text,
      "username": _usernameController.text,
      "password": _passwordController.text,
      "role": "U",
    };
    final username = _usernameController.text;
    print('$username');
    try {
      // Check if the username is available before registering
      bool isUsernameAvailable = await checkUsernameAvailability(username);

      if (isUsernameAvailable) {
        // Username is available, proceed with registration
        final http.Response response = await http.post(
          uri,
          headers: {'Content-Type': 'application/json'},
          body: jsonEncode(requestData),
        );

        if (response.statusCode == 200) {
          // Registration successful, navigate to verification page
          Navigator.pushReplacement(
            currentContext, // Use the stored context
            MaterialPageRoute(
              builder: (_) => const LoginDemo(),
            ),
          );
        } else {
          // Registration failed, handle the error
          showDialog(
            context: context,
            builder: (BuildContext context) {
              return AlertDialog(
                title: Text(
                  'Have empty value',
                  style: GoogleFonts.mali(
                    fontWeight: FontWeight.bold,
                    color: Colors.black,
                  ),
                ),
                content: Text(
                  'Please put the information.',
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
          print(
              'User registration failed. Status code: ${response.statusCode}');
        }
      } else {
        // Username is not available, show an error message or take appropriate action
        showDialog(
          context: context,
          builder: (BuildContext context) {
            return AlertDialog(
              title: Text(
                'Username Not Available',
                style: GoogleFonts.mali(
                  fontWeight: FontWeight.bold,
                  color: Colors.black,
                ),
              ),
              content: Text(
                'Please choose a different username.',
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
        print('Username is not available');
      }
    } catch (error) {
      print('Error during user registration: $error');
    }
  }

  Future<bool> checkUsernameAvailability(String username) async {
    final Uri uri =
        Uri.parse('https://kitcherfromlocal.vercel.app/api/register/$username');

    try {
      final http.Response response = await http.get(uri);
      print('${response.body}');
      print('${response.statusCode}');
      if (response.statusCode == 200) {
        // Username is exists
        return false;
      } else if (response.statusCode == 404) {
        // Username is not exists
        return true;
      } else {
        // have issues
        return false;
      }
    } catch (error) {
      // Handle the error, e.g., network issues
      print('Error checking username availability: $error');
      return false;
    }
  }

  @override
  Widget build(BuildContext context) {
    return Scaffold(
      backgroundColor: const Color.fromARGB(255, 255, 251, 193),
      appBar: AppBar(
        title: Text(
          'Register',
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
        child: Padding(
          padding: const EdgeInsets.all(16.0),
          child: Column(
            children: <Widget>[
              Padding(
                padding: const EdgeInsets.only(left: 15, right: 15, top: 10),
                child: TextField(
                  controller: _usernameController,
                  cursorColor: Colors.black,
                  obscureText: false,
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
                  ),
                ),
              ),
              Padding(
                padding: const EdgeInsets.only(left: 15, right: 15, top: 10),
                child: TextField(
                  controller: _emailController,
                  cursorColor: Colors.black,
                  obscureText: false,
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
                    labelText: 'Email',
                    labelStyle: TextStyle(color: Colors.black),
                  ),
                ),
              ),
              Padding(
                padding: const EdgeInsets.only(left: 15, right: 15, top: 10),
                child: TextField(
                  controller: _fNameController,
                  cursorColor: Colors.black,
                  obscureText: false,
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
                    labelText: 'First Name',
                    labelStyle: TextStyle(color: Colors.black),
                  ),
                ),
              ),
              Padding(
                padding: const EdgeInsets.only(left: 15, right: 15, top: 10),
                child: TextField(
                  controller: _lNameController,
                  cursorColor: Colors.black,
                  obscureText: false,
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
                    labelText: 'Last Name',
                    labelStyle: TextStyle(color: Colors.black),
                  ),
                ),
              ),
              Padding(
                padding: const EdgeInsets.only(left: 15, right: 15, top: 10),
                child: TextField(
                  controller: _telnoController,
                  cursorColor: Colors.black,
                  obscureText: false,
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
                    labelText: 'Telephone Number',
                    labelStyle: TextStyle(color: Colors.black),
                  ),
                ),
              ),
              Padding(
                padding: const EdgeInsets.only(top: 16),
                child: Container(
                  height: 50,
                  width: 250,
                  decoration: BoxDecoration(
                    color: const Color.fromARGB(255, 255, 225, 136),
                    borderRadius: BorderRadius.circular(20),
                  ),
                  child: TextButton(
                    onPressed: _registerUser,
                    child: Text(
                      'Sign Up',
                      style: GoogleFonts.mali(
                        fontSize: 24,
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
    );
  }
}
