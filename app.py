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

# ──────────────────────────────────────────────
# Route 3 – Display / Answer a Question
# ──────────────────────────────────────────────
@app.route("/quiz", methods=["GET", "POST"])
def quiz_question():
    session_id = session.get("session_id")
    quiz: QuizSession = quiz_sessions.get(session_id)

    if not quiz:
        return redirect(url_for("index"))

    if request.method == "POST":
        # User submitted an answer
        answer = request.form.get("answer", "")
        current_q_data = session.get("current_question")
        if current_q_data and answer:
            # Reconstruct the Question object from stored dict
            from models import Question
            q = Question(
                current_q_data["question_text"],
                current_q_data["options"],
                current_q_data["correct_answer"],
                current_q_data["country"],
            )
            quiz.submit_answer(q, answer)

        # Check if queue is empty
        if not quiz.question_queue:
            quiz.finish()
            summary = quiz.get_result_summary()
            results_history.push(summary)
            session["result"] = summary
            return redirect(url_for("results"))

        # Dequeue next question (FIFO)
        next_q = quiz.get_next_question()
        session["current_question"] = next_q.to_dict()
        session["q_index"] = session.get("q_index", 0) + 1
        total = len(quiz.answers) + len(quiz.question_queue) + 1
        return render_template(
            "quiz.html",
            question=next_q,
            q_number=session["q_index"],
            total=total,
            player_name=quiz.player_name,
        )

    # GET — serve the first question
    first_q = quiz.get_next_question()
    if not first_q:
        return redirect(url_for("index"))

    session["current_question"] = first_q.to_dict()
    total = len(get_question_bank())
    return render_template(
        "quiz.html",
        question=first_q,
        q_number=1,
        total=total,
        player_name=quiz.player_name,
    )

# ──────────────────────────────────────────────
# Route 4 – Results Page (timestamped)
# ──────────────────────────────────────────────
@app.route("/results")
def results():
    summary = session.get("result")
    if not summary:
        return redirect(url_for("index"))
    return render_template("results.html", summary=summary)


# ──────────────────────────────────────────────
# Route 5 – Leaderboard (Recently Completed)
# ──────────────────────────────────────────────
@app.route("/leaderboard")
def leaderboard():
    recent = results_history.get_recent()
    return render_template("leaderboard.html", recent_results=recent)


if __name__ == "__main__":
    app.run(debug=True)


