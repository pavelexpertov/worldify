from flask import Flask, render_template, request, jsonify
from generate_dataset import get_dataset
from generate_mood_words import generate_words
from run import run_sentiment_analysis
from spotify_lib import generate_playlist
import json

app = Flask(__name__)

@app.route("/")
def hello():
    return render_template("index.html")

@app.route("/generate_playlist", methods=["POST"])
def test_map():
    city = request.form["city"]
    dataset = get_dataset(city)
    words = generate_words(dataset)
    energy_value = run_sentiment_analysis(dataset)
    gen = get_generes(words)
    generate_playlist(gen, 'GB', energy_value)
    return jsonify(dataset)


def get_generes(words):
    with open("static/data/moodwords.json") as data:
        WORDS = json.loads(data.read())
    generes = []
    for word in words:
        for key in WORDS:
            if word in WORDS[key]:
                generes.append(word)
                break
    return generes

if __name__ == "__main__":
    app.run()
