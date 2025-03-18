import 'dart:convert';
import 'package:http/http.dart' as http;
import '../models/service.dart';

class ApiService {
  static const String baseUrl = 'http://localhost:8000';  // Change if needed

  Future<List<Service>> fetchServices() async {
    final response = await http.get(Uri.parse('$baseUrl/services'));

    if (response.statusCode == 200) {
      List<dynamic> data = jsonDecode(response.body);
      return data.map((json) => Service.fromJson(json)).toList();
    } else {
      throw Exception('Failed to load services');
    }
  }
}
