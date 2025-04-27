from flask import Flask, request, jsonify
from flask_cors import CORS
import firebase_admin
from firebase_admin import credentials, firestore
from datetime import datetime, timedelta

# Initialize Firebase
cred = credentials.Certificate("../wearable/avi-care-firebase-adminsdk-fbsvc-3b2558e032.json")
firebase_admin.initialize_app(cred)
db = firestore.client()

app = Flask(__name__)
CORS(app)  # Enable CORS
current_user = None  # Stores logged-in user's ID

# Helper functions
def get_user_collection():
    if not current_user:
        return None
    return db.collection("users").document(current_user)

@app.route('/set_user', methods=['POST'])
def set_user():
    """Set the current user ID from Flutter app"""
    global current_user
    data = request.json
    if "user_id" in data:
        current_user = data["user_id"]
        return jsonify({"message": f"User set to {current_user}"}), 200
    return jsonify({"error": "No user_id provided"}), 400

@app.route('/get_user', methods=['GET'])
def get_user():
    """Get current user ID for other services"""
    return jsonify({"user_id": current_user}) if current_user else jsonify({"error": "No user"}), 200

@app.route('/health_metrics', methods=['GET'])
def get_health_metrics():
    """Get latest health metrics for current user"""
    if not current_user:
        return jsonify({"error": "No user logged in"}), 400
    
    try:
        docs = get_user_collection().collection("health_metrics")\
            .order_by("timestamp", direction=firestore.Query.DESCENDING)\
            .limit(1)\
            .stream()
        
        latest_data = next(docs).to_dict() if docs else {}
        return jsonify(latest_data), 200
    except Exception as e:
        return jsonify({"error": str(e)}), 500

@app.route('/notifications', methods=['GET'])
def get_notifications():
    """Get unread notifications for current user"""
    if not current_user:
        return jsonify({"error": "No user logged in"}), 400
    
    try:
        docs = get_user_collection().collection("notifications")\
            .where("read", "==", False)\
            .order_by("timestamp", direction=firestore.Query.DESCENDING)\
            .stream()
        
        notifications = [doc.to_dict() for doc in docs]
        return jsonify(notifications), 200
    except Exception as e:
        return jsonify({"error": str(e)}), 500

@app.route('/send_command', methods=['POST'])
def send_command():
    """Forward commands to wearable simulation system"""
    if not current_user:
        return jsonify({"error": "No user logged in"}), 400
    
    data = request.json
    if not data or 'command' not in data:
        return jsonify({"error": "No command provided"}), 400
    
    command = data['command']
    valid_commands = {
        'simulate_fever', 'stop_fever',
        'simulate_dehydration', 'stop_dehydration',
        'set_activity', 'trigger_movement_reminder'
    }
    
    # Validate command
    if not any(cmd in command for cmd in valid_commands):
        return jsonify({"error": "Invalid command"}), 400
    
    try:
        # Write command to Firestore
        action = command.split()[0] if ' ' in command else command
        get_user_collection().collection("actions").document(action).set({
            'command': command,
            'timestamp': datetime.utcnow()
        })
        return jsonify({"message": f"Command '{command}' sent"}), 200
    except Exception as e:
        return jsonify({"error": str(e)}), 500

@app.route('/historical_data', methods=['GET'])
def get_historical_data():
    """Get historical data for charts"""
    if not current_user:
        return jsonify({"error": "No user logged in"}), 400
    
    try:
        time_filter = datetime.utcnow() - timedelta(hours=24)
        metrics = ['heart_rate', 'body_temp', 'steps']
        
        data = {}
        for metric in metrics:
            docs = get_user_collection().collection("health_metrics")\
                .where("timestamp", ">", time_filter)\
                .order_by("timestamp")\
                .stream()
            
            data[metric] = [{
                "timestamp": doc.get("timestamp").isoformat(),
                "value": doc.get(metric)
            } for doc in docs]
        
        return jsonify(data), 200
    except Exception as e:
        return jsonify({"error": str(e)}), 500

if __name__ == "__main__":
    app.run(host="0.0.0.0", port=5000, debug=True)
