from flask import Flask, request, jsonify, send_from_directory
import openai
import os

app = Flask(__name__)

openai.api_key = os.getenv("OPENAI_API_KEY")

# Serve the frontend
@app.route("/generate")
def index():
    return send_from_directory('.', '/templates/index.html')

@app.route('/generate', methods=['POST'])
def generate_site():
    data = request.get_json()
    prompt = data.get('prompt', '')

    if not prompt:
        return jsonify({'error': 'Missing prompt'}), 400

    full_prompt = f"Generate a single-page HTML website with inline CSS based on: {prompt}"

    try:
        response = openai.ChatCompletion.create(
            model="gpt-3.5-turbo",
            messages=[
                {"role": "system", "content": "You are a helpful assistant that outputs only HTML and CSS without markdown formatting."},
                {"role": "user", "content": full_prompt}
            ],
            max_tokens=1000,
            temperature=0.7,
        )
        html_code = response.choices[0].message.content.strip()

        # Remove markdown fences if they exist
        if html_code.startswith("```") and html_code.endswith("```"):
            html_code = "\n".join(html_code.split("\n")[1:-1]).strip()

        return jsonify({'html': html_code})

    except Exception as e:
        return jsonify({'error': str(e)}), 500

if __name__ == '__main__':
    app.run(debug=True, host='0.0.0.0', port=int(os.environ.get("PORT", 5000)))
