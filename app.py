from flask import Flask, render_template, request, redirect, url_for, session
from models import session as db_session, Message
import random

app = Flask(__name__)
app.secret_key = 'secret_key_for_sessions'  # можешь заменить на свой ключ

# --- Главная страница CRM ---
@app.route("/")
def index():
    if 'logged_in' not in session:
        return redirect(url_for('login'))
    messages = db_session.query(Message).order_by(Message.timestamp.desc()).all()
    return render_template("index.html", messages=messages)

# --- Авторизация ---
@app.route("/login", methods=["GET", "POST"])
def login():
    background_id = random.randint(0, 9)  # случайный фон 0–9
    if request.method == "POST":
        username = request.form["username"]
        password = request.form["password"]
        if username == "admin" and password == "12345":
            session['logged_in'] = True
            return redirect(url_for("index"))
        else:
            error = "❌ Неверный логин или пароль"
            return render_template("login.html", error=error, bg_id=background_id)
    return render_template("login.html", error=None, bg_id=background_id)

# --- Выход ---
@app.route("/logout")
def logout():
    session.pop('logged_in', None)
    return redirect(url_for("login"))

if __name__ == "__main__":
    app.run(debug=True)
