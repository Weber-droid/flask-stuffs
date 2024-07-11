from flask import Flask, render_template, url_for, redirect, request
import os
from flask_wtf import FlaskForm
from wtforms import StringField, PasswordField, SubmitField
from wtforms.validators import DataRequired, Length, EqualTo

app = Flask(__name__)
app.config['SECRET_KEY'] = os.urandom(24)

class SignUpForm(FlaskForm):
    username = StringField('Username: ', validators=[DataRequired(), Length(min=3, max=12)])
    password = PasswordField('Password: ', validators=[DataRequired(), Length(min=6, max=15)])
    confirm_password = PasswordField('Confirm Password: ', validators=[DataRequired(), EqualTo('password')])
    submit = SubmitField('Sign Up')

@app.route('/')
def home():
    return render_template('base.html')

@app.route('/signup' , methods = ["POST", "GET"])
def signup():
    form = SignUpForm()
    if form.validate_on_submit():
        return redirect(url_for('success'))
    return render_template('signup.html', form = form)

@app.route('/success')
def success():
    return "<h1> Yayyy. Welcome!!!!!!!!</h1>"

if __name__ == '__main__':
    app.run(debug=True)
