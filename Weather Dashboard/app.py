from flask import Flask, render_template, request
import requests
import os

app = Flask(__name__)
app.config['SECRET_KEY'] = os.urandom(24)

@app.route('/')
def index():
    return render_template('index.html')

@app.route('/weather', methods=['POST'])
def weather():
    city = request.form['city']
    api_key = '07582126fec9653382f9bcaeb936881a'
    url = f'http://api.openweathermap.org/data/2.5/weather?q={city}&units=metric&appid={api_key}'
    response = requests.get(url)
    weather_data = response.json()

    if weather_data['cod'] == '404':
        return render_template('weather.html', error='City not found')
    else:
        return render_template('weather.html', weather=weather_data)

if __name__ == '__main__':
    app.run(debug=True)
