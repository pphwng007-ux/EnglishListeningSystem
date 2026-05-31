from datetime import datetime

from flask import Flask, abort, redirect, render_template, request, session, url_for


app = Flask(__name__)
app.config["SECRET_KEY"] = "english-listening-dev-key"


LESSONS = [
    {
        "id": 1,
        "title": "Daily Routine",
        "level": "Level 3",
        "duration": "02:10",
        "topic": "Everyday English",
        "audio": "audio/level3/audio3_1.mp3",
        "description": "Luyen nghe mot doan hoi thoai ngan ve thoi quen hang ngay.",
        "transcript": (
            "Every morning, Emma wakes up at six thirty. She makes a cup of tea, "
            "checks her calendar, and walks to the bus stop. On the way to work, "
            "she listens to an English podcast for fifteen minutes."
        ),
        "questions": [
            {
                "id": "q1",
                "text": "Emma wakes up at...",
                "options": ["six thirty", "seven fifteen", "eight o'clock"],
                "answer": "six thirty",
            },
            {
                "id": "q2",
                "text": "What does she drink in the morning?",
                "options": ["coffee", "tea", "orange juice"],
                "answer": "tea",
            },
            {
                "id": "q3",
                "text": "She listens to a podcast for...",
                "options": ["five minutes", "fifteen minutes", "fifty minutes"],
                "answer": "fifteen minutes",
            },
        ],
    },
    {
        "id": 2,
        "title": "At The Cafe",
        "level": "Level 3",
        "duration": "01:55",
        "topic": "Ordering Food",
        "audio": "audio/level3/audio3_2.mp3",
        "description": "Luyen nghe cach goi mon, hoi gia va xac nhan don hang.",
        "transcript": (
            "A customer orders a chicken sandwich and a small latte. The cashier "
            "asks if the order is for here or to go. The customer says it is to go "
            "and pays by card."
        ),
        "questions": [
            {
                "id": "q1",
                "text": "The customer orders a...",
                "options": ["beef burger", "chicken sandwich", "vegetable soup"],
                "answer": "chicken sandwich",
            },
            {
                "id": "q2",
                "text": "What size is the latte?",
                "options": ["small", "medium", "large"],
                "answer": "small",
            },
            {
                "id": "q3",
                "text": "How does the customer pay?",
                "options": ["by cash", "by card", "by phone"],
                "answer": "by card",
            },
        ],
    },
    {
        "id": 3,
        "title": "Weekend Plan",
        "level": "Level 3",
        "duration": "02:25",
        "topic": "Planning",
        "audio": "audio/level3/audio3_3.mp3",
        "description": "Luyen nghe doan noi ve ke hoach cuoi tuan va thoi gian bieu.",
        "transcript": (
            "Tom and Lily are planning their weekend. On Saturday morning, they "
            "will visit the museum. In the afternoon, they will meet friends at "
            "the park if the weather is sunny."
        ),
        "questions": [
            {
                "id": "q1",
                "text": "Tom and Lily will visit the museum on...",
                "options": ["Friday night", "Saturday morning", "Sunday afternoon"],
                "answer": "Saturday morning",
            },
            {
                "id": "q2",
                "text": "Where will they meet friends?",
                "options": ["at the park", "at the station", "at the library"],
                "answer": "at the park",
            },
            {
                "id": "q3",
                "text": "They will meet friends if the weather is...",
                "options": ["rainy", "windy", "sunny"],
                "answer": "sunny",
            },
        ],
    },
]


def get_lesson(lesson_id):
    return next((lesson for lesson in LESSONS if lesson["id"] == lesson_id), None)


def get_history():
    return session.setdefault("history", [])


@app.route("/")
def dashboard():
    history = get_history()
    completed_ids = {item["lesson_id"] for item in history}
    best_score = max((item["score"] for item in history), default=0)
    average_score = round(
        sum(item["score"] for item in history) / len(history), 1
    ) if history else 0

    stats = {
        "total_lessons": len(LESSONS),
        "completed": len(completed_ids),
        "best_score": best_score,
        "average_score": average_score,
    }
    return render_template("dashboard.html", lessons=LESSONS, stats=stats)


@app.route("/lessons")
def lessons():
    return render_template("lessons.html", lessons=LESSONS)


@app.route("/practice")
def practice_default():
    return redirect(url_for("practice", lesson_id=LESSONS[0]["id"]))


@app.route("/practice/<int:lesson_id>")
def practice(lesson_id):
    lesson = get_lesson(lesson_id)
    if lesson is None:
        abort(404)
    return render_template("practice.html", lesson=lesson)


@app.route("/submit/<int:lesson_id>", methods=["POST"])
def submit(lesson_id):
    lesson = get_lesson(lesson_id)
    if lesson is None:
        abort(404)

    results = []
    correct_count = 0
    for question in lesson["questions"]:
        selected = request.form.get(question["id"], "")
        is_correct = selected == question["answer"]
        correct_count += int(is_correct)
        results.append(
            {
                "question": question["text"],
                "selected": selected or "Chua chon",
                "answer": question["answer"],
                "is_correct": is_correct,
            }
        )

    total = len(lesson["questions"])
    score = round(correct_count / total * 100)
    history = get_history()
    history.insert(
        0,
        {
            "lesson_id": lesson["id"],
            "lesson_title": lesson["title"],
            "score": score,
            "correct": correct_count,
            "total": total,
            "created_at": datetime.now().strftime("%d/%m/%Y %H:%M"),
        },
    )
    session["history"] = history[:20]

    return render_template(
        "result.html",
        lesson=lesson,
        results=results,
        score=score,
        correct_count=correct_count,
        total=total,
    )


@app.route("/result")
def result():
    return redirect(url_for("lessons"))


@app.route("/history")
def history():
    return render_template("history.html", history=get_history())


if __name__ == "__main__":
    app.run(debug=True)
