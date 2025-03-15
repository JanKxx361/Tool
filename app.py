from flask import Flask, request, jsonify
import openai
import requests
from flask_cors import CORS
import os

app = Flask(__name__)
CORS(app)  # Erlaubt API-Anfragen von anderen Domains

# OpenAI API Key aus Umgebungsvariablen
OPENAI_API_KEY = os.getenv("OPENAI_API_KEY")
VIDEO_API_KEY = os.getenv("VIDEO_API_KEY")

if not OPENAI_API_KEY:
    raise ValueError("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")
if not VIDEO_API_KEY:
    raise ValueError("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")

openai.api_key = OPENAI_API_KEY

@app.route('/generate_script', methods=['POST'])
def generate_script():
    try:
        data = request.get_json(force=True)
        if not data or "product_name" not in data:
            return jsonify({"error": "Fehlende oder ungültige JSON-Daten"}), 400

        product_name = data.get("product_name", "Produkt")

        response = openai.ChatCompletion.create(
            model="gpt-4",
            messages=[
                {"role": "system", "content": "Erstelle ein TikTok-Vergleichsskript für ein Produkt."},
                {"role": "user", "content": f"Erstelle ein Skript für einen TikTok-Produktvergleich zwischen günstig und teuer für {product_name}."}
            ]
        )

        return jsonify({"script": response['choices'][0]['message']['content']})
    
    except Exception as e:
        return jsonify({"error": f"Fehler bei der Skriptgenerierung: {str(e)}"}), 500

@app.route('/generate_video', methods=['POST'])
def generate_video():
    try:
        data = request.get_json(force=True)
        if not data or "product_name" not in data:
            return jsonify({"error": "Fehlende oder ungültige JSON-Daten"}), 400

        product_name = data.get("product_name", "Produkt")

        # Video-Erstellung API (Hier eigene API-URL eintragen)
        video_api_url = "https://api.example.com/videoai"
        video_response = requests.post(video_api_url, json={"text": f"Vergleichsvideo für {product_name}"}, headers={"Authorization": f"Bearer {VIDEO_API_KEY}"})

        if video_response.status_code == 200:
            return jsonify(video_response.json())

        return jsonify({"error": "Fehler bei der Videoerstellung"}), 500
    
    except Exception as e:
        return jsonify({"error": f"Fehler bei der Videoanfrage: {str(e)}"}), 500

if __name__ == '__main__':
    app.run(host="0.0.0.0", port=5000, debug=True)
