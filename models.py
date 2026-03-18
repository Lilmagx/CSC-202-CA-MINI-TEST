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
    
    # --- Shared question bank ---

def get_question_bank():
    """Returns a list of Question objects about world countries."""
    data = [
        Question(
            "What is the capital city of Japan?",
            ["A. Beijing", "B. Seoul", "C. Tokyo", "D. Bangkok"],
            "C", "Japan"
        ),
        Question(
            "Which country has the largest population in the world?",
            ["A. USA", "B. India", "C. Russia", "D. Brazil"],
            "B", "India"
        ),
        Question(
            "What is the official language of Brazil?",
            ["A. Spanish", "B. French", "C. Portuguese", "D. English"],
            "C", "Brazil"
        ),
        Question(
            "Which country is both a continent and a country?",
            ["A. Greenland", "B. Antarctica", "C. Australia", "D. Iceland"],
            "C", "Australia"
        ),
        Question(
            "What is the currency of Germany?",
            ["A. Pound", "B. Franc", "C. Lira", "D. Euro"],
            "D", "Germany"
        ),
        Question(
            "Which country has the longest coastline in the world?",
            ["A. Norway", "B. Canada", "C. Russia", "D. USA"],
            "B", "Canada"
        ),
        Question(
            "In which country would you find the ancient ruins of Machu Picchu?",
            ["A. Mexico", "B. Colombia", "C. Peru", "D. Chile"],
            "C", "Peru"
        ),
        Question(
            "What is the smallest country in the world by area?",
            ["A. Monaco", "B. San Marino", "C. Liechtenstein", "D. Vatican City"],
            "D", "Vatican City"
        ),
        Question(
            "Which African country has the most pyramids?",
            ["A. Egypt", "B. Sudan", "C. Ethiopia", "D. Libya"],
            "B", "Sudan"
        ),
        Question(
            "What is the capital of Canada?",
            ["A. Toronto", "B. Vancouver", "C. Ottawa", "D. Montreal"],
            "C", "Canada"
        ),
        Question(
            "Which country is home to the Great Wall?",
            ["A. Japan", "B. Mongolia", "C. China", "D. South Korea"],
            "C", "China"
        ),
        Question(
            "What is the capital city of Nigeria?",
            ["A. Lagos", "B. Kano", "C. Ibadan", "D. Abuja"],
            "D", "Nigeria"
        ),
        Question(
            "Which country invented the sport of cricket?",
            ["A. Australia", "B. India", "C. England", "D. South Africa"],
            "C", "England"
        ),
        Question(
            "What is the largest country in the world by land area?",
            ["A. Canada", "B. USA", "C. China", "D. Russia"],
            "D", "Russia"
        ),
        Question(
            "Which country is known as the 'Land of the Rising Sun'?",
            ["A. China", "B. Japan", "C. South Korea", "D. Vietnam"],
            "B", "Japan"
        ),
        Question(
            "What is the capital of Argentina?",
            ["A. Santiago", "B. Lima", "C. Buenos Aires", "D. Montevideo"],
            "C", "Argentina"
        ),
        Question(
            "Which country has the most natural lakes in the world?",
            ["A. Russia", "B. USA", "C. Finland", "D. Canada"],
            "D", "Canada"
        ),
        Question(
            "In which country is the Sahara Desert located?",
            ["A. It spans multiple countries", "B. Egypt only", "C. Libya only", "D. Algeria only"],
            "A", "Africa"
        ),
        Question(
            "What is the official currency of Japan?",
            ["A. Yuan", "B. Won", "C. Yen", "D. Baht"],
            "C", "Japan"
        ),
    ]
    return data


# Stack for recent quiz history (LIFO) — also fulfills Data Structure requirement
class ResultsHistory:
    """Keeps a LIFO Stack of recent quiz results for the leaderboard."""

    def __init__(self, max_size=10):
        self._stack = []
        self.max_size = max_size

    def push(self, result):
        if len(self._stack) >= self.max_size:
            self._stack.pop(0)   # remove oldest
        self._stack.append(result)

    def get_recent(self):
        """Return results newest-first (LIFO order)."""
        return list(reversed(self._stack))


# Global results history instance
results_history = ResultsHistory()



