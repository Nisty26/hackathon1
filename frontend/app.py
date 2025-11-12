from flask import Flask, render_template, request, jsonify
import os, json
from PIL import Image
from collections import Counter
import cv2
import numpy as np
from sklearn.cluster import KMeans

app = Flask(__name__)

# Folders
UPLOAD_FOLDER = 'uploads'
RESULT_FOLDER = 'results'
os.makedirs(UPLOAD_FOLDER, exist_ok=True)
os.makedirs(RESULT_FOLDER, exist_ok=True)

app.config['UPLOAD_FOLDER'] = UPLOAD_FOLDER


def get_dominant_color(image_path):
    image = cv2.imread(image_path)
    image = cv2.cvtColor(image, cv2.COLOR_BGR2RGB)
    image = cv2.resize(image, (100, 100))

    pixels = image.reshape(-1, 3)
    kmeans = KMeans(n_clusters=3, n_init=10, random_state=42)
    kmeans.fit(pixels)

    counts = np.bincount(kmeans.labels_)
    dominant_color = kmeans.cluster_centers_[np.argmax(counts)]

    return {
        'r': int(dominant_color[0]),
        'g': int(dominant_color[1]),
        'b': int(dominant_color[2])
    }

@app.route('/')
def home():
    return render_template('index.html')

@app.route('/analyze', methods=['POST'])
def analyze_images():
    results = {}

    for field in ['selfie', 'outfit1', 'outfit2']:
        if field in request.files and request.files[field]:
            file = request.files[field]
            filename = file.filename
            upload_path = os.path.join(app.config['UPLOAD_FOLDER'], filename)
            result_path = os.path.join(RESULT_FOLDER, f"{filename}.json")

            # Save image
            file.save(upload_path)

            # 🔒 Reuse analysis if it exists
            if os.path.exists(result_path):
                with open(result_path, 'r') as f:
                    dominant = json.load(f)
            else:
                dominant = get_dominant_color(upload_path)
                with open(result_path, 'w') as f:
                    json.dump(dominant, f)

            results[field] = dominant
        else:
            results[field] = None

    results['summary'] = "Analysis complete! Dominant colors extracted successfully."
    return jsonify(results)

if __name__ == '__main__':
    app.run(debug=True)
