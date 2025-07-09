# serve.py
from flask import Flask, request, Response, send_from_directory, jsonify
from flask_cors import CORS
import threading, json, time, os

app = Flask(__name__)
CORS(app)                       # izinkan akses dari Streamlit & halaman Web

# ---------------------------
# state & sinkronisasi
# ---------------------------
current_params = {"kv": 80, "mA": 100, "Sec": 2, "kode": "x"}
lock = threading.Lock()

# ---------------------------
# endpoint  ➜  menerima update
# ---------------------------
@app.route("/update", methods=["POST"])
def update_params():
    data = request.get_json(force=True) or {}
    with lock:
        current_params.update(data)
    return jsonify(status="ok")

# ---------------------------
# endpoint  ➜  SSE stream
# ---------------------------
@app.route("/events")
def sse_events():
    def stream():
        while True:
            with lock:
                payload = json.dumps(current_params)
            yield f"data: {payload}\n\n"
            time.sleep(0.1)      # 10 fps
    return Response(stream(), mimetype="text/event-stream")

# ---------------------------
# endpoint  ➜  file statis /web
# ---------------------------
BASE_DIR = os.path.dirname(os.path.abspath(__file__))
WEB_DIR  = os.path.join(BASE_DIR, "web")

@app.route("/web/<path:filename>")
def serve_web(filename):
    return send_from_directory(WEB_DIR, filename)

# ---------------------------
# main
# ---------------------------
if __name__ == "__main__":
    print("=== FLASK SERVER STARTED ===")
    print("Listening  : http://localhost:8000")
    print("SSE stream : http://localhost:8000/events")
    print("Simulation : http://localhost:8000/web/index.html")
    app.run(port=8000, debug=True)
