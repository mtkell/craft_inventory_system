import 'package:flutter/material.dart';
import 'package:craft_inventory_system/screens/material_list_screen.dart'; // Import Material List Screen
import 'package:craft_inventory_system/screens/low_stock_screen.dart'; // Import Low Stock Screen

class InventoryScreen extends StatelessWidget {
  @override
  Widget build(BuildContext context) {
    return Scaffold(
      appBar: AppBar(
        title: Text('Inventory Management'),
        actions: [
          IconButton(
            icon: Icon(Icons.list),
            onPressed: () {
              // Navigate to the Material List Screen
              Navigator.push(
                context,
                MaterialPageRoute(builder: (context) => MaterialListScreen()),
              );
            },
          ),
          IconButton(
            icon: Icon(Icons.warning),
            onPressed: () {
              // Navigate to the Low Stock Screen
              Navigator.push(
                context,
                MaterialPageRoute(builder: (context) => LowStockScreen()),
              );
            },
          ),
        ],
      ),
      body: Center(
        child: Column(
          mainAxisAlignment: MainAxisAlignment.center,
          children: <Widget>[
            Text(
              'Welcome to Inventory Management',
              style: TextStyle(fontSize: 24),
            ),
            SizedBox(height: 20),
            ElevatedButton(
              onPressed: () {
                // Navigate to the Material List Screen
                Navigator.push(
                  context,
                  MaterialPageRoute(builder: (context) => MaterialListScreen()),
                );
              },
              child: Text('View Materials'),
            ),
            ElevatedButton(
              onPressed: () {
                // Navigate to the Low Stock Screen
                Navigator.push(
                  context,
                  MaterialPageRoute(builder: (context) => LowStockScreen()),
                );
              },
              child: Text('View Low Stock Materials'),
            ),
          ],
        ),
      ),
    );
  }
}
