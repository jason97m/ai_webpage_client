from flask import Flask, request, render_template
import requests

app = Flask(__name__)
API_URL = "https://aiwebgenback-b5b8903aef86.herokuapp.com/generate"  # Openai API

@app.route("/", methods=["GET", "POST"])
def index():
    html_result = ""
    prompt = ""

    if request.method == "POST":
        prompt = request.form["prompt"]

        try:
            response = requests.post(API_URL, json={"prompt": prompt})
            print("Raw response:", response.text)  # debug print check
            html_result = response.json().get("html", "No HTML returned")

        except Exception as e:
            html_result = f"<p>Error: {str(e)}</p>"

    return render_template("index.html", prompt=prompt, result=html_result)

if __name__ == "__main__":
    app.run(debug=True)
