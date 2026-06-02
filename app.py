from datetime import datetime

from flask import Flask, jsonify, render_template, request, url_for

from database.database import db
from models.models import Attempt, AudioLesson, Level1, Level2, Level3
from service.scoring import calculate_score, get_similarity


app = Flask(__name__)
app.config["SQLALCHEMY_DATABASE_URI"] = "sqlite:///english_listening.db"
app.config["SQLALCHEMY_TRACK_MODIFICATIONS"] = False
db.init_app(app)


class HintHandler:
    def get_hints(self, transcript):
        hints = []
        for word in transcript.split():
            cleaned = word.strip(".,!?;:\"'()")
            if cleaned[:1].isupper() and cleaned not in hints:
                hints.append(cleaned)
        return hints[:5]


def get_level_checker(level):
    return {
        1: Level1(),
        2: Level2(),
        3: Level3(),
    }.get(level, Level1())


@app.route("/")
def index():
    lessons = AudioLesson.query.order_by(AudioLesson.level, AudioLesson.id).all()
    return render_template("index.html", lessons=lessons)


@app.route("/practice/<int:lesson_id>")
def practice(lesson_id):
    lesson = AudioLesson.query.get_or_404(lesson_id)
    attempt = Attempt(lesson_id=lesson.id)
    db.session.add(attempt)
    db.session.commit()
    return render_template(
        "practice.html",
        lesson=lesson,
        attempt_id=attempt.id,
        handler=HintHandler(),
    )


@app.route("/submit/<int:attempt_id>", methods=["POST"])
def submit(attempt_id):
    attempt = Attempt.query.get_or_404(attempt_id)
    payload = request.get_json(silent=True) or {}
    answers = payload.get("answers", {})
    duration = int(payload.get("duration", 0) or 0)
    checker = get_level_checker(attempt.lesson.level)
    segments = attempt.lesson.segments

    if not segments:
        return jsonify({"error": "Lesson has no segments"}), 400

    total_similarity = 0
    passed = 0
    for segment in segments:
        answer = answers.get(str(segment.id), "")
        total_similarity += get_similarity(answer, segment.transcript)
        if checker.check_answer(answer, segment.transcript):
            passed += 1

    accuracy = round((total_similarity / len(segments)) * 100, 2)
    attempt.accuracy = accuracy
    attempt.score = calculate_score(accuracy, passed, len(segments))
    attempt.duration = duration
    attempt.finished_at = datetime.utcnow()
    db.session.commit()

    return jsonify({"redirect_url": url_for("result", attempt_id=attempt.id)})


@app.route("/result/<int:attempt_id>")
def result(attempt_id):
    attempt = Attempt.query.get_or_404(attempt_id)
    return render_template("result.html", attempt=attempt)


@app.route("/history")
def history():
    attempts = Attempt.query.order_by(Attempt.created_at.desc()).all()
    return render_template("history.html", attempts=attempts)


@app.route("/api/lesson/<int:lesson_id>/segments")
def lesson_segments(lesson_id):
    lesson = AudioLesson.query.get_or_404(lesson_id)
    return jsonify({
        "segments": [
            {
                "id": segment.id,
                "transcript": segment.transcript,
                "audio_url": url_for(
                    "static",
                    filename=segment.audio_path.replace("static/", "", 1),
                ),
            }
            for segment in lesson.segments
        ]
    })


@app.route("/api/chart-data")
def chart_data():
    attempts = Attempt.query.order_by(Attempt.created_at.asc()).all()
    return jsonify({
        "labels": [
            (attempt.finished_at or attempt.created_at).strftime("%d/%m %H:%M")
            for attempt in attempts
        ],
        "scores": [attempt.score for attempt in attempts],
        "accuracies": [attempt.accuracy for attempt in attempts],
    })


with app.app_context():
    db.create_all()


if __name__ == "__main__":
    app.run(debug=True)
