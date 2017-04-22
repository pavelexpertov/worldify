from flask import Flask, render_template
app = Flask(__name__)

@app.route("/")
def hello():
    return render_template("index.html")

@app.route("/test_map")
def test_map():
    return render_template("test_map.html")

if __name__ == "__main__":
    app.run()
