from flask import Flask
from flask import request
from .deep_learning_object_detection import detect_object

app = Flask(__name__)


@app.route("/", methods=["POST"])
def hello():
    print(request.files['file'])
    files = request.files['file']
    files.save("/Users/arturveres/image.png")
    data = detect_object()
    return data


if __name__ == "__main__":
    app.run(debug=True)
