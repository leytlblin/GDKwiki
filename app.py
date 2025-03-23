import os
from flask import Flask, render_template, request, redirect, url_for
from flask_sqlalchemy import SQLAlchemy
from datetime import datetime

app = Flask(__name__)

base_dir = os.path.abspath(os.path.dirname(__file__))

# Путь для базы данных
db_path = os.path.join(base_dir, "wiki.db")
app.config["SQLALCHEMY_DATABASE_URI"] = f"sqlite:///{db_path}"
app.config["SQLALCHEMY_TRACK_MODIFICATIONS"] = False
db = SQLAlchemy(app)

# Модель для статей
class Article(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    title = db.Column(db.String(255), nullable=False)
    content = db.Column(db.Text, nullable=False)
    created_at = db.Column(db.DateTime, default=datetime.utcnow)

# Модель для персонажей
class Character(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    name = db.Column(db.String(100), nullable=False)
    quote = db.Column(db.Text, nullable=True)
    gender = db.Column(db.String(50), nullable=False)
    age = db.Column(db.Integer, nullable=True)
    full_name = db.Column(db.String(255), nullable=True)
    origin = db.Column(db.String(50), nullable=False)
    religion = db.Column(db.String(50), nullable=False)
    appearance = db.Column(db.Text, nullable=True)
    personality = db.Column(db.Text, nullable=True)
    history = db.Column(db.Text, nullable=True)
    first_appearance = db.Column(db.String(255), nullable=True)
    image = db.Column(db.String(255), nullable=True)
    created_at = db.Column(db.DateTime, default=datetime.utcnow)

# Модель для мест
class Place(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    name = db.Column(db.String(100), nullable=False)
    quote = db.Column(db.Text, nullable=True)
    image = db.Column(db.String(255), nullable=True)  
    location = db.Column(db.String(100), nullable=False)  
    first_appearance = db.Column(db.String(255), nullable=True)  
    description = db.Column(db.Text, nullable=True)  
    history = db.Column(db.Text, nullable=True)  
    created_at = db.Column(db.DateTime, default=datetime.utcnow)

# Создание таблицы в базе данных
with app.app_context():
    db.create_all()

# Главная страница
@app.route("/")
def index():
    articles = Article.query.all()
    characters = Character.query.all()
    places = Place.query.all()
    return render_template("index.html", articles=articles, characters=characters, places=places)

# Форма для добавления статьи
@app.route("/add_article", methods=["GET", "POST"])
def add_article():
    if request.method == "POST":
        title = request.form["title"].strip()
        content = request.form["content"].strip()
        new_article = Article(title=title, content=content)
        db.session.add(new_article)
        db.session.commit()
        return redirect(url_for("index"))
    return render_template("add_article.html")

# Форма для добавления персонажа
@app.route("/add_character", methods=["GET", "POST"])
def add_character():
    if request.method == "POST":
        name = request.form["name"].strip()
        quote = request.form.get("quote", "").strip()
        gender = request.form["gender"].strip()
        age = request.form.get("age", None)
        age = int(age) if age else None
        full_name = request.form.get("full_name", "").strip()
        origin = request.form["origin"].strip()
        religion = request.form["religion"].strip()
        first_appearance = request.form.get("first_appearance", "").strip()

        image = request.form.get("image", "").strip()
        appearance = request.form.get("appearance", "").strip()
        personality = request.form.get("personality", "").strip()
        history = request.form.get("history", "").strip()

        new_character = Character(
            name=name,
            quote=quote,
            gender=gender,
            age=age,
            full_name=full_name,
            origin=origin,
            religion=religion,
            first_appearance=first_appearance,
            image=image,
            appearance=appearance,
            personality=personality,
            history=history,
        )

        db.session.add(new_character)
        db.session.commit()

        return redirect(url_for("character_page", character_id=new_character.id))

    return render_template("add_character.html")

# Форма для добавления места
@app.route("/add_place", methods=["GET", "POST"])
def add_place():
    if request.method == "POST":
        name = request.form["name"].strip()
        quote = request.form.get("quote", "").strip()
        image = request.form.get("image", "").strip()
        location = request.form["location"].strip()
        first_appearance = request.form.get("first_appearance", "").strip()
        description = request.form.get("description", "").strip()
        history = request.form.get("history", "").strip()

        new_place = Place(
            name=name,
            quote=quote,
            image=image,
            location=location,
            first_appearance=first_appearance,
            description=description,
            history=history,
        )

        db.session.add(new_place)
        db.session.commit()

        return redirect(url_for("place_page", place_id=new_place.id))

    return render_template("add_place.html")

#Страница персонажа
@app.route("/character/<int:character_id>")
def character_page(character_id):
    character = Character.query.get_or_404(character_id)
    return render_template("character.html", character=character)

#Страница места
@app.route("/place/<int:place_id>")
def place_page(place_id):
    place = Place.query.get_or_404(place_id)
    return render_template("place.html", place=place)

#Страница статьи
@app.route("/article/<int:article_id>")
def article_page(article_id):
    article = Article.query.get_or_404(article_id)
    return render_template("article.html", article=article)

#Страница анализа текста
@app.route("/text_analysis")
def text_analysis():
    return render_template("text_analysis.html")

#Запуск
if __name__ == "__main__":
    app.run(debug=True)
