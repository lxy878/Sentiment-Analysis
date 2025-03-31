from textblob import TextBlob

def analyze_sentiment_textblob(text):
    blob = TextBlob(text)
    polarity = blob.sentiment.polarity
    # print(f"Text: {text}")
    # print(f"Polarity: {polarity}")
    return polarity
    # if polarity > 0:
    #     return "Positive"
    # elif polarity < 0:
    #     return "Negative"
    # else:
    #     return "Neutral"

# Example Usage
if __name__ == "__main__":
    # Example review for testing
    review = "I love this sweater! The embroidery is gorgeous and it fits perfectly."
    print(analyze_sentiment_textblob(review))