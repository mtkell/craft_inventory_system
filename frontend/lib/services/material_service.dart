import 'dart:convert';
import 'package:http/http.dart' as http;
import 'package:flutter/material.dart';
import '../models/material.dart';

class MaterialService {
  final String baseUrl = 'http://your-api-url.com/materials';

  Future<List<Material>> fetchMaterials() async {
    final response = await http.get(Uri.parse('$baseUrl/'));

    if (response.statusCode == 200) {
      List<dynamic> data = json.decode(response.body);
      return data.map((item) => Material.fromJson(item)).toList();
    } else {
      throw Exception('Failed to load materials');
    }
  }

  Future<Material> restockMaterial(
    int materialId,
    double quantity,
    String note,
  ) async {
    final response = await http.post(
      Uri.parse('$baseUrl/restock/'),
      headers: {'Content-Type': 'application/json'},
      body: json.encode({
        'material_id': materialId,
        'quantity': quantity,
        'note': note,
      }),
    );

    if (response.statusCode == 200) {
      return Material.fromJson(json.decode(response.body));
    } else {
      throw Exception('Failed to restock material');
    }
  }
}
