from flask_sqlalchemy import SQLAlchemy
import json

db = SQLAlchemy()

# model for our reviews
class Review(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    text = db.Column(db.String, nullable=False)
    sentiment = db.Column(db.String, nullable=False)
    embedding = db.Column(db.Text, nullable=False)

    def to_dict(self):
        return {
            'id': self.id,
            'text': self.text,
            'sentiment': self.sentiment,
            'embedding': json.loads(self.embedding) 
        }