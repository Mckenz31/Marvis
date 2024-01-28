import 'package:flutter/material.dart';
import 'package:http/http.dart' as http;
import 'dart:convert';

class ChatScreen extends StatefulWidget {
  const ChatScreen({Key? key}) : super(key: key);

  @override
  State<ChatScreen> createState() {
    return _ChatScreen();
  }
}

class _ChatScreen extends State<ChatScreen> {
  List<Message> messages = [];
  Set<int> selectedMessages = {}; // Keep track of selected message indices
  TextEditingController messageController = TextEditingController();

  @override
  Widget build(BuildContext context) {
    return Scaffold(
      appBar: AppBar(
        title: const Text('Warvis'),
        centerTitle: true,
        backgroundColor: Colors.blue,
      ),
      body: Column(
        children: [
          Expanded(
            child: ListView.builder(
              reverse: true,
              itemCount: messages.length,
              itemBuilder: (context, index) {
                final message = messages[index];
                return GestureDetector(
                  onTap: () {
                    _toggleMessageSelection(index);
                  },
                  child: Align(
                    alignment: message.isSentByMe
                        ? Alignment.centerRight
                        : Alignment.centerLeft,
                    child: Container(
                      margin: const EdgeInsets.symmetric(
                          vertical: 5, horizontal: 10),
                      padding: const EdgeInsets.symmetric(
                          vertical: 10, horizontal: 15),
                      decoration: BoxDecoration(
                        color: _getMessageBackgroundColor(index),
                        borderRadius: BorderRadius.circular(20),
                        boxShadow: [
                          BoxShadow(
                            color: Colors.grey.withOpacity(0.5),
                            spreadRadius: 2,
                            blurRadius: 3,
                            offset: Offset(0, 2),
                          ),
                        ],
                      ),
                      child: Text(
                        message.text,
                        style: TextStyle(
                          color: message.isSentByMe
                              ? Colors.white
                              : Colors.black,
                        ),
                      ),
                    ),
                  ),
                );
              },
            ),
          ),
          Padding(
            padding: const EdgeInsets.all(8.0),
            child: Row(
              children: [
                Expanded(
                  child: TextField(
                    controller: messageController,
                    decoration: InputDecoration(
                      hintText: "Type a message",
                      border: OutlineInputBorder(
                        borderRadius: BorderRadius.circular(20),
                      ),
                    ),
                  ),
                ),
                IconButton(
                  icon: const Icon(Icons.send),
                  color: Colors.blueGrey,
                  onPressed: _sendMessage,
                ),
              ],
            ),
          ),
        ],
      ),
      floatingActionButton: selectedMessages.isNotEmpty
          ? FloatingActionButton(
              onPressed: _saveSelectedMessages,
              child: const Icon(Icons.save),
            )
          : null,
    );
  }

  void _sendMessage() async {
    if (messageController.text.isNotEmpty) {
      // Insert user's message into the list
      setState(() {
        messages.insert(0, Message(messageController.text, true));
        messages.insert(0, Message("Cross communication is coming soon", false));
      });

      // Prepare data for the API request
      String tokenJson = Uri.encodeFull(
          "{'token': 'ya29.a0AfB_byAYlq8a29oXXMIoHuMGzziQ1KVIgNqHcNdqV55xiziQ0IDO2I5roVYiVUgcoHYG4n2tjv5a0WonDzWuEQErPp5X-B9tVafuYq-xqc8pMW1x1JPwOiFmoIekuvI1ukk93BAZZF7E3UndkuFas2TDvXtY32bEp95XtQaCgYKAdwSAQ4SFQHGX2MiQ0NC-z70Wf67aUNHPVwi8A0173', 'refresh_token': '1//0flnRR4eyc3BdCgYIARAAGA8SNwF-L9IrhzGAIw89AmhLorjxRaTS4w6RhNOAc3PLW4aHK3r5Dv2L0lZuBHvGogZIiCDVWVw3_F0', 'token_uri': 'https://oauth2.googleapis.com/token', 'client_id': '41098689972-ga1pactc1udgsa93ikntit74rbn6lhuf.apps.googleusercontent.com', 'client_secret': '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', 'scopes': ['https://www.googleapis.com/auth/gmail.compose', 'https://www.googleapis.com/auth/gmail.readonly', 'https://www.googleapis.com/auth/calendar'], 'universe_domain': 'googleapis.com', 'account': "", 'expiry': '2024-01-28T08:42:07.612709Z'}");

      // Extract the chat history from the list of messages
      List<String> chatHistory =
          messages.map((message) => message.text).toList();
      String chatHistoryJson = jsonEncode(chatHistory);

      // Construct the API endpoint
      String apiUrl =
          "http://localhost:8080/chat?google_user_file=$tokenJson&chat_history=$chatHistoryJson";

      try {
        // Make the GET request to the API
        final response = await http.get(Uri.parse(apiUrl));

        // Check if the request was successful
        if (response.statusCode == 200) {
          // Handle the response here if needed
          print("API response: ${response.body}");
        } else {
          // Handle the error response if needed
          print("API request failed with status: ${response.statusCode}");
        }
      } catch (e) {
        // Handle any exceptions that may occur during the request
        print("Error during API request: $e");
      }

      // Clear the message input field
      messageController.clear();
    }
  }

  void _toggleMessageSelection(int index) {
    setState(() {
      if (selectedMessages.contains(index)) {
        selectedMessages.remove(index);
      } else {
        selectedMessages.add(index);
      }
    });
  }

  void _saveSelectedMessages() {
    // Implement logic to save selected messages
    List<Message> selectedMessagesList =
        selectedMessages.map((index) => messages[index]).toList();
    // Do something with selected messages, e.g., save them to storage or display in a dialog
    print("Selected Messages: ${selectedMessagesList.map((m) => m.text)}");
  }

  Color _getMessageBackgroundColor(int index) {
    return selectedMessages.contains(index)
        ? Colors.blueAccent
        : messages[index].isSentByMe
            ? Colors.green
            : Colors.grey[300]!;
  }
}

class Message {
  String text;
  bool isSentByMe;

  Message(this.text, this.isSentByMe);
}
