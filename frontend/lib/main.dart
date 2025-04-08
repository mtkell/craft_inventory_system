import 'package:flutter/material.dart';
import 'screens/login_screen.dart';
import 'screens/register_screen.dart';
import 'screens/inventory_screen.dart';
import 'screens/material_list_screen.dart'; // Import for Material List Screen
import 'screens/low_stock_screen.dart'; // Import for Low Stock Screen

void main() {
  runApp(MyApp());
}

class MyApp extends StatelessWidget {
  @override
  Widget build(BuildContext context) {
    return MaterialApp(
      title: 'Craft Inventory System',
      initialRoute: '/login',
      routes: {
        '/login': (context) => LoginScreen(),
        '/register': (context) => RegisterScreen(),
        '/inventory': (context) => InventoryScreen(),
        '/material-list':
            (context) => MaterialListScreen(), // Route for Material List Screen
        '/low-stock':
            (context) => LowStockScreen(), // Route for Low Stock Screen
      },
    );
  }
}
