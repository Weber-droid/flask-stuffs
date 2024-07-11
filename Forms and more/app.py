from flask import Flask, render_template, url_for, redirect, request
from forms import SignUpForm
import os

app =Flask(__name__)
app.config['SECRET_KEY'] = os.urandom(24)

@app.route('/')
def home():
    return render_template('home.html')

@app.route('/login', methods = ["POST", "GET"])
def login():
    if request.method == "GET":
        return render_template('login.html')
    elif request.method == "POST":
        user = request.form['username']
        pword = request.form['password']
        
        if user == "weber" and pword == "jess":
            return "Success"
        else:
            return "Failure"
        
@app.route('/signup')
def signup():
    form = SignUpForm()
    return render_template('signup.html', form = form)    
if __name__ == '__main__':
    app.run(debug=True)