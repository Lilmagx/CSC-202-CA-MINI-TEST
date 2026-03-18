from flask import Flask, render_template, request, redirect, url_for, session
from models import QuizSession, get_question_bank, results_history
import random

app = Flask(__name__)
app.secret_key = "country_quiz_secret_2024"

# In-memory session store keyed by a simple session id
quiz_sessions = {}


# ──────────────────────────────────────────────
# Route 1 – Home Page
# ──────────────────────────────────────────────
@app.route("/")
def index():
    recent = results_history.get_recent()
    return render_template("index.html", recent_results=recent)

# ──────────────────────────────────────────────
# Route 2 – Start Quiz (POST from home form)
# ──────────────────────────────────────────────
@app.route("/start", methods=["POST"])
def start_quiz():
    player_name = request.form.get("player_name", "").strip()
    if not player_name:
        return redirect(url_for("index"))

    # Create a new QuizSession (OOP)
    quiz = QuizSession(player_name)

    # Load and shuffle questions, then enqueue them (Queue / FIFO)
    questions = get_question_bank()
    random.shuffle(questions)
    quiz.load_questions(questions)

    # Store in server-side dict; keep id in Flask session cookie
    session_id = str(id(quiz))
    quiz_sessions[session_id] = quiz
    session["session_id"] = session_id
    session["q_index"] = 0

    return redirect(url_for("quiz_question"))

