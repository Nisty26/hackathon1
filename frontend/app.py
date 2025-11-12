# frontend/app.py

from flask import Flask, render_template, request, jsonify
import os
import requests

app = Flask(__name__)

# Point this to your FastAPI base URL.
# For local dev it’s 127.0.0.1:8000; for ngrok set FASTAPI_BASE env var.
FASTAPI_BASE = os.environ.get("FASTAPI_BASE", "http://127.0.0.1:8000")

@app.route("/")
def home():
    return render_template("index.html")

@app.route("/health")
def health():
    try:
        r = requests.get(f"{FASTAPI_BASE}/health", timeout=5)
        return jsonify({"frontend_ok": True, "backend_ok": r.ok, "backend_response": r.json()})
    except Exception as e:
        return jsonify({"frontend_ok": True, "backend_ok": False, "error": str(e)}), 503

@app.route("/analyze", methods=["POST"])
def analyze_images():
    # Expect all three files from the form: selfie, outfit1, outfit2
    required = ["selfie", "outfit1", "outfit2"]
    files = {}

    for key in required:
        f = request.files.get(key)
        if not f:
            return jsonify({"error": f"Missing file: {key}"}), 400
        # pass-through stream directly to FastAPI (no need to save locally)
        files[key] = (f.filename, f.stream, f.mimetype or "application/octet-stream")

    try:
        resp = requests.post(f"{FASTAPI_BASE}/analyze/all", files=files, timeout=60)
        resp.raise_for_status()
        return jsonify(resp.json())
    except requests.RequestException as e:
        # Bubble up a helpful error to the UI
        return jsonify({"error": f"Backend request failed: {e}"}), 502

if __name__ == "__main__":
    # Run Flask on port 5000
    app.run(debug=True, port=5000)
