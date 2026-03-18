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
    
    def submit_answer(self, question, user_answer):
        """Record the user's answer and update the score."""
        is_correct = question.check_answer(user_answer)
        if is_correct:
            self.score += 1
        self.answers.append({
            "question": question.question_text,
            "country": question.country,
            "user_answer": user_answer.upper(),
            "correct_answer": question.correct_answer,
            "is_correct": is_correct,
        })

    def finish(self):
        """Mark session as complete and record end time."""
        self.end_time = datetime.now()
        self.submitted = True

    def get_result_summary(self):
        """Return a summary dict for the results page."""
        total = len(self.answers)
        percentage = round((self.score / total) * 100, 1) if total > 0 else 0
        duration = None
        if self.end_time:
            seconds = int((self.end_time - self.start_time).total_seconds())
            duration = f"{seconds // 60}m {seconds % 60}s"
        grade = "Excellent 🏆" if percentage >= 80 else "Good 👍" if percentage >= 50 else "Keep Practising 📚"
        return {
            "player_name": self.player_name,
            "score": self.score,
            "total": total,
            "percentage": percentage,
            "grade": grade,
            "duration": duration,
            "submitted_at": self.end_time.strftime("%Y-%m-%d %H:%M:%S") if self.end_time else "",
            "answers": self.answers,
        }


