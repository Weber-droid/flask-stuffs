from flask import Flask, render_template, redirect, url_for, request
import os
from forms import SignUpForm


app = Flask(__name__)
app.config['SECRET_KEY'] = os.urandom(24)


@app.route('/')
def home():
    return render_template('base.html')


@app.route('/signup', methods = ["GET", "POST"])
def signup():
    form = SignUpForm()
    if form.validate_on_submit():
        username = ""
        username = form.username.data
        password = form.password.data
        return redirect(url_for('success'))
    else:
        return render_template('signup.html', form = form, username = username, password = password)

if __name__ == '__main__':
    app.run(debug=True)

