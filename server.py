from flask import Flask
from flask import request
from deep_learning_object_detection import detect_object
import json

app = Flask(__name__)


@app.route("/", methods=["POST"])
def hello():
    files = request.files['file']
    files.save("/Users/arturveres/image.png")
    data = detect_object()
    return json.dumps(data)


if __name__ == "__main__":
    app.run(debug=True)
