import 'package:flutter/material.dart';
import 'package:whooshapp/screens/service_list_screens.dart';  // ✅ Package import

void main() {
  runApp(MyApp());
}

class MyApp extends StatelessWidget {
  @override
  Widget build(BuildContext context) {
    return MaterialApp(
      title: 'Vehicle Services',
      color: Colors.white,
      home: ServiceListScreen(),
    );
  }
}
