from flask import Flask

app = Flask(__name__)

@app.route('/')
def home():
    return "This is the homepage"


@app.route('/login')
def login():
    return "Click on the link below to login or sign up."

@app.route('/<int:num1>/<int:num2>')
def sum(num1, num2):
    return f"The sum is {num1 + num2}."

@app.route('/<string:user>')
def dashboard(user):
    return f"Welcome {user}"


if __name__ == '__main__':
    app.run()