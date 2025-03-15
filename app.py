from flask import Flask, request, jsonify
import openai
import requests
from flask_cors import CORS
import os

app = Flask(__name__)
CORS(app)

openai.api_key = os.getenv("OPENAI_API_KEY")
VIDEO_API_KEY = os.getenv("VIDEO_API_KEY")

@app.route('/generate_script', methods=['POST'])
def generate_script():
    data = request.get_json(force=True)
    product_name = data.get("product_name", "Produkt")

    response = openai.ChatCompletion.create(
        model="gpt-4",
        messages=[
            {"role": "system", "content": "Erstelle ein TikTok-Vergleichsskript für ein Produkt."},
            {"role": "user", "content": f"Vergleiche ein günstiges und ein teures {product_name} für ein TikTok-Video."}
        ]
    )

    return jsonify({"script": response['choices'][0]['message']['content']})

@app.route('/generate_video', methods=['POST'])
def generate_video():
    data = request.get_json(force=True)
    product_name = data.get("product_name", "Produkt")

    video_api_url = "https://api.example.com/videoai"
    video_response = requests.post(video_api_url, json={"text": f"Vergleichsvideo für {product_name}"}, headers={"Authorization": f"Bearer {VIDEO_API_KEY}"})

    if video_response.status_code == 200:
        return jsonify(video_response.json())

    return jsonify({"error": "Fehler bei der Videoerstellung"}), 500

if __name__ == '__main__':
    app.run(host="0.0.0.0", port=5000)

