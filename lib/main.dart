
import "package:flutter/material.dart";
import "package:flutter_frontend/pages/chatscreen.dart";
import "package:flutter_frontend/pages/speech2text.dart";

var kColorScheme = ColorScheme.fromSeed(
  seedColor: const Color.fromARGB(255, 203, 63, 228),
);

var kDarkColorScheme = ColorScheme.fromSeed(
    brightness: Brightness.dark,
    seedColor: const Color.fromARGB(255, 221, 147, 236)
);

void main() {
  runApp(
    const MaterialApp(
      debugShowCheckedModeBanner: false,
      home: SpeechToTextPage(),
    ),
  );
}


