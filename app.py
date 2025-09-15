from flask import Flask, request, jsonify, render_template
import requests
import os
from datetime import datetime
import webbrowser

app = Flask(__name__)

# ✅ Get SerpAPI key from environment variable
SERPAPI_API_KEY = os.getenv("SERPAPI_API_KEY")


@app.route("/")
def home():
    return render_template("index.html")   # Serves templates/index.html


@app.route("/search", methods=["POST"])
def search_google():
    data = request.get_json()
    query = data.get("query", "").lower()

    # --- 🟢 Custom Jarvis commands ---
    if "who are you" in query:
        return jsonify({"answer": "I am your Jarvis assistant."})

    elif "what is your name" in query:
        return jsonify({"answer": "My name is Jarvis."})

    elif "time" in query:
        now = datetime.now().strftime("%H:%M:%S")
        return jsonify({"answer": f"The current time is {now}"})

    elif "date" in query:
        today = datetime.now().strftime("%A, %d %B %Y")
        return jsonify({"answer": f"Today is {today}"})

    elif "play music" in query:
        # 👉 Option 1: Open YouTube for music
        return jsonify({"answer": "Playing music on YouTube 🎶", 
                        "action": "open_url", 
                        "url": "https://music.youtube.com"})

    # --- 🟡 Otherwise, fallback to SerpAPI ---
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
            ab = data["answer_box"]
            if "answer" in ab:
                answer = ab["answer"]
            elif "snippet" in ab:
                answer = ab["snippet"]
            elif "snippet_highlighted_words" in ab:
                answer = ", ".join(ab["snippet_highlighted_words"])
        elif "organic_results" in data and len(data["organic_results"]) > 0:
            answer = data["organic_results"][0].get("snippet", None)

        return jsonify({"answer": answer or "Sorry, I couldn't find an answer."})

    except Exception as e:
        return jsonify({"error": str(e)}), 500


if __name__ == "__main__":
    app.run(debug=True)
