# 🌍 Country Quiz — Flask Web Application

A Mini Computer-Based Test (CBT) engine built with **Python** and **Flask** that quizzes users on world countries — capitals, languages, geography, and more.

---

## What the App Does

- Users enter their name and start a 10-question quiz about world countries
- Questions are randomised each session and served one at a time
- After finishing, a **timestamped result page** shows score, grade, duration, and a per-question breakdown
- A **leaderboard** page shows the 10 most recently completed sessions

---

## Core Technical Features

| Requirement | Implementation |
|---|---|
| OOP (Class + `__init__` + methods) | `Question` class, `QuizSession` class, `ResultsHistory` class in `models.py` |
| Data Structure — Queue (FIFO) | `collections.deque` in `QuizSession.question_queue` to serve questions in order |
| Data Structure — Stack (LIFO) | `ResultsHistory._stack` stores recent results newest-first |
| Standard API — `datetime` | `datetime.now()` timestamps session start/end; displayed on results page |
| Flask Routes (≥ 2) | `/` Home, `/start` POST, `/quiz` GET+POST, `/results`, `/leaderboard` |

---

## How to Run Locally

### 1. Prerequisites
- Python 3.8 or newer
- `pip` (comes with Python)

### 2. Clone the repository
```bash
git clone https://github.com/YOUR_USERNAME/country-quiz.git
cd country-quiz
```

### 3. Install Flask
```bash
pip install flask
```

### 4. Run the app
```bash
python app.py
```

### 5. Open in browser
Go to: [http://127.0.0.1:5000](http://127.0.0.1:5000)

---

## Project Structure

```
country_quiz/
├── app.py          # Flask routes and application logic
├── models.py       # OOP classes: Question, QuizSession, ResultsHistory
├── templates/
│   ├── base.html       # Shared layout / navigation
│   ├── index.html      # Home page + name entry form
│   ├── quiz.html       # Question display page
│   ├── results.html    # Timestamped results page
│   └── leaderboard.html # Recent quiz leaderboard
└── README.md
```

---

## Author
CSC 202 — Continuous Assessment Project  
