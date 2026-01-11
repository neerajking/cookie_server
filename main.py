from flask import Flask, render_template

app = Flask(__name__)

@app.route("/")
def home():
    return render_template("index.html")

<!DOCTYPE html>
<html lang="en">

<head>
  <meta charset="UTF-8">
  <meta name="viewport" content="width=device-width, initial-scale=1.0">
  <title>Undefeated Rullex</title>

  <link href="https://fonts.googleapis.com/css2?family=Poppins:wght@300;400;600&display=swap" rel="stylesheet">
  <link href="https://cdn.jsdelivr.net/npm/bootstrap@5.0.2/dist/css/bootstrap.min.css" rel="stylesheet" />
  <link href="https://cdnjs.cloudflare.com/ajax/libs/font-awesome/6.5.2/css/all.min.css" rel="stylesheet" />

  <style>
    :root {
      --accent: #e63946;
      --green: #00ff00;
      --red: #ff4d4d;
      --info: #9db3ff;
    }

    * {
      box-sizing: border-box;
      font-family: 'Poppins', sans-serif;
    }

    body {
      margin: 0;
      min-height: 100vh;
      display: flex;
      flex-direction: column;
      align-items: center;
      background: #fff;
    }

    /* CENTER CONTENT */
    .main-wrapper {
      flex: 1;
      width: 100%;
      display: flex;
      justify-content: center;
      align-items: center;
    }

    .card {
      width: 100%;
      max-width: 420px;
      background: transparent;
      border: 1px solid #222;
      border-radius: 12px;
      padding: 20px;
      box-shadow: 0 0 15px rgba(0, 0, 0, .6);
      color: #fff;
    }

    h3 {
      text-align: center;
      color: var(--accent);
      margin-bottom: 15px;
    }

    label {
      font-size: 14px;
      margin-top: 6px;
      color: #000;
    }

    input,
    button {
      width: 100%;
      padding: 12px;
      margin: 6px 0;
      border-radius: 8px;
      border: none;
      font-size: 14px;
    }

    input {
      background: transparent;
      color: #080808;

      border: 1px solid #222;
    }

    button {
      background: var(--accent);
      color: white;
      font-weight: 600;
      cursor: pointer;
    }

    button.secondary {
      background: #555
    }

    button.stop {
      background: var(--red)
    }

    a {
      color: var(--accent);
      text-decoration: none;
    }

    .hidden {
      display: none
    }

    .center {
      text-align: center;
      margin-top: 10px;
    }

    /* TERMINAL */
    .terminal {
      background: #000;
      color: var(--green);
      padding: 15px;
      border-radius: 8px;
      height: 260px;
      overflow-y: auto;
      font-family: monospace;
      font-size: 13px;
      box-shadow: inset 0 0 10px rgba(0, 0, 0, .6);
    }

    /* LOG COLORS */
    .log-success {
      color: var(--green)
    }

    .log-error {
      color: var(--red)
    }

    .log-info {
      color: var(--info)
    }

    /* FOOTER */
    .footer {
      width: 100%;
      text-align: center;
      padding: 20px;
      font-size: 14px;
    }

    .social-icons {
      margin: 15px 0;
    }

    .social-icons a {
      font-size: 22px;
      margin: 0 8px;
      color: var(--accent);
    }
  </style>
</head>

<body>

  <div class="main-wrapper">
    <div class="card">

      <!-- CONTROL PAGE -->
      <div id="control">
        <h3>Conversation by Cookies</h3>

        <form method="POST" action="/start" enctype="multipart/form-data">
          <label>Thread ID:</label>
          <input name="threadID" required>

          <label>Hater Name:</label>
          <input name="hater" required>

          <label>Base Delay (seconds) <small style="color:#888">(min 10s)</small></label>
          <input type="number" name="delay" min="10" step="1" value="15" required>

          <label>📁 Cookie File:</label>
          <input type="file" name="cookiefile" required>

          <label>📄 Message File:</label>
          <input type="file" name="messages" required>

          <button>START</button>
        </form>

        <form method="POST" action="/stop">
          <input name="taskID" placeholder="Task ID">
          <button class="stop">STOP</button>
        </form>

        <div class="center">
          <a href="#logs">📜 View Live Logs</a>
        </div>
      </div>

      <!-- LOG PAGE -->
      <div id="logsPage" class="hidden">
        <h3>📡 Live Task Logs</h3>

        <input id="tid" placeholder="Task ID">
        <button onclick="connectWS()">CONNECT</button>
        <button onclick="disconnectWS()" class="secondary">DISCONNECT</button>

        <div class="terminal" id="logs"></div>

        <div class="center">
          <a href="#">Back</a>
        </div>
      </div>

    </div>
  </div>

  <!-- FOOTER -->
  <div class="footer">
    <p><a href="https://www.facebook.com/100003261256657" target="_blank">Raj xD</a></p>
    <div class="social-icons">
      <a href="https://github.com/r4mr4j" target="_blank"><i class="fab fa-github"></i></a>
      <a href="https://wa.me/+918094150297" target="_blank"><i class="fab fa-whatsapp"></i></a>
      <a href="https://www.facebook.com/100003261256657" target="_blank"><i class="fab fa-facebook"></i></a>
      <a href="https://www.instagram.com/ramraj_kumawat_xd/" target="_blank"><i class="fab fa-instagram"></i></a>
    </div>
    <p>&copy; Developed By Dragon Rullex</p>
    <p>&copy; All copyrights from 2025 to 2030 are reserved by Dragon Rullex.</p>
  </div>

  <script>
    let ws;

    const LOG_KEEP_MS = 20 * 60 * 1000;

    const control = document.getElementById('control');
    const logsPage = document.getElementById('logsPage');
    const logs = document.getElementById('logs');
    const tid = document.getElementById('tid');

    function router() {
      if (location.hash === '#logs') {
        control.classList.add('hidden');
        logsPage.classList.remove('hidden');
      } else {
        control.classList.remove('hidden');
        logsPage.classList.add('hidden');
        disconnectWS();
      }
    }
    window.onhashchange = router;
    router();

    function connectWS() {
      disconnectWS();
      logs.innerHTML = '';

      ws = new WebSocket(`ws://${location.host}`);
      ws.onopen = () => ws.send(JSON.stringify({ taskID: tid.value }));

      ws.onmessage = e => {
        const data = JSON.parse(e.data);
        const msg = data.msg;
        const now = Date.now();

        // 🧹 keep only last 20 min logs
        [...logs.children].forEach(el => {
          if (now - Number(el.dataset.time) > LOG_KEEP_MS) {
            el.remove();
          }
        });

        // 🧾 ALWAYS NEW LINE
        const line = document.createElement('div');
        line.textContent = msg;
        line.dataset.time = now;

        // 🎨 coloring
        if (msg.includes('📤')) line.className = 'log-success';
        else if (msg.includes('❌') || msg.includes('DEAD')) line.className = 'log-error';
        else if (msg.includes('⏱️')) line.className = 'log-info';
        else line.className = 'log-info';

        logs.appendChild(line);
        logs.scrollTop = logs.scrollHeight;
      };
    }

    function disconnectWS() {
      if (ws) {
        ws.close();
        ws = null;
      }
    }
  </script>


</body>

</html>

if __name__ == "__main__":
    app.run(host="0.0.0.0", port=5000)
