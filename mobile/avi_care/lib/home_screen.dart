import 'package:flutter/material.dart';
import 'package:cloud_firestore/cloud_firestore.dart';
import 'package:firebase_auth/firebase_auth.dart';

class HomeScreen extends StatefulWidget {
  const HomeScreen({super.key});

  @override
  State<HomeScreen> createState() => _HomeScreenState();
}

class _HomeScreenState extends State<HomeScreen> {
  bool _feverAlertShown = false; // To prevent showing the SnackBar repeatedly

  @override
  Widget build(BuildContext context) {
    // Get the current user's ID
    String? userId = FirebaseAuth.instance.currentUser?.uid;

    if (userId == null) {
      return Scaffold(
        appBar: AppBar(
          title: const Text('Dashboard'),
        ),
        body: const Center(
          child: Text('User not logged in'),
        ),
      );
    }

    return Scaffold(
      appBar: AppBar(
        title: const Text('Dashboard'),
        backgroundColor: const Color(0xFF5BE7C4), // Modern color for the AppBar
      ),
      body: StreamBuilder<QuerySnapshot>(
        stream: FirebaseFirestore.instance
            .collection('users')
            .doc(userId)
            .collection('health_metrics')
            .orderBy('timestamp', descending: true)
            .limit(1)
            .snapshots(),
        builder: (context, snapshot) {
          if (snapshot.connectionState == ConnectionState.waiting) {
            return const Center(child: CircularProgressIndicator());
          }

          if (!snapshot.hasData || snapshot.data!.docs.isEmpty) {
            return const Center(child: Text('No data available'));
          }

          // Get the latest document
          var latestData = snapshot.data!.docs.first.data() as Map<String, dynamic>;

          // Check for fever
          bool hasFever = latestData['health_status'] == 'fever' ||
              (latestData['body_temp'] != null && latestData['body_temp'] > 37.5);

          // Show a SnackBar if fever is detected and not already shown
          if (hasFever && !_feverAlertShown) {
            _feverAlertShown = true;
            WidgetsBinding.instance.addPostFrameCallback((_) {
              ScaffoldMessenger.of(context).showSnackBar(
                SnackBar(
                  duration: const Duration(seconds: 8),
                  content: const Text(
                    '⚠️ Fever detected! Please take care.',
                    style: TextStyle(color: Colors.black),
                  ),
                  backgroundColor: Colors.pinkAccent,
                ),
              );
            });
          }

          return Padding(
            padding: const EdgeInsets.all(16.0),
            child: SingleChildScrollView(
              child: Column(
                crossAxisAlignment: CrossAxisAlignment.stretch,
                children: [
                  // First row with square cards
                  Row(
                    mainAxisAlignment: MainAxisAlignment.spaceBetween,
                    children: [
                      _buildSquareCard(
                        title: 'Activity Level',
                        value: latestData['activity_level'],
                        icon: Icons.directions_run,
                        color: Colors.blueAccent,
                      ),
                      SizedBox(width: 16.0), // Space between cards
                      _buildSquareCard(
                        title: 'Blood Oxygen',
                        value: '${latestData['blood_oxygen']}%',
                        icon: Icons.bloodtype,
                        color: Colors.redAccent,
                      ),
                    ],
                  ),
                  const SizedBox(height: 16.0),
                  Row(
                    mainAxisAlignment: MainAxisAlignment.spaceEvenly,
                    children: [
                      _buildSquareCard(
                        title: 'Body Temperature',
                        value: '${latestData['body_temp']}°C',
                        icon: Icons.thermostat,
                        color: hasFever ? Colors.red : Colors.orangeAccent,
                      ),
                      SizedBox(width: 16.0), // Space between cards
                      _buildSquareCard(
                        title: 'Health Status',
                        value: latestData['health_status'],
                        icon: Icons.health_and_safety,
                        color: hasFever ? Colors.red : Colors.green,
                      ),
                    ],
                  ),
                  const SizedBox(height: 16.0),

                  // Remaining tall cards
                  _buildMetricCard(
                    title: 'Heart Rate',
                    value: '${latestData['heart_rate']} bpm',
                    icon: Icons.favorite,
                    color: Colors.purpleAccent,
                  ),
                  _buildMetricCard(
                    title: 'HRV',
                    value: latestData['hrv'].toString(),
                    icon: Icons.monitor_heart_rounded,
                    color: Colors.teal,
                  ),
                  _buildMetricCard(
                    title: 'Hydration Level',
                    value: '${latestData['hydration_level']}%',
                    icon: Icons.water_drop,
                    color: Colors.lightBlueAccent,
                  ),
                  _buildMetricCard(
                    title: 'Inactive Duration',
                    value: '${latestData['inactive_duration']} min',
                    icon: Icons.access_time,
                    color: Colors.grey,
                  ),
                  _buildMetricCard(
                    title: 'Movement Intensity',
                    value: latestData['movement_intensity'].toString(),
                    icon: Icons.fitness_center,
                    color: Colors.amber,
                  ),
                  _buildMetricCard(
                    title: 'Steps',
                    value: latestData['steps'].toString(),
                    icon: Icons.directions_walk,
                    color: Colors.greenAccent,
                  ),
                ],
              ),
            ),
          );
        },
      ),
    );
  }

  Widget _buildSquareCard({
    required String title,
    required String value,
    required IconData icon,
    required Color color,
  }) {
    return Expanded(
      child: Container(
        // margin: const EdgeInsets.symmetric(horizontal: 8.0),
        padding: const EdgeInsets.symmetric(vertical: 16.0),
        decoration: BoxDecoration(
          color: color.withOpacity(0.1),
          borderRadius: BorderRadius.circular(12.0),
          border: Border.all(color: color, width: 1.5),
        ),
        child: Column(
          mainAxisAlignment: MainAxisAlignment.center,
          children: [
            CircleAvatar(
              backgroundColor: color,
              child: Icon(icon, color: Colors.white),
            ),
            const SizedBox(height: 8.0),
            Text(
              title,
              textAlign: TextAlign.center,
              style: const TextStyle(
                fontSize: 14.0,
                fontWeight: FontWeight.bold,
                color: Colors.white,
              ),
            ),
            const SizedBox(height: 4.0),
            Text(
              value,
              textAlign: TextAlign.center,
              style: const TextStyle(
                fontSize: 12.0,
                color: Colors.white,
              ),
            ),
          ],
        ),
      ),
    );
  }

  Widget _buildMetricCard({
    required String title,
    required String value,
    required IconData icon,
    required Color color,
  }) {
    return Container(
      margin: const EdgeInsets.symmetric(vertical: 8.0),
      padding: const EdgeInsets.all(16.0),
      decoration: BoxDecoration(
        color: color.withOpacity(0.1),
        borderRadius: BorderRadius.circular(12.0),
        border: Border.all(color: color, width: 1.5),
      ),
      child: Row(
        children: [
          CircleAvatar(
            backgroundColor: color,
            child: Icon(icon, color: Colors.white),
          ),
          const SizedBox(width: 16.0),
          Expanded(
            child: Column(
              crossAxisAlignment: CrossAxisAlignment.start,
              children: [
                Text(
                  title,
                  style: const TextStyle(
                    fontSize: 16.0,
                    fontWeight: FontWeight.bold,
                    color: Colors.white,
                  ),
                ),
                const SizedBox(height: 4.0),
                Text(
                  value,
                  style: const TextStyle(
                    fontSize: 14.0,
                    color: Colors.white,
                  ),
                ),
              ],
            ),
          ),
        ],
      ),
    );
  }
}