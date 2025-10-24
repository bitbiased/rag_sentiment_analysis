import os
import json
import numpy as np
from flask import Flask, request, jsonify
from database import db, Review
from dotenv import load_dotenv
from database import db
import google.generativeai as genai
from sklearn.metrics.pairwise import cosine_similarity
from tools.helper_functions import  generate_sentiment , generate_embedding

load_dotenv() # env variables
genai.configure(api_key=os.getenv("GEMINI_API_KEY"))

#  Flask App and database setup
app = Flask(__name__)
app.config['SQLALCHEMY_DATABASE_URI'] = 'sqlite:///reviews.db' # db creation
app.config['SQLALCHEMY_TRACK_MODIFICATIONS'] = False
db.init_app(app)


# add review to Database route

@app.route('/add-review', methods=['POST'])
def add_review():
    data = request.get_json()
    if not data or 'review' not in data:
        return jsonify({'error': 'Review text is missing'}), 400

    review_text = data['review']

    sentiment = generate_sentiment(review_text) # get sentiment

    embedding = generate_embedding(review_text) # get embeddings

    if sentiment == "Error" or not embedding:
        return jsonify({'error': 'Failed to process review with AI API'}), 500

    new_review = Review(    # store review in DB
        text=review_text,
        sentiment=sentiment,
        embedding=json.dumps(embedding) 
    )
    db.session.add(new_review)
    db.session.commit()

    return jsonify({
        'message': 'Review added successfully!',
        'id': new_review.id,
        'sentiment': new_review.sentiment
    }), 201



# Ask Question route 

@app.route('/ask-question', methods=['POST'])
def ask_question():
    data = request.get_json()
    if not data or 'question' not in data:
        return jsonify({'error': 'Question is missing'}), 400

    question_text = data['question']

    # RAG

    question_embedding = generate_embedding(question_text) # convert user ques. to embeddings.

    if not question_embedding:
        return jsonify({'error': 'Failed to create embedding for the question'}), 500

    all_reviews = Review.query.all()  # retriving all the reviews from DB
    if not all_reviews:
        return jsonify({'answer': "I don't have any reviews yet to answer this question."})

  
    review_embeddings = np.array([json.loads(review.embedding) for review in all_reviews])

    question_embedding_np = np.array(question_embedding).reshape(1, -1)

    
    similarities = cosine_similarity(question_embedding_np, review_embeddings) # Using cosine similarity to find the 'distance' between the question and each review

   
    top_k = min(3, len(all_reviews)) # Getting top 3, or less reviews
    top_indices = similarities[0].argsort()[-top_k:][::-1]
    
    relevant_reviews = [all_reviews[i].text for i in top_indices]
    
   
    # Building a prompt for the LLM

    context = "\n".join(f"- {review}" for review in relevant_reviews)
    prompt = f"""
    You are a helpful customer support assistant. Answer the user's question based ONLY on the provided context of customer reviews. If the context doesn't contain the answer, say "I cannot answer this question based on the provided reviews."

    Context of relevant reviews:
    {context}

    Question:
    {question_text}

    Answer:
    """

    # Generate the final answer
    try:
        model = genai.GenerativeModel("gemini-flash-latest")
        response = model.generate_content(prompt)
        answer = response.text.strip()
        return jsonify({'answer': answer, 'relevant_reviews_found': relevant_reviews})
    except Exception as e:
        print(f"Error generating answer: {e}")
        return jsonify({'error': 'Failed to generate an answer'}), 500



if __name__ == '__main__':
    with app.app_context():
        db.create_all() # Create the database and tables
    app.run(debug=True)