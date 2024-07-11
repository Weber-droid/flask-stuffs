from flask_wtf import FlaskForm
from wtforms import StringField, PasswordField, SubmitField

class SignUpForm(FlaskForm):
    username = StringField('Enter your username:')
    password = PasswordField('Enter your password:')
    submit = SubmitField('Sign up')