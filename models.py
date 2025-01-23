from flask_sqlalchemy import SQLAlchemy

# Create a single db instance that can be used across the app
db = SQLAlchemy()

class DayEntry(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    date = db.Column(db.Date, unique=True, nullable=False)
    completed = db.Column(db.String(20), nullable=False)  # "on_time", "late", "missed"
    mood = db.Column(db.String(20), nullable=False)  # "happy", "sad", "neutral"
    period = db.Column(db.Boolean, default=False)  # Track period days
