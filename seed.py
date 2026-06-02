from app import app
from database.database import db
from models.models import AudioLesson, Segment


def add_lesson(lessons, title, audio_path, transcript, level):
    lesson = AudioLesson(
        title=title,
        transcript=transcript,
        level=level,
    )
    lesson.segments.append(Segment(
        transcript=transcript,
        audio_path=audio_path,
        position=1,
    ))
    lessons.append(lesson)


def seed_database():
    with app.app_context():
        db.create_all()

        if AudioLesson.query.first():
            print("Database already has lessons. Skipped seeding.")
            return

        lessons = []

        add_lesson(
            lessons,
            "Bai Nghe So 1 - Talking about water",
            "static/audio/level1/audio1_1.mp3",
            (
                "I was going to say that I think everyone likes drinking water, but actually, "
                "I do know people that don't like drinking water. I do like drinking water. "
                "I always bring a bottle of water to the office. Neil used to laugh at me "
                "because I had a bottle that was about two litres. So, yeah, I do like water. "
                "What about you?"
            ),
            1,
        )

        add_lesson(
            lessons,
            "Bai Nghe So 2 - Talking about the weather",
            "static/audio/level1/audio1_2.mp3",
            (
                "Freezing. Freezing is literally zero degrees, when the water turns "
                "into ice. But also we use freezing just to mean that something is "
                "very cold. Yeah. So, for example, if you forget your coat, then you "
                "might be very cold. You'd say 'Oh, it's freezing'. But, actually, "
                "maybe it's ten degrees outside."
            ),
            1,
        )

        add_lesson(
            lessons,
            "Bai Nghe So 3 - Halloween",
            "static/audio/level2/audio2_1.mp3",
            (
                "I really like Halloween because of the dressing up. So, fancy dress - you see all of the children "
                "and adults dressing up in fun costumes, scary costumes, in the UK. And I have a lot of memories "
                "of dressing up as all sorts of weird and scary things when I was a child."
            ),
            2,
        )

        add_lesson(
            lessons,
            "Bai Nghe So 4 - Memory",
            "static/audio/level3/audio3_1.mp3",
            (
                "I've got lots of good memories. I think the best memory I have was when I was about eight years "
                "old. I went to a concert. And I went to this concert with my dad, my best friend and her dad, and "
                "it was outside - a summer's day. It was, kind of, sunset time. We were both on our dads' "
                "shoulders, singing, dancing. And she has the exact same memory, so I know that it's real. "
                "It's not fake."
            ),
        

            3,
        )

        for i in range(5, 11):
            level = ((i - 1) % 3) + 1
            slot = ((i - 1) // 3) + 1
            add_lesson(
                lessons,
                f"Bai Nghe So {i}",
                f"static/audio/level{level}/audio{level}_{slot}.mp3",
                f"This is the temporary transcript for listening lesson number {i}.",
                level,
            )

        db.session.add_all(lessons)
        db.session.commit()
        print("Seeded listening lessons successfully.")


if __name__ == "__main__":
    seed_database()
