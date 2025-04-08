import 'package:flutter/material.dart';
import '../services/material_service.dart';
import '../models/material.dart';

class MaterialListScreen extends StatefulWidget {
  @override
  _MaterialListScreenState createState() => _MaterialListScreenState();
}

class _MaterialListScreenState extends State<MaterialListScreen> {
  late Future<List<Material>> futureMaterials;

  @override
  void initState() {
    super.initState();
    futureMaterials = MaterialService().fetchMaterials();
  }

  @override
  Widget build(BuildContext context) {
    return Scaffold(
      appBar: AppBar(title: Text('Materials')),
      body: FutureBuilder<List<Material>>(
        future: futureMaterials,
        builder: (context, snapshot) {
          if (snapshot.connectionState == ConnectionState.waiting) {
            return Center(child: CircularProgressIndicator());
          } else if (snapshot.hasError) {
            return Center(child: Text('Error: ${snapshot.error}'));
          } else if (!snapshot.hasData || snapshot.data!.isEmpty) {
            return Center(child: Text('No materials found'));
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
                  trailing: IconButton(
                    icon: Icon(Icons.add),
                    onPressed: () => _restockMaterial(context, material.id),
                  ),
                );
              },
            );
          }
        },
      ),
    );
  }

  void _restockMaterial(BuildContext context, int materialId) async {
    // Add restock functionality here, show a dialog for quantity
    await MaterialService().restockMaterial(materialId, 10.0, 'Restocking');
    ScaffoldMessenger.of(
      context,
    ).showSnackBar(SnackBar(content: Text('Material restocked!')));
  }
}
