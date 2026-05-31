import Levenshtein
import re
from abc import ABC, abstractmethod

# 1. Lớp đại diện cho một phân đoạn Audio ngắn
class Segment:
    def __init__(self, audio_url, transcript, duration):
        self.audio_url = audio_url      # Đường dẫn file âm thanh (vd: /static/audio/...)
        self.transcript = transcript    # Đáp án chuẩn văn bản
        self.duration = duration        # Thời lượng đoạn audio (giây)

# 2. Lớp trừu tượng định nghĩa Cấp độ (Tính Đa Hình)
class Level(ABC):
    @abstractmethod
    def check_answer(self, user_input: str, transcript: str) -> float:
        pass

class Level1(Level):
    def check_answer(self, user_input: str, transcript: str) -> float:
        # Level 1: Chấp nhận sai chính tả nhẹ, bỏ qua viết hoa/thường, xóa dấu câu
        s1 = re.sub(r'[.,?!]', '', user_input.lower().strip())
        s2 = re.sub(r'[.,?!]', '', transcript.lower().strip())
        return Levenshtein.ratio(s1, s2) * 100

class Level2(Level):
    def check_answer(self, user_input: str, transcript: str) -> float:
        # Level 2: Khắt khe hơn một chút (Bắt lỗi chính tả, bỏ qua viết hoa)
        return Levenshtein.ratio(user_input.lower().strip(), transcript.lower().strip()) * 100

class Level3(Level):
    def check_answer(self, user_input: str, transcript: str) -> float:
        # Level 3: Nghiêm ngặt tuyệt đối (So khớp từng ký tự bao gồm cả dấu câu, viết hoa)
        return Levenshtein.ratio(user_input.strip(), transcript.strip()) * 100

# 3. Lớp quản lý toàn bộ Bài Học
class AudioLesson:
    def __init__(self, id, title, level_type: str, segments: list):
        self.id = id
        self.title = title
        self.segments = segments
        self.level_type = level_type
        self.total_duration = sum(s.duration for s in segments)
        
        # Đa hình khởi tạo lớp con tương ứng
        if level_type == "Level 1": self.level = Level1()
        elif level_type == "Level 2": self.level = Level2()
        else: self.level = Level3()