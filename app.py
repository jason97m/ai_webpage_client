from flask import Flask, request, render_template
import requests

app = Flask(__name__)
API_URL = "https://aiwebgenback-b5b8903aef86.herokuapp.com/generate" 

@app.route("/", methods=["GET", "POST"])
def index():
    html_result = ""
    prompt = ""

    if request.method == "POST":
        prompt = request.form["prompt"]
        print("=== RAW POST DATA ===", prompt)  # This will log the whole JSON prompt

        try:
            response = requests.post(API_URL, json={"prompt": prompt})
            html_result = response.json().get("html", "No HTML returned")

        except Exception as e:
            html_result = f"<p>Error: {str(e)}</p>"

    return render_template("index.html", prompt=prompt, result=html_result)

if __name__ == "__main__":
    app.run(debug=True)
