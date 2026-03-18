from datetime import datetime
from collections import deque


class Question:
    """Represents a single quiz question about countries."""

    def __init__(self, question_text, options, correct_answer, country):
        self.question_text = question_text
        self.options = options          # list of 4 option strings
        self.correct_answer = correct_answer   # e.g. "A"
        self.country = country
        self.created_at = datetime.now()

    def check_answer(self, user_answer):
        """Returns True if the user's answer matches the correct answer."""
        return user_answer.strip().upper() == self.correct_answer.strip().upper()
    
    def to_dict(self):
        return {
            "question_text": self.question_text,
            "options": self.options,
            "correct_answer": self.correct_answer,
            "country": self.country,
        }
    
class QuizSession:
    """Manages a quiz session using a Queue (FIFO) of questions."""

    def __init__(self, player_name):
        self.player_name = player_name
        self.question_queue = deque()   # FIFO Queue — Data Structure requirement
        self.answers = []               # list of (question, user_answer, is_correct)
        self.score = 0
        self.start_time = datetime.now()
        self.end_time = None
        self.submitted = False

    def load_questions(self, questions):
        """Enqueue all questions into the FIFO queue."""
        for q in questions:
            self.question_queue.append(q)

    def get_next_question(self):
        """Dequeue and return the next question (FIFO)."""
        if self.question_queue:
            return self.question_queue.popleft()
        return None

