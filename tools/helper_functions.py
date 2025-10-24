
import google.generativeai as genai

# Sentiment generator

def generate_sentiment(review_text):
    try:
        model = genai.GenerativeModel("gemini-flash-latest")
        prompt = (
            "You are a sentiment analysis expert. "
            "Classify the following review as 'Positive', 'Negative', or 'Neutral'. "
            "Respond with only one of those words.\n"
            f"Review: {review_text}"
        )
        response = model.generate_content(prompt)
        sentiment = response.text.strip()
        return sentiment
    except Exception as e:
        print(f"Error getting sentiment: {e}")
        return "Error"


# Embedding Generator

def generate_embedding(text):

    try:
        embedding_model = genai.embed_content(
            model="models/text-embedding-004",
            content=text
        )
        return embedding_model["embedding"]
    except Exception as e:
        print(f"Error getting embedding: {e}")
        return []
