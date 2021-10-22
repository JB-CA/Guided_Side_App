from flask import Flask


app = Flask(__name__)


@app.route("/")
def hello_world():
    return "Hello World!\n"

@app.route('/signup')
def get_signup():
    return "This will be a sign up form\n"


if __name__ == '__main__':
    app.run(host="localhost", port=8000, debug=True)