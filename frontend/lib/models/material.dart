class Material {
  final int id;
  final String name;
  final double quantity;
  final String unit;
  final double reorderPoint;

  Material({
    required this.id,
    required this.name,
    required this.quantity,
    required this.unit,
    required this.reorderPoint,
  });

  factory Material.fromJson(Map<String, dynamic> json) {
    return Material(
      id: json['id'],
      name: json['name'],
      quantity: json['quantity'],
      unit: json['unit'],
      reorderPoint: json['reorder_point'],
    );
  }
}
