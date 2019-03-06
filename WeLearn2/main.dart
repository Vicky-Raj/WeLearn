import 'package:flutter/material.dart';
import 'package:http/http.dart' as http;
import 'dart:convert';

void main(){
  runApp(MaterialApp(
    debugShowCheckedModeBanner: false,
    home: HomePage(),
  )); 
}


class HomePage extends StatefulWidget {
  @override
  _HomePageState createState() => _HomePageState();
}

class _HomePageState extends State<HomePage> {

   getData()async{
    var response = await http.get('https://jsonplaceholder.typicode.com/users');
    var result = jsonDecode(response.body);
    return result;
  }
 
  @override
  Widget build(BuildContext context) {
    return Scaffold(
      appBar: AppBar(title: Text('Test'),centerTitle: true,),
      body:FutureBuilder(
    future: getData(), // a previously-obtained Future<String> or null
    builder: (BuildContext context, snapshot) {
    switch (snapshot.connectionState) {
      case ConnectionState.none:
        return CircularProgressIndicator();
      case ConnectionState.active:
      case ConnectionState.waiting:
        return CircularProgressIndicator();
      case ConnectionState.done:
        return ListView.builder(
          itemCount: 10,
          itemBuilder: (context, index){
            return ListTile(
              title: Text(snapshot.data[index]['name']),
            );
          },
        );
    }// unreachable
  },
)
    );
  }
}