from flask import Flask, render_template, request, jsonify
from flask_socketio import SocketIO
import time
import threading
import uuid

app = Flask(__name__)
socketio = SocketIO(app, cors_allowed_origins="*")

tasks = {}

@app.route("/")
def home():
    return render_template("index.html")


@app.route("/start", methods=["POST"])
def start():
    task_id = str(uuid.uuid4())[:8]

    def fake_bot():
        for i in range(1, 50):
            if task_id not in tasks:
                break
            socketio.emit("message", {
                "msg": f"📤 Message sent {i}"
            })
            time.sleep(2)

        socketio.emit("message", {
            "msg": "✅ Task completed"
        })

    t = threading.Thread(target=fake_bot)
    tasks[task_id] = t
    t.start()

    return f"Task Started. Task ID: {task_id}"


@app.route("/stop", methods=["POST"])
def stop():
    task_id = request.form.get("taskID")
    tasks.pop(task_id, None)
    return "Task stopped"


@socketio.on("message")
def handle_ws(data):
    pass


if __name__ == "__main__":
    socketio.run(app, host="0.0.0.0", port=5000)
