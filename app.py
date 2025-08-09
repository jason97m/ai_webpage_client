from flask import Flask, render_template, request, jsonify
import requests
import os

app = Flask(__name__)

BACKEND_URL = os.getenv("BACKEND_URL")  # e.g. "https://your-backend-app.herokuapp.com/generate"

@app.route('/')
def index():
    return render_template('index.html')

@app.route('/generate', methods=['POST'])
def generate():
    data = request.get_json()
    prompt = data.get('prompt', '')

    if not prompt:
        return jsonify({'error': 'Missing prompt'}), 400

    try:
        # Call your backend API with full URL
        backend_response = requests.post(
            BACKEND_URL,
            json={'prompt': prompt}
        )
        backend_response.raise_for_status()
        result = backend_response.json()
        return jsonify(result)

    except requests.exceptions.RequestException as e:
        return jsonify({'error': str(e)}), 500


if __name__ == '__main__':
    app.run(debug=True, host='0.0.0.0', port=int(os.environ.get("PORT", 5000)))
