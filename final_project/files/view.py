from flask import Blueprint, render_template, redirect, request
from flask_login import login_required, current_user
import requests
import json

from files.db_models import Notes

views = Blueprint('views', __name__)

@views.route('/')
@login_required
def home():
    notes = Notes.query.filter_by(user_id = current_user.id).all()
    return render_template("home.html", notes = notes)

@views.route('/landing')
def landing():
    return render_template("landing.html")

@views.app_errorhandler(404)
def page_not_found(e):
    return render_template('404.html'), 404

@views.route("/glossary", methods = ['GET', 'POST'])
@login_required
def glossary():

    title = request.form.get("wordo")
    if title and request.method == "POST":
        response = requests.get(f"https://api.dictionaryapi.dev/api/v2/entries/en/{title}")

        if int(response.status_code) == 200:    
            data = response.json()

            # Getting the word
            word = data[0]['word']
            word = word.capitalize()

            # Getting the definition
            definition = data[0]['meanings']
            definition = definition[0]['definitions']
            definition = definition[0]['definition']
            
            return render_template("glossary.html", definition = definition, word = word)
        else:
            print("Not possible!")
    else:
        return render_template("glossary.html")