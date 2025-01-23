class Config:
    SQLALCHEMY_DATABASE_URI = 'sqlite:///prayer_tracker.db'
    SQLALCHEMY_TRACK_MODIFICATIONS = False  # To prevent a warning from Flask-SQLAlchemy
