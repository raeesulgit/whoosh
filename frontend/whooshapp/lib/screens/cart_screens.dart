import 'package:flutter/material.dart';
import '../models/service.dart';

class CartScreen extends StatefulWidget {
  final List<Service> cart;
  final Function(List<Service>) onCartUpdated; // ✅ Callback to update HomeScreen

  CartScreen({required this.cart, required this.onCartUpdated});

  @override
  _CartScreenState createState() => _CartScreenState();
}

class _CartScreenState extends State<CartScreen> {
  late List<Service> cart;

  @override
  void initState() {
    super.initState();
    cart = List.from(widget.cart); // ✅ Copy cart list locally
  }

  void removeFromCart(int index) {
    setState(() {
      cart.removeAt(index); // ✅ Remove item
    });

    widget.onCartUpdated(cart); // ✅ Notify HomeScreen that cart has changed

    ScaffoldMessenger.of(context).showSnackBar(
      SnackBar(content: Text('Service removed from cart')),
    );
  }

  @override
  Widget build(BuildContext context) {
    double total = cart.fold(0, (sum, item) => sum + item.price); // ✅ Recalculate total

    return Scaffold(
      appBar: AppBar(title: Text('Cart')),
      body: cart.isEmpty
          ? Center(child: Text('Your cart is empty!'))
          : Column(
              children: [
                Expanded(
                  child: ListView.builder(
                    itemCount: cart.length,
                    itemBuilder: (context, index) {
                      final service = cart[index];
                      return Card(
                        margin: EdgeInsets.symmetric(horizontal: 10, vertical: 5),
                        child: ListTile(
                          title: Text(service.name, style: TextStyle(fontWeight: FontWeight.bold)),
                          subtitle: Text(service.description),
                          trailing: Row(
                            mainAxisSize: MainAxisSize.min,
                            children: [
                              Text(
                                '₹${service.price.toStringAsFixed(0)}',
                                style: TextStyle(fontWeight: FontWeight.bold),
                              ),
                              SizedBox(width: 10),
                              OutlinedButton(
                                onPressed: () => removeFromCart(index), // ✅ Remove item
                                style: OutlinedButton.styleFrom(
                                  side: BorderSide(color: Colors.red),
                                  padding: EdgeInsets.symmetric(horizontal: 12, vertical: 6),
                                ),
                                child: Text('Remove', style: TextStyle(color: Colors.red)),
                              ),
                            ],
                          ),
                        ),
                      );
                    },
                  ),
                ),
                Container(
                  padding: EdgeInsets.all(16),
                  child: Column(
                    children: [
                      Text(
                        'Total: ₹$total',
                        style: TextStyle(fontSize: 18, fontWeight: FontWeight.bold),
                      ),
                      SizedBox(height: 10),
                      ElevatedButton(
                        style: ElevatedButton.styleFrom(
                          backgroundColor: Colors.black,
                          foregroundColor: Colors.white,
                        ),
                        onPressed: () {
                          ScaffoldMessenger.of(context).showSnackBar(
                            SnackBar(content: Text('Proceeding to checkout...')),
                          );
                        },
                        child: Text('Checkout'),
                      ),
                    ],
                  ),
                ),
              ],
            ),
    );
  }
}
