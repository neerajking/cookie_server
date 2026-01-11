import eventlet
eventlet.monkey_patch()

from flask import Flask, render_template, request, jsonify
from flask_socketio import SocketIO
import threading
import time
import uuid

app = Flask(__name__)
app.config["SECRET_KEY"] = "dragon-rullex"
socketio = SocketIO(app, cors_allowed_origins="*")

tasks = {}

@app.route("/")
def home():
    return render_template("index.html")

@app.route("/start", methods=["POST"])
def start_task():
    thread_id = request.form.get("threadID")
    hater = request.form.get("hater")
    delay = int(request.form.get("delay", 15))

    task_id = str(uuid.uuid4())[:8]
    tasks[task_id] = True

    def worker():
        socketio.emit("log", {"msg": f"🟢 Task {task_id} started"})
        socketio.emit("log", {"msg": f"📌 ThreadID: {thread_id}"})
        socketio.emit("log", {"msg": f"👤 Hater: {hater}"})

        count = 1
        while tasks.get(task_id):
            socketio.emit("log", {
                "msg": f"📤 [{count}] Message sent using cookies (demo)"
            })
            count += 1
            time.sleep(delay)

        socketio.emit("log", {"msg": f"❌ Task {task_id} stopped"})

    threading.Thread(target=worker, daemon=True).start()

    return jsonify({"status": "started", "taskID": task_id})

@app.route("/stop", methods=["POST"])
def stop_task():
    task_id = request.form.get("taskID")
    tasks[task_id] = False
    return jsonify({"status": "stopped", "taskID": task_id})

@socketio.on("message")
def handle_message(data):
    task_id = data.get("taskID")
    socketio.emit("log", {"msg": f"🔌 Connected to task {task_id}"})

if __name__ == "__main__":
    socketio.run(app, host="0.0.0.0", port=5000)
