
from flask import Flask, request, jsonify
from dotenv import load_dotenv
from database import db, Review


load_dotenv() # env variables

# Flask App and database setup
app = Flask(__name__)
app.config['SQLALCHEMY_DATABASE_URI'] = 'sqlite:///reviews.db' # db connection
app.config['SQLALCHEMY_TRACK_MODIFICATIONS'] = False
db.init_app(app)

if __name__ == '__main__':
    with app.app_context():
        db.create_all() # Create the database and tables
    app.run(debug=True)