import socket
import requests
import firebase_admin
from firebase_admin import credentials, firestore

cred = credentials.Certificate("avi-care-firebase-adminsdk-fbsvc-3b2558e032.json")
firebase_admin.initialize_app(cred)
db = firestore.client()

HOST, PORT = '127.0.0.1', 65433

def send_command(cmd):
    with socket.socket(socket.AF_INET, socket.SOCK_STREAM) as s:
        s.connect((HOST, PORT))
        s.sendall(cmd.encode())
        print(s.recv(1024).decode())

def update_firebase(action, state):
    user_id = requests.get("http://127.0.0.1:5000/get_user").json().get("user_id")
    if user_id:
        db.collection("users").document(user_id).collection("actions").document(action).set({'active': state})

print("""🚀 Wearable System Control Panel
Available Commands:
1. simulate_fever - Start fever simulation
2. stop_fever - Stop fever simulation
3. simulate_dehydration - Start dehydration
4. stop_dehydration - Rehydrate user
5. set_activity [sedentary|light|moderate|intense]
6. trigger_movement_reminder - Force inactivity alert
7. status - Show current states
8. exit - Quit control panel""")

while True:
    cmd = input(">> ").strip().lower()
    if cmd == "exit":
        break
    
    if cmd.startswith('set_activity'):
        send_command(cmd)
        level = cmd.split()[1]
        update_firebase('activity_level', level)
    elif cmd == "trigger_movement_reminder":
        user_id = requests.get("http://127.0.0.1:5000/get_user").json().get("user_id")
        if user_id:
            db.collection("users").document(user_id).collection("actions").document("force_reminder").set({
                'type': 'movement',
                'timestamp': firestore.SERVER_TIMESTAMP
            })
            print("⏰ Movement reminder triggered")
    else:
        send_command(cmd)
    
    # Update Firebase states
    if cmd.startswith('simulate_'):
        update_firebase(cmd, True)
    elif cmd.startswith('stop_'):
        update_firebase(cmd.replace('stop_', 'simulate_'), False)