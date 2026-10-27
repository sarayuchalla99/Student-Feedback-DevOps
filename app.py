from flask import Flask, render_template, request, redirect, url_for, flash
import os, sqlite3
from pathlib import Path

app = Flask(__name__)
app.secret_key = os.environ.get("SECRET_KEY", "change-this-secret")
DB_PATH = os.environ.get("DATABASE_PATH", str(Path(__file__).with_name("feedback.db")))

def db_connect():
    conn = sqlite3.connect(DB_PATH)
    conn.row_factory = sqlite3.Row
    return conn

def init_db():
    Path(DB_PATH).parent.mkdir(parents=True, exist_ok=True)
    with db_connect() as db:
        db.execute('''CREATE TABLE IF NOT EXISTS feedback (
            id INTEGER PRIMARY KEY AUTOINCREMENT,
            student_name TEXT NOT NULL, subject TEXT NOT NULL,
            faculty TEXT NOT NULL, rating INTEGER NOT NULL,
            comments TEXT NOT NULL, created_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP)''')

@app.route("/")
def home():
    return render_template("index.html")

@app.route("/feedback", methods=["GET", "POST"])
def feedback():
    if request.method == "POST":
        name = request.form.get("student_name", "").strip()
        subject = request.form.get("subject", "").strip()
        faculty = request.form.get("faculty", "").strip()
        comments = request.form.get("comments", "").strip()
        try:
            rating = int(request.form.get("rating", "0"))
        except ValueError:
            rating = 0
        if not all([name, subject, faculty, comments]) or rating not in range(1, 6):
            flash("Please complete all fields and select a rating from 1 to 5.", "error")
            return redirect(url_for("feedback"))
        with db_connect() as db:
            db.execute("INSERT INTO feedback (student_name, subject, faculty, rating, comments) VALUES (?, ?, ?, ?, ?)",
                       (name, subject, faculty, rating, comments))
        flash("Feedback submitted successfully. Thank you!", "success")
        return redirect(url_for("dashboard"))
    return render_template("feedback.html")

@app.route("/dashboard")
def dashboard():
    with db_connect() as db:
        entries = db.execute("SELECT * FROM feedback ORDER BY id DESC").fetchall()
        summary = db.execute("SELECT COUNT(*) AS total, ROUND(AVG(rating), 1) AS average FROM feedback").fetchone()
    return render_template("dashboard.html", entries=entries, summary=summary)

@app.route("/health")
def health():
    return {"status": "healthy"}, 200

init_db()
if __name__ == "__main__":
    app.run(host="0.0.0.0", port=int(os.environ.get("PORT", "5000")))
