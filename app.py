from flask import Flask, render_template, request, redirect
from flask_sqlalchemy import SQLAlchemy
from datetime import datetime
from flask_migrate import Migrate
from config import Config

app = Flask(__name__)
app.config['SQLALCHEMY_DATABASE_URI'] = 'sqlite:///day_tracker.db'
app.config['SQLALCHEMY_TRACK_MODIFICATIONS'] = False

db = SQLAlchemy(app)
migrate = Migrate(app, db)

# Define mood colors and day emojis
MOOD_COLORS = {
    "happy": "violet",
    "sad": "yellow",
    "neutral": "olive",
    "period": "red"
}

DAY_EMOJIS = {
    "on_time": "😊",
    "late": "😐",
    "missed": "😢"
}

# Define the database model
class DayEntry(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    date = db.Column(db.Date, unique=True, nullable=False)
    completed = db.Column(db.String(20), nullable=False)  # "on_time", "late", "missed"
    mood = db.Column(db.String(20), nullable=False)  # "happy", "sad", "neutral"
    period = db.Column(db.Boolean, default=False)  # Track period days

# Create tables if they don't exist
with app.app_context():
    db.create_all()

@app.route('/')
def index():
    entries = DayEntry.query.filter(DayEntry.date.between('2025-01-01', '2025-12-31')).all()
    
    calendar_data = {}
    for entry in entries:
        day = entry.date.strftime('%Y-%m-%d')
        mood_color = MOOD_COLORS.get(entry.mood, "gray")
        if entry.period:
            mood_color = MOOD_COLORS["period"]
        emoji = DAY_EMOJIS.get(entry.completed, "❓")
        calendar_data[day] = {"color": mood_color, "emoji": emoji}

    return render_template('calendar.html', calendar_data=calendar_data)

@app.route('/add', methods=['POST'])
def add_entry():
    date = request.form['date']
    completed = request.form['completed']
    mood = request.form['mood']
    period = 'period' in request.form  # Checkbox for period days

    # Add or update the entry
    existing_entry = DayEntry.query.filter_by(date=datetime.strptime(date, '%Y-%m-%d').date()).first()
    
    if existing_entry:
        existing_entry.completed = completed
        existing_entry.mood = mood
        existing_entry.period = period
    else:
        entry = DayEntry(
            date=datetime.strptime(date, '%Y-%m-%d'),
            completed=completed,
            mood=mood,
            period=period
        )
        db.session.add(entry)

    db.session.commit()

    return redirect('/')

if __name__ == '__main__':
    app.run(host='0.0.0.0', port=5000)
