from flask import Flask, request, jsonify, render_template
import requests
import os

app = Flask(__name__)

# ✅ Get SerpAPI key from environment variable (set in Vercel)
SERPAPI_API_KEY = os.getenv("SERPAPI_API_KEY")

# 👉 Home route: serve index.html
@app.route("/")
def home():
    return render_template("index.html")   # Flask looks inside /templates/

# 👉 Search route: API for queries
@app.route("/search", methods=["POST"])
def search_google():
    data = request.get_json()
    query = data.get("query")

    if not query:
        return jsonify({"error": "No query provided"}), 400

    params = {
        "engine": "google",
        "q": query,
        "api_key": SERPAPI_API_KEY
    }
    try:
        response = requests.get("https://serpapi.com/search", params=params)
        data = response.json()

        # Extract best answer
        answer = None
        if "answer_box" in data:
            answer_box = data["answer_box"]
            if "answer" in answer_box:
                answer = answer_box["answer"]
            elif "snippet" in answer_box:
                answer = answer_box["snippet"]
            elif "snippet_highlighted_words" in answer_box:
                answer = ", ".join(answer_box["snippet_highlighted_words"])
        elif "organic_results" in data and len(data["organic_results"]) > 0:
            answer = data["organic_results"][0].get("snippet", None)

        return jsonify({"answer": answer or "Sorry, I couldn't find an answer."})

    except Exception as e:
        return jsonify({"error": str(e)}), 500


if __name__ == "__main__":
    # ✅ Debug only when running locally, not on Vercel
    app.run(debug=True)
