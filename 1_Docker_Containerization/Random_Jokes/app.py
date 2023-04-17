from flask import Flask, render_template
import requests

app = Flask(__name__)

@app.route('/')
def index():
    joke_data = requests.get('https://v2.jokeapi.dev/joke/Any?blacklistFlags=nsfw,religious,political,racist,sexist,explicit&amount=3').json()
    jokes = joke_data['jokes']
    return render_template('index.html', jokes=jokes)