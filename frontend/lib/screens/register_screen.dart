import 'package:flutter/material.dart';
import 'package:your_app/services/http_service.dart';

class RegisterScreen extends StatefulWidget {
  @override
  _RegisterScreenState createState() => _RegisterScreenState();
}

class _RegisterScreenState extends State<RegisterScreen> {
  final HttpService _httpService = HttpService();
  final TextEditingController _usernameController = TextEditingController();
  final TextEditingController _passwordController = TextEditingController();
  final TextEditingController _roleController = TextEditingController();

  Future<void> _register() async {
    try {
      final username = _usernameController.text;
      final password = _passwordController.text;
      final role = _roleController.text;
      await _httpService.register(username, password, role);
      Navigator.pushReplacementNamed(context, '/login'); // Go to login screen
    } catch (e) {
      ScaffoldMessenger.of(
        context,
      ).showSnackBar(SnackBar(content: Text('Registration failed')));
    }
  }

  @override
  Widget build(BuildContext context) {
    return Scaffold(
      appBar: AppBar(title: Text("Register")),
      body: Padding(
        padding: EdgeInsets.all(16.0),
        child: Column(
          children: [
            TextField(
              controller: _usernameController,
              decoration: InputDecoration(labelText: "Username"),
            ),
            TextField(
              controller: _passwordController,
              obscureText: true,
              decoration: InputDecoration(labelText: "Password"),
            ),
            TextField(
              controller: _roleController,
              decoration: InputDecoration(labelText: "Role (admin/operator)"),
            ),
            SizedBox(height: 20),
            ElevatedButton(onPressed: _register, child: Text("Register")),
          ],
        ),
      ),
    );
  }
}
