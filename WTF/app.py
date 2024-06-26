from flask import Flask, render_template, redirect, url_for
from flask_wtf import FlaskForm
from wtforms import StringField, SubmitField
from wtforms.validators import DataRequired

app = Flask(__name__)
app.config['SECRET_KEY'] = 'Weber-droid'  # Required for CSRF protection

# Step 3: Define the WTForms Form Class

class MyForm(FlaskForm):
    username = StringField('Username', validators=[DataRequired()])
    submit = SubmitField('Submit')

# Step 4: Create a Route and View Function to Handle Form

@app.route('/', methods=['GET', 'POST'])
def index():
    form = MyForm()
    if form.validate_on_submit():
        username = form.username.data
        return redirect(url_for('greet', username=username))
    return render_template('index.html', form=form)

# Step 5: Create a Template to Render the Form

@app.route('/greet/<username>')
def greet(username):
    return f'<h1>Hello, {username}!</h1>'

if __name__ == '__main__':
    app.run(debug=True)
