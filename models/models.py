from datetime import datetime

from database.database import db
from service.scoring import level1_check, level2_check, level3_check


class User(db.Model):
    __tablename__ = "users"

    id = db.Column(db.Integer, primary_key=True)
    username = db.Column(db.String(80), unique=True, nullable=False)
    email = db.Column(db.String(120), unique=True, nullable=False)
    attempts = db.relationship("Attempt", backref="user", lazy=True)


class AudioLesson(db.Model):
    __tablename__ = "audio_lessons"

    id = db.Column(db.Integer, primary_key=True)
    title = db.Column(db.String(200), nullable=False)
    transcript = db.Column(db.Text, nullable=False)
    level = db.Column(db.Integer, nullable=False)
    attempts = db.relationship("Attempt", backref="lesson", lazy=True)
    segments = db.relationship(
        "Segment",
        backref="lesson",
        lazy=True,
        cascade="all, delete-orphan",
        order_by="Segment.position",
    )

    @property
    def level_label(self):
        return f"Level {self.level}"


class Segment(db.Model):
    __tablename__ = "segments"

    id = db.Column(db.Integer, primary_key=True)
    lesson_id = db.Column(db.Integer, db.ForeignKey("audio_lessons.id"), nullable=False)
    transcript = db.Column(db.Text, nullable=False)
    audio_path = db.Column(db.String(500), nullable=False)
    position = db.Column(db.Integer, nullable=False, default=1)


class Attempt(db.Model):
    __tablename__ = "attempts"

    id = db.Column(db.Integer, primary_key=True)
    user_id = db.Column(db.Integer, db.ForeignKey("users.id"), nullable=True)
    lesson_id = db.Column(db.Integer, db.ForeignKey("audio_lessons.id"), nullable=False)
    score = db.Column(db.Float, nullable=False, default=0)
    accuracy = db.Column(db.Float, nullable=False, default=0)
    duration = db.Column(db.Integer, nullable=False, default=0)
    created_at = db.Column(db.DateTime, default=datetime.utcnow)
    finished_at = db.Column(db.DateTime)


class Level:
    def __init__(self, level_id, level_name):
        self.level_id = level_id
        self.level_name = level_name

    def get_lessons(self):
        return AudioLesson.query.filter_by(level=self.level_id).all()


class Level1(Level):
    def __init__(self):
        super().__init__(level_id=1, level_name="Level 1")

    def check_answer(self, user_input, transcript):
        return level1_check(user_input, transcript)


class Level2(Level):
    def __init__(self):
        super().__init__(level_id=2, level_name="Level 2")

    def check_answer(self, user_input, transcript):
        return level2_check(user_input, transcript)


class Level3(Level):
    def __init__(self):
        super().__init__(level_id=3, level_name="Level 3")

    def check_answer(self, user_input, transcript):
        return level3_check(user_input, transcript)
