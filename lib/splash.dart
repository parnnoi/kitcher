import 'package:splash_screen_view/SplashScreenView.dart';
import 'login.dart';
import 'package:flutter/material.dart';

class Splash extends StatefulWidget {
  static const routeName = '/';
  const Splash({Key? key}) : super(key: key);

  @override
  _SplashState createState() => _SplashState();
}

class _SplashState extends State<Splash> {
  @override
  Widget build(BuildContext context) {
    return SplashScreenView(
      navigateRoute: const LoginDemo(),
      duration: 5000,
      imageSize: 600,
      imageSrc: "assets/kitcher_intro.png",
      backgroundColor: const Color.fromARGB(255, 255, 251, 193),
    );
  }
}
