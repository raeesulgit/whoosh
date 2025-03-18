import 'package:flutter/material.dart';
import 'package:udemy/gradient_container.dart';

void main() {
  runApp(MaterialApp(
    home:Scaffold(
      body:GradientContainer(
        colours : [Color.fromARGB(255, 69, 5, 115), Color.fromARGB(255, 21, 1, 35)]
        )
        ,
    )
  ));
}
