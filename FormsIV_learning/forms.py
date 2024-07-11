from flask_wtf import FlaskForm
from wtforms import StringField, PasswordField, SubmitField
from wtforms.validators import DataRequired, EqualTo

class SignUpForm(FlaskForm):
    username = StringField('Enter your username: ', validators=[DataRequired()])
    password = PasswordField('Enter your password: ', validators=[DataRequired()])
    confirm_password = PasswordField("Confirm your password: ", validators=[DataRequired(), EqualTo('password')])
    submit = SubmitField("Sign Up")