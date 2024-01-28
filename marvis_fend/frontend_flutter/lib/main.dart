import "package:frontend_flutter/pages/chatscreen.dart";
import "package:flutter/material.dart";
import "package:frontend_flutter/pages/home.dart";

var kColorScheme = ColorScheme.fromSeed(
  seedColor: const Color.fromARGB(255, 203, 63, 228),
);

var kDarkColorScheme = ColorScheme.fromSeed(
    brightness: Brightness.dark,
    seedColor: const Color.fromARGB(255, 221, 147, 236)
);

void main() {
  runApp(
    MaterialApp(
      debugShowCheckedModeBanner: false,
      home: Home(),
    ),
  );
}


