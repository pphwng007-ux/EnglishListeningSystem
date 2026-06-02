from difflib import SequenceMatcher


def get_similarity(
        user_input,
        transcript):

    return SequenceMatcher(
        None,
        user_input.lower(),
        transcript.lower()
    ).ratio()


def check_answer(
        user_input,
        transcript,
        threshold):

    similarity = get_similarity(
        user_input,
        transcript
    )

    return similarity >= threshold


def level1_check(
        user_input,
        transcript):

    return check_answer(
        user_input,
        transcript,
        0.75
    )


def level2_check(
        user_input,
        transcript):

    return check_answer(
        user_input,
        transcript,
        0.85
    )


def level3_check(
        user_input,
        transcript):

    return check_answer(
        user_input,
        transcript,
        0.95
    )


def calculate_score(
        accuracy,
        passed_count,
        total_segments):

    if total_segments <= 0:
        return 0

    pass_rate = passed_count / total_segments
    score = accuracy * 0.8 + pass_rate * 20

    return round(min(max(score, 0), 100), 2)
