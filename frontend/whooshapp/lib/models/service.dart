class Service {
  final int id;
  final String name;
  final String description;
  final double price;
  final String vehicleType;
  final String imageUrl;

  Service({
    required this.id,
    required this.name,
    required this.description,
    required this.price,
    required this.vehicleType,
    required this.imageUrl,
  });

  factory Service.fromJson(Map<String, dynamic> json) {
    return Service(
      id: json['id'],
      name: json['name'],
      description: json['description'],
      price: json['price'].toDouble(),
      vehicleType: json['vehicle_type'],
      imageUrl: json['image_url'],
    );
  }
}
