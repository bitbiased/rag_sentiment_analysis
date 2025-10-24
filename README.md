# RAG Sentiment Analysis

Lightweight Flask REST API that analyzes customer reviews for sentiment, stores review text + sentiment + vector embeddings in SQLite, and answers user questions about the stored reviews using Retrieval-Augmented Generation (RAG).

## Features
- POST `/add-review` — analyze sentiment, generate embedding, store review in SQLite.
- POST `/ask-question` — embed the question, retrieve top-K relevant reviews using cosine similarity, and synthesize an answer using a generative model constrained to the retrieved context.

## Tech stack
- Python 3.12+
- Flask, SQLAlchemy (SQLite)
- NumPy, scikit-learn (cosine similarity)
- One of: Google Gemini (`google-generativeai`) or OpenAI (`openai`) for embeddings & generation (project contains helper code for Gemini by default).

## Quick start

1. Clone the repo

```bash
git clone https://github.com/bitbiased/rag_sentiment_analysis.git
cd rag_sentiment_analysis
```

2. Create & activate a virtual environment (Windows PowerShell example)

```powershell
python -m venv venv
.\venv\Scripts\Activate
```

3. Install dependencies

```powershell
pip install -r requirements.txt
```

4. Configure environment variables

- By default the code uses Google Gemini via `google-generativeai`. Put your Gemini key in a `.env` file at the project root:

```
GEMINI_API_KEY="your-gemini-key-here"
```

- If you prefer OpenAI models, set up `OPENAI_API_KEY` and update the helper code to call OpenAI-compatible methods (or ask me to convert the repo).

5. Run the app

```powershell
python app.py
# or
flask run
```

The server runs on http://127.0.0.1:5000 by default.

## API — examples

1) Add a review

```bash
curl -X POST http://127.0.0.1:5000/add-review \
  -H "Content-Type: application/json" \
  -d '{"review":"The battery life on this phone is incredible, it lasts for two full days!"}'
```

Expected response (example):

```json
{ "message": "Review added successfully!", "id": 1, "sentiment": "Positive" }
```

2) Ask a question (RAG)

```bash
curl -X POST http://127.0.0.1:5000/ask-question \
  -H "Content-Type: application/json" \
  -d '{"question":"What features do users like the most?"}'
```

Response contains a synthesized `answer` and `relevant_reviews_found`.

## Configuration 
- The repository currently includes code that targets Google Gemini (`google-generativeai`) by default. If you see 404s or empty responses:
  - Ensure `GEMINI_API_KEY` is set in `.env` and matches the client used in the code.


