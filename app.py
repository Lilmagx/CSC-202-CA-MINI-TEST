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