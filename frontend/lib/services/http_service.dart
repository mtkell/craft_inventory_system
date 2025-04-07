import 'dart:convert';
import 'package:http/http.dart' as http;
import 'package:flutter_secure_storage/flutter_secure_storage.dart';

class HttpService {
  final String baseUrl = 'http://your-backend-url/api';
  final FlutterSecureStorage storage = FlutterSecureStorage();

  Future<Map<String, String>> _getHeaders() async {
    String? token = await storage.read(key: 'jwt_token');
    return {
      'Authorization': 'Bearer $token',
      'Content-Type': 'application/json',
    };
  }

  Future<dynamic> login(String username, String password) async {
    final response = await http.post(
      Uri.parse('$baseUrl/auth/login'),
      headers: {'Content-Type': 'application/json'},
      body: json.encode({'username': username, 'password': password}),
    );

    if (response.statusCode == 200) {
      final data = json.decode(response.body);
      await storage.write(key: 'jwt_token', value: data['access_token']);
      return data;
    } else {
      throw Exception('Failed to login');
    }
  }

  Future<dynamic> register(
    String username,
    String password,
    String role,
  ) async {
    final response = await http.post(
      Uri.parse('$baseUrl/auth/register'),
      headers: {'Content-Type': 'application/json'},
      body: json.encode({
        'username': username,
        'password': password,
        'role': role,
      }),
    );

    if (response.statusCode == 201) {
      return json.decode(response.body);
    } else {
      throw Exception('Failed to register');
    }
  }

  Future<dynamic> getInventory() async {
    final response = await http.get(
      Uri.parse('$baseUrl/inventory'),
      headers: await _getHeaders(),
    );
    if (response.statusCode == 200) {
      return json.decode(response.body);
    } else {
      throw Exception('Failed to fetch inventory');
    }
  }
}
