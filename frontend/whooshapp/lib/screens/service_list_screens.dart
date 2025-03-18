import 'package:flutter/material.dart';
import '../models/service.dart';
import '../services/api_service.dart';
import '../screens/cart_screens.dart';

class ServiceListScreen extends StatefulWidget {
  @override
  State<ServiceListScreen> createState() => _ServiceListScreenState();
}

class _ServiceListScreenState extends State<ServiceListScreen> {
  late Future<List<Service>> services;
  List<Service> cart = [];
  Set<int> addedServiceIds = {}; // ✅ To track added items

  @override
  void initState() {
    super.initState();
    services = ApiService().fetchServices();
  }

  void updateCart(List<Service> updatedCart) {
    setState(() {
      cart = updatedCart;
      addedServiceIds = updatedCart.map((service) => service.id).toSet();
    });
  }

  void addToCart(Service service) {
    setState(() {
      cart.add(service);
      addedServiceIds.add(service.id);
    });

    ScaffoldMessenger.of(context).showSnackBar(
      SnackBar(
        content: Text('${service.name} added to cart!'),
        duration: Duration(seconds: 1),
        action: SnackBarAction(
          label: 'View Cart',
          onPressed: () {
            ScaffoldMessenger.of(context).hideCurrentSnackBar();
            navigateToCart();
          },
        ),
      ),
    );
  }

  void navigateToCart() {
    Navigator.push(
      context,
      MaterialPageRoute(
        builder: (context) => CartScreen(cart: cart, onCartUpdated: updateCart),
      ),
    );
  }

  @override
  Widget build(BuildContext context) {
    return Scaffold(
      appBar: ServiceAppBar(
        cartCount: cart.length,
        onCartPressed: navigateToCart,
      ),
      body: ServiceListBody(
        services: services,
        addToCart: addToCart,
        addedServiceIds: addedServiceIds,
      ),
      floatingActionButton:
          cart.isNotEmpty
              ? FloatingCartButton(onPressed: navigateToCart)
              : null,
    );
  }
}

class ServiceAppBar extends StatelessWidget implements PreferredSizeWidget {
  final int cartCount;
  final VoidCallback onCartPressed;

  const ServiceAppBar({required this.cartCount, required this.onCartPressed});

  @override
  Widget build(BuildContext context) {
    return AppBar(
      title: Text('Available Services'),
      actions: [
        Stack(
          children: [
            IconButton(
              icon: Icon(Icons.shopping_cart),
              onPressed: onCartPressed,
            ),
            if (cartCount > 0)
              Positioned(right: 6, top: 6, child: Badge(count: cartCount)),
          ],
        ),
      ],
    );
  }

  @override
  Size get preferredSize => Size.fromHeight(kToolbarHeight);
}

class ServiceListBody extends StatelessWidget {
  final Future<List<Service>> services;
  final Function(Service) addToCart;
  final Set<int> addedServiceIds;

  const ServiceListBody({
    required this.services,
    required this.addToCart,
    required this.addedServiceIds,
  });

  @override
  Widget build(BuildContext context) {
    return FutureBuilder<List<Service>>(
      future: services,
      builder: (context, snapshot) {
        if (snapshot.connectionState == ConnectionState.waiting) {
          return Center(child: CircularProgressIndicator());
        } else if (snapshot.hasError) {
          return Center(child: Text('Error: ${snapshot.error}'));
        } else if (!snapshot.hasData || snapshot.data!.isEmpty) {
          return Center(child: Text('No services found'));
        }

        final serviceList = snapshot.data!;
        return ListView.builder(
          itemCount: serviceList.length,
          itemBuilder: (context, index) {
            final service = serviceList[index];
            final isAdded = addedServiceIds.contains(service.id);
            return ServiceCard(
              service: service,
              isAdded: isAdded,
              onAddToCart: () => addToCart(service),
            );
          },
        );
      },
    );
  }
}

class ServiceDetails extends StatelessWidget {
  final Service service;
  final bool isAdded;
  final VoidCallback onAddToCart;

  const ServiceDetails({
    required this.service,
    required this.isAdded,
    required this.onAddToCart,
  });

  @override
  Widget build(BuildContext context) {
    return Column(
      crossAxisAlignment: CrossAxisAlignment.start,
      children: [
        Text(
          service.name,
          style: TextStyle(fontSize: 18, fontWeight: FontWeight.bold),
        ),
        Text(service.description),
        Row(
          children: [
            Text('₹${service.price}'),
            Spacer(),
            ElevatedButton(
              onPressed: isAdded ? null : onAddToCart,
              child: Text(isAdded ? 'Added' : 'Add'),
            ),
          ],
        ),
      ],
    );
  }
}

class ServiceCard extends StatelessWidget {
  final Service service;
  final bool isAdded; // Whether this service is already added to cart
  final VoidCallback
  onAddToCart; // Function to call when "Add" button is clicked
  const ServiceCard({
    super.key,
    required this.service,
    required this.isAdded,
    required this.onAddToCart,
  });

  @override
  Widget build(BuildContext context) {
    return Card(
      margin: const EdgeInsets.all(8),
      child: Padding(
        padding: const EdgeInsets.all(8),
        child: Row(
          crossAxisAlignment: CrossAxisAlignment.center,
          children: [
            Expanded(
              child: ServiceDetails(
                service: service,
                isAdded: isAdded,
                onAddToCart: onAddToCart,
              ),
            ),
            const SizedBox(width: 10),
            ServiceImage(imageUrl: service.imageUrl),
          ],
        ),
      ),
    );
  }
}

class ServiceImage extends StatelessWidget {
  final String imageUrl;

  const ServiceImage({required this.imageUrl});

  @override
  Widget build(BuildContext context) {
    return ClipRRect(
      borderRadius: BorderRadius.circular(8),
      child: Image.network(
        'http://localhost:8000$imageUrl',
        width: 80,
        height: 80,
        fit: BoxFit.cover,
        errorBuilder: (context, error, stackTrace) => Icon(Icons.image),
      ),
    );
  }
}

class Badge extends StatelessWidget {
  final int count;

  const Badge({required this.count});

  @override
  Widget build(BuildContext context) {
    return Container(
      padding: EdgeInsets.all(6),
      decoration: BoxDecoration(color: Colors.red, shape: BoxShape.circle),
      child: Text(
        count.toString(),
        style: TextStyle(
          color: Colors.white,
          fontSize: 12,
          fontWeight: FontWeight.bold,
        ),
      ),
    );
  }
}

class FloatingCartButton extends StatelessWidget {
  final VoidCallback onPressed;

  const FloatingCartButton({required this.onPressed});

  @override
  Widget build(BuildContext context) {
    return FloatingActionButton.extended(
      onPressed: onPressed,
      backgroundColor: Colors.black,
      icon: Icon(Icons.shopping_cart),
      label: Text('Go to Cart'),
    );
  }
}
