from flask import Flask, render_template, request, jsonify
from generate_dataset import get_dataset
from generate_mood_words import generate_words

app = Flask(__name__)

@app.route("/")
def hello():
    return render_template("index.html")

@app.route("/generate_playlist", methods=["POST"])
def test_map():
    print("In method")
    print("test")
    print(request.form["city"])
    print("test2")
    city = request.form["city"]
    print("before method calls")
    dataset = get_dataset(city)
    print(dataset)
    words = generate_words(dataset)
    print(words)
    return jsonify(dataset)

if __name__ == "__main__":
    app.run()
