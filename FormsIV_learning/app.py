from flask import Flask, redirect, url_for, request, render_template
import os
from forms import SignUpForm

app = Flask(__name__)
app.config['SECRET_KEY'] = os.urandom(24)

@app.route('/')
def home():
    return render_template('base.html')

@app.route('/signup')
def signup():
    form = SignUpForm()
    return render_template('signup.html', form = form)







if __name__ == '__main__':
    app.run(debug=True)
