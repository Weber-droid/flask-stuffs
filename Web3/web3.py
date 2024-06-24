from flask import Flask, redirect, url_for, render_template

app = Flask(__name__)

@app.route('/')
def home():
    return "Hey, I am back and this I am on templates rendering"

@app.route('/greet')
def greet():
    return render_template('index.html')

@app.route('/about')
def about():
    return render_template('greet.html', content = ["Weber", "MICKMG", "Kissi&Co"])





if __name__ == '__main__':
    app.run()