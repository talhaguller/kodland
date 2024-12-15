from flask import Flask, render_template, request, redirect, url_for, session
from models import db, Question, UserScore
import os

app = Flask(__name__)
app.secret_key = "4'^E<S]XabO6A8DL?5tRh%tB_wG5;Js-"  # Gizli anahtar
app.config['SQLALCHEMY_DATABASE_URI'] = 'sqlite:///database.db'
app.config['SQLALCHEMY_TRACK_MODIFICATIONS'] = False
db.init_app(app)

@app.before_first_request
def create_tables():
    db.create_all()
    # Örnek soruları ekleme
    if not Question.query.first():
        db.session.add_all([
            Question(text="Python'da AI geliştirme nedir?", 
                     option1="NLP", 
                     option2="Computer Vision", 
                     option3="Model Eğitimi", 
                     correct_option="Model Eğitimi"),
                     
            Question(text="Computer Vision hangi alanda kullanılır?", 
                     option1="Görsel Veri Analizi", 
                     option2="Metin Analizi", 
                     option3="Ses İşleme", 
                     correct_option="Görsel Veri Analizi"),
                     
            Question(text="NLP neyi ifade eder?", 
                     option1="Ses İşleme", 
                     option2="Doğal Dil İşleme", 
                     option3="Veritabanı Yönetimi", 
                     correct_option="Doğal Dil İşleme"),

            Question(text="Yapay Zeka'nın alt dallarından biri aşağıdakilerden hangisidir?", 
                     option1="Web Geliştirme", 
                     option2="Makine Öğrenimi", 
                     option3="Bulut Bilişim", 
                     correct_option="Makine Öğrenimi")
        ])
        db.session.commit()

    db.create_all()
    # Örnek soruları ekleme
    if not Question.query.first():
        db.session.add_all([
            Question(text="Python'da AI geliştirme nedir?", option1="NLP", option2="Computer Vision", option3="Model Eğitimi", correct_option="Model Eğitimi"),
            Question(text="Computer Vision hangi alanda kullanılır?", option1="Görsel Veri Analizi", option2="Metin Analizi", option3="Ses İşleme", correct_option="Görsel Veri Analizi"),
            Question(text="NLP neyi ifade eder?", option1="Ses İşleme", option2="Doğal Dil İşleme", option3="Veritabanı Yönetimi", correct_option="Doğal Dil İşleme")
        ])
        db.session.commit()

@app.route("/", methods=["GET", "POST"])
def index():
    if request.method == "POST":
        session['username'] = request.form['username']
        return redirect(url_for('quiz'))
    return render_template("index.html")

@app.route("/quiz", methods=["GET", "POST"])
def quiz():
    if 'username' not in session:
        return redirect(url_for('index'))
    
    username = session['username']
    questions = Question.query.all()
    user = UserScore.query.filter_by(username=username).first()
    highest_score = user.highest_score if user else 0
    total = Question.query.count()
    
    # En yüksek skoru yüzde olarak hesapla
    highest_percentage = (highest_score / total) * 100 if total > 0 else 0
    highest_percentage = round(highest_percentage, 2)
    
    return render_template("quiz.html", questions=questions, highest_score=highest_percentage, username=username)

@app.route("/submit", methods=["POST"])
def submit():
    if 'username' not in session:
        return redirect(url_for('index'))
    
    username = session['username']
    score = 0
    total = Question.query.count()
    questions = Question.query.all()

    # Skoru hesapla
    for question in questions:
        user_answer = request.form.get(str(question.id))
        if user_answer == question.correct_option:
            score += 1

    # En yüksek skor güncellemesi
    user = UserScore.query.filter_by(username=username).first()
    if not user:
        user = UserScore(username=username, highest_score=score)
        db.session.add(user)
    else:
        user.highest_score = max(user.highest_score, score)
    db.session.commit()

    # Yüzde skoru hesapla
    percentage_score = (score / total) * 100 if total > 0 else 0
    percentage_score = round(percentage_score, 2)
    
    # En yüksek skoru yüzde olarak hesapla
    highest_percentage = (user.highest_score / total) * 100 if total > 0 else 0
    highest_percentage = round(highest_percentage, 2)
    
    return render_template("result.html", score=score, total=total, highest_score=highest_percentage, username=username, percentage_score=percentage_score)

@app.route("/logout")
def logout():
    session.pop('username', None)
    return redirect(url_for('index'))

if __name__ == "__main__":
    app.run(debug=True, port=5000)
