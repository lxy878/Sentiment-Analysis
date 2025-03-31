from flask import Flask, request, jsonify, send_from_directory
from sentiment import analyze_sentiment_textblob  # Import the function from sentiment.py
from flask_cors import CORS

app = Flask(__name__, static_folder=".")
CORS(app)  # Enable CORS for all routes

# Global variables to track total reviews and cumulative sentiment score
total_reviews = 0
cumulative_sentiment = 0

@app.route("/")
def serve_frontend():
    return send_from_directory(".", "index.html")  # Serve the index.html file

@app.route("/analyze_text", methods=["POST"])
def analyze_text():
    global total_reviews, cumulative_sentiment
    total_reviews = 0  # Reset total reviews for each new analysis
    cumulative_sentiment = 0  # Reset cumulative sentiment for each new analysis
    data = request.json
    if "text" not in data:
        return jsonify({"error": "No text provided"}), 400
    text = data["text"]
    sentiment = analyze_sentiment_textblob(text)

    # Update global counters
    total_reviews += 1
    cumulative_sentiment += sentiment

    # Calculate average sentiment
    average_sentiment = cumulative_sentiment / total_reviews

    return jsonify({
        "text": text,
        "sentiment_score": sentiment,
        "sentiment": "Positive" if sentiment > 0 else "Negative" if sentiment < 0 else "Neutral",
        "total_reviews": total_reviews,
        "average_sentiment": average_sentiment
    })

@app.route("/analyze_file", methods=["POST"])
def analyze_file():
    global total_reviews, cumulative_sentiment
    total_reviews = 0
    cumulative_sentiment = 0
    if "file" not in request.files:
        return jsonify({"error": "No file provided"}), 400
    file = request.files["file"]
    lines = file.read().decode("utf-8").splitlines()

    results = []
    for line in lines:
        sentiment = analyze_sentiment_textblob(line)
        results.append({
            "line": line,
            "sentiment_score": sentiment,
            "sentiment": "Positive" if sentiment > 0 else "Negative" if sentiment < 0 else "Neutral"
        })

        # Update global counters
        total_reviews += 1
        cumulative_sentiment += sentiment

    # Calculate average sentiment
    average_sentiment = cumulative_sentiment / total_reviews

    return jsonify({
        "results": results,
        "total_reviews": total_reviews,
        "average_sentiment": average_sentiment
    })

if __name__ == "__main__":
    app.run(debug=True)