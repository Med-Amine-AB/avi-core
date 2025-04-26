import threading
import time
import random
import socket
import requests
import firebase_admin
from firebase_admin import credentials, firestore
from datetime import datetime, timedelta

# Initialize Firebase
cred = credentials.Certificate("aqwaflow-firebase-adminsdk-fbsvc-fca1477020.json")
firebase_admin.initialize_app(cred)
db = firestore.client()

USER_ID_API = "http://127.0.0.1:5000/get_user"

def get_user_id():
    try:
        response = requests.get(USER_ID_API)
        return response.json().get("user_id") if response.ok else None
    except Exception as e:
        print(f"Error fetching user ID: {e}")
        return None

# Simulation states and health parameters
sim_states = {
    'fever': False,
    'dehydration': False,
    'activity_level': 'moderate',
    'last_movement': datetime.now(),
    'hydration_level': 100,  # Percentage
    'base_heart_rate': 72,
    'movement_reminder_sent': False
}
state_lock = threading.Lock()
HOST, PORT = '127.0.0.1', 65433

# Physiological parameters
HEALTH_BASELINES = {
    'hydration_threshold': 30,
    'inactivity_threshold': timedelta(minutes=15),
    'fever_temp_increase': 1.5,
    'dehydration_hr_increase': 0.2  # % increase per minute
}

def handle_client(conn):
    global sim_states
    with conn:
        while True:
            cmd = conn.recv(1024).decode().strip().lower()
            if not cmd:
                break
            with state_lock:
                response = ""
                if cmd == "simulate_fever":
                    sim_states['fever'] = True
                    response = "🔥 Fever simulation activated"
                elif cmd == "stop_fever":
                    sim_states['fever'] = False
                    response = "👍 Fever simulation stopped"
                elif cmd == "simulate_dehydration":
                    sim_states['dehydration'] = True
                    sim_states['hydration_level'] = 25
                    response = "🏜️ Dehydration simulation activated"
                elif cmd == "stop_dehydration":
                    sim_states['dehydration'] = False
                    sim_states['hydration_level'] = 100
                    response = "👍 Dehydration simulation stopped"
                elif cmd.startswith("set_activity"):
                    level = cmd.split()[1]
                    sim_states['activity_level'] = level
                    response = f"🏃 Activity level set to {level}"
                elif cmd == "status":
                    response = str(sim_states)
                conn.sendall(response.encode())

def start_socket_server():
    with socket.socket(socket.AF_INET, socket.SOCK_STREAM) as s:
        s.bind((HOST, PORT))
        s.listen()
        while True:
            conn, _ = s.accept()
            threading.Thread(target=handle_client, args=(conn,), daemon=True).start()

def send_reminder(user_id, message):
    try:
        db.collection("users").document(user_id).collection("notifications").add({
            "timestamp": datetime.utcnow(),
            "message": message,
            "read": False
        })
        print(f"🔔 Sent reminder: {message}")
    except Exception as e:
        print(f"🔥 Error sending reminder: {e}")

def generate_metrics():
    user_id = get_user_id()
    last_activity = datetime.now()
    hr_dehydration_modifier = 0
    
    while True:
        with state_lock:
            current_states = sim_states.copy()
        
        # Calculate inactivity duration
        inactivity_duration = datetime.now() - current_states['last_movement']
        
        # Generate base metrics
        heart_rate = current_states['base_heart_rate']
        temp = 36.5
        spo2 = 98
        steps = 0
        hrv = random.randint(60, 100)
        
        # Activity-based metrics
        activity_levels = {
            'sedentary': (0.5, 0.3),
            'light': (2.0, 0.7),
            'moderate': (5.0, 1.2),
            'intense': (10.0, 2.0)
        }
        activity_modifier, intensity = activity_levels[current_states['activity_level']]
        
        # Generate steps based on activity
        steps = int(random.gauss(activity_modifier * 5, 1.5))
        if steps < 0:
            steps = 0
        
        # Update last movement time if steps detected
        if steps > 0:
            last_activity = datetime.now()
            sim_states['last_movement'] = datetime.now()
            sim_states['movement_reminder_sent'] = False
        
        # Dehydration effects
        if current_states['dehydration']:
            hr_dehydration_modifier += HEALTH_BASELINES['dehydration_hr_increase']
            heart_rate += int(heart_rate * (hr_dehydration_modifier/100))
            spo2 -= 2
            hrv -= 15
            temp += 0.3
        
        # Fever effects
        if current_states['fever']:
            temp += HEALTH_BASELINES['fever_temp_increase'] + random.uniform(-0.2, 0.5)
            heart_rate += 15
            hrv -= 20
        
        # Inactivity reminder logic
        if not current_states['movement_reminder_sent'] and \
           inactivity_duration > HEALTH_BASELINES['inactivity_threshold']:
            send_reminder(user_id, "🛑 Prolonged inactivity detected! Consider moving around.")
            sim_states['movement_reminder_sent'] = True
        
        # Hydration reminder
        if current_states['hydration_level'] < HEALTH_BASELINES['hydration_threshold']:
            send_reminder(user_id, "💧 Low hydration level detected! Please drink water.")
        
        # Prepare data payload
        data = {
            "timestamp": datetime.utcnow(),
            "heart_rate": max(50, min(heart_rate, 140)),
            "hrv": max(20, hrv),
            "body_temp": round(temp, 1),
            "blood_oxygen": max(85, spo2),
            "steps": steps,
            "movement_intensity": round(intensity, 1),
            "inactive_duration": int(inactivity_duration.total_seconds() / 60),
            "hydration_level": current_states['hydration_level'],
            "activity_level": current_states['activity_level'],
            "health_status": "fever" if current_states['fever'] else 
                           "dehydrated" if current_states['dehydration'] else "normal"
        }

        # Push to Firestore
        if user_id:
            try:
                db.collection("users").document(user_id).collection("health_metrics").add(data)
                print(f"📊 Data logged: {data}")
            except Exception as e:
                print(f"🔥 Firestore error: {e}")
        
        time.sleep(5)

if __name__ == "__main__":
    threading.Thread(target=start_socket_server, daemon=True).start()
    generate_metrics()