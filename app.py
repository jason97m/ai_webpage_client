from flask import Flask, request, jsonify
import openai
import os
import re

app = Flask(__name__)
openai.api_key = os.getenv("OPENAI_API_KEY")

@app.route('/generate', methods=['POST'])
def generate_site():
    data = request.get_json()
    prompt = data.get('prompt', '')

    if not prompt:
        return jsonify({'error': 'Missing prompt'}), 400

    full_prompt = f"Generate a single-page HTML website with inline CSS based on: {prompt}"

    try:
        response = openai.chat.completions.create(
            model="gpt-3.5-turbo",
            messages=[
                {"role": "system", "content": "You are a helpful assistant that ONLY returns raw HTML code without any explanations or markdown formatting."},
                {"role": "user", "content": full_prompt}
            ],
            max_tokens=1000,
            temperature=0.7,
        )
        html_code = response.choices[0].message.content.strip()

        # Remove any leading text before <!DOCTYPE or <html>
        doctype_match = re.search(r"(<\!DOCTYPE html>|<html)", html_code, re.IGNORECASE)
        if doctype_match:
            html_code = html_code[doctype_match.start():]

        # Remove ```html or ``` wrappers if they exist
        if html_code.startswith("```"):
            html_code = re.sub(r"^```(?:html)?\n?", "", html_code)
            html_code = re.sub(r"\n?```$", "", html_code)

        return jsonify({'html': html_code})

    except Exception as e:
        return jsonify({'error': str(e)}), 500


if __name__ == '__main__':
    app.run(debug=True, host='0.0.0.0', port=int(os.environ.get("PORT", 5000)))

