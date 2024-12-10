import random
import time
import threading
from datetime import datetime
import uuid  # For generating unique IDs
from webSocketServer import WebSocketServer, socketio, app

app = WebSocketServer().create_app()

connected_clients = 0

# List of random usernames for system-generated messages
random_usernames = [
    "ChatterBot", "FriendlyAI", "RoboTalker", "CodeBuddy", "ChatMaster"
]

chat_messages = [
    {"text": "Hello there!", "userId": "system", "timestamp": "", "username": random.choice(random_usernames)},
    {"text": "How's it going?", "userId": "system", "timestamp": "", "username": random.choice(random_usernames)},
    {"text": "Real-time messaging is awesome!", "userId": "system", "timestamp": "", "username": random.choice(random_usernames)},
]

# Add timestamps and unique IDs to the system messages
for msg in chat_messages:
    msg["timestamp"] = datetime.now().strftime("%Y-%m-%d %H:%M:%S")
    msg["id"] = str(uuid.uuid4())  # Generate unique ID

def broadcast_random_messages():
    """Send random chat messages periodically to all connected clients."""
    while True:
        time.sleep(3)
        random_message = random.choice(chat_messages)
        socketio.emit("message", random_message)

@socketio.on("connect")
def handle_connect():
    global connected_clients
    connected_clients += 1
    print("Client connected. Total clients:", connected_clients)

@socketio.on("disconnect")
def handle_disconnect():
    global connected_clients
    connected_clients -= 1
    print("Client disconnected. Total clients:", connected_clients)

@socketio.on("message")
def handle_message(message):
    """Handle incoming messages, add unique ID and timestamp."""
    message["timestamp"] = datetime.now().strftime("%Y-%m-%d %H:%M:%S")
    message["id"] = str(uuid.uuid4())  # Assign unique ID to the message
    print(f"Received message: {message}")
    socketio.emit("message", message)

@socketio.on("delete_message")
def handle_delete_message(message_id):
    """Handle deletion of a message by its ID."""
    print(f"Deleting message with ID: {message_id}")
    socketio.emit("delete_message", message_id)

@socketio.on("edit_message")
def handle_edit_message(data):
    """Handle editing of a message."""
    print(f"Editing message: {data}")
    socketio.emit("edit_message", data)

if __name__ == "__main__":
    broadcaster_thread = threading.Thread(target=broadcast_random_messages, daemon=True)
    broadcaster_thread.start()
    socketio.run(app)
