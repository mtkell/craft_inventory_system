import 'package:flutter/material.dart';
import '../services/material_service.dart';
import '../models/material.dart';

class LowStockScreen extends StatefulWidget {
  @override
  _LowStockScreenState createState() => _LowStockScreenState();
}

class _LowStockScreenState extends State<LowStockScreen> {
  late Future<List<Material>> futureLowStock;

  @override
  void initState() {
    super.initState();
    futureLowStock = MaterialService().fetchLowStockMaterials();
  }

  @override
  Widget build(BuildContext context) {
    return Scaffold(
      appBar: AppBar(title: Text('Low Stock Materials')),
      body: FutureBuilder<List<Material>>(
        future: futureLowStock,
        builder: (context, snapshot) {
          if (snapshot.connectionState == ConnectionState.waiting) {
            return Center(child: CircularProgressIndicator());
          } else if (snapshot.hasError) {
            return Center(child: Text('Error: ${snapshot.error}'));
          } else if (!snapshot.hasData || snapshot.data!.isEmpty) {
            return Center(child: Text('No low stock materials'));
          } else {
            final materials = snapshot.data!;
            return ListView.builder(
              itemCount: materials.length,
              itemBuilder: (context, index) {
                final material = materials[index];
                return ListTile(
                  title: Text(material.name),
                  subtitle: Text(
                    'Quantity: ${material.quantity} ${material.unit}',
                  ),
                );
              },
            );
          }
        },
      ),
    );
  }
}
