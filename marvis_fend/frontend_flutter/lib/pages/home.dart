import 'package:flutter/material.dart';
import 'package:frontend_flutter/pages/chatscreen.dart';

class Home extends StatelessWidget {
  @override
  Widget build(BuildContext context) {
    return Scaffold(
      backgroundColor: Colors.blueGrey[900],
      body: Center(
        child: Padding(
          padding: const EdgeInsets.all(16.0),
          child: Column(
            mainAxisAlignment: MainAxisAlignment.center,
            children: [
              const Text(
                'Warvis',
                style: TextStyle(
                  color: Colors.white,
                  fontSize: 48.0,
                  fontWeight: FontWeight.bold,
                ),
              ),
              const SizedBox(height: 20.0),
              const Text(
                'Too much to deal with?\nYour personal assistant is here to help!',
                textAlign: TextAlign.center,
                style: TextStyle(
                  color: Colors.white,
                  fontSize: 16.0,
                ),
              ),
              const SizedBox(height: 40.0),
              Container(
                width: 180.0,
                height: 40.0,
                decoration: BoxDecoration(
                  color: Colors.blueAccent,
                  borderRadius: BorderRadius.circular(10.0),
                  boxShadow: [
                    BoxShadow(
                      color: Colors.blueAccent.withOpacity(0.5),
                      spreadRadius: 3,
                      blurRadius: 5,
                      offset: const Offset(0, 3),
                    ),
                  ],
                ),
                child: InkWell(
                  onTap: () {
                    Navigator.of(context).push(MaterialPageRoute(builder: (context)=>const ChatScreen()));
                  },
                  child: const Center(
                    child: Text(
                      'Start Chat',
                      style: TextStyle(
                        color: Colors.white,
                        fontSize: 16.0,
                        fontWeight: FontWeight.bold,
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