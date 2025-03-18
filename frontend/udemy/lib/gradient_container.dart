import 'package:flutter/material.dart';
import 'package:udemy/styled_text.dart';
import 'dart:math';

const startAlighnment = Alignment.topLeft;
const endAlighnment = Alignment.bottomRight;

class GradientContainer extends StatefulWidget {
  GradientContainer({super.key, required this.colours});
  final List<Color> colours;

  @override
  State<GradientContainer> createState() => _GradientContainerState();
}

class _GradientContainerState extends State<GradientContainer> {
  List<String> images = ['dice-1', 'dice-2', 'dice-3', 'dice-4'];
  String image = "assets/images/dice-1.png";
  Widget build(ctx) {
    Random random = Random();
    return Container(
      decoration: BoxDecoration(
        gradient: LinearGradient(
          colors: widget.colours,
          begin: startAlighnment,
          end: endAlighnment,
        ),
      ),
      child: Center(
        child: Column(
          mainAxisAlignment: MainAxisAlignment.center,
          crossAxisAlignment: CrossAxisAlignment.center,
          children: [
            Image.asset(
              image,
              width: 100,
              ),
            TextButton(
              style: TextButton.styleFrom( foregroundColor: Colors.white, padding: EdgeInsets.all(10)),
              onPressed: (){
          setState(() {
              image = "assets/images/"+images[random.nextInt(images.length)]+".png";
              });
            }, 
            child:Text("Dice random", style: TextStyle(fontSize: 20),)
            )
          ],
        ),
      ),
    );
  }
}
