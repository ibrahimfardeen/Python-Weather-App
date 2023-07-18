from flask import Flask, render_template, request, session, redirect
import requests
import json

app = Flask(__name__)
app.secret_key = '3a9eb2265870397351caa5b34faac36e487a7d77ca25e35ec3fae7d5bad80449'

# Weather API configuration
API_KEY = '542d4773728d9f704d07738211c002f5'

# Helper function to fetch weather data
def get_weather_data(location):
    url = f'http://api.openweathermap.org/data/2.5/weather?q={location}&appid={API_KEY}'
    print(url)

    response = requests.get(url)
    data = response.json()
    return data

# Helper function to fetch weather forecast
def get_weather_forecast(location):
    url = f'http://api.openweathermap.org/data/2.5/forecast?q={location}&appid={API_KEY}'
    response = requests.get(url)
    data = response.json()
    return data

# Home page route
@app.route('/', methods=['GET', 'POST'])
def index():
    print('Test')
    if request.method == 'POST':
        location = request.form['location']
        session['location'] = location
        return redirect('/weather')
    return render_template('index.html')

# Weather route
@app.route('/weather', methods=['GET'])
def weather():
    print('Test123')
    location = session.get('location')
    if location:
        weather_data = get_weather_data(location)
        print(weather_data)
        temperature = weather_data['main']['temp']
        humidity = weather_data['main']['humidity']
        wind_speed = weather_data['wind']['speed']
        weather_condition = weather_data['weather'][0]['main']
        return render_template('weather.html', location=location, temperature=temperature, humidity=humidity, wind_speed=wind_speed, weather_condition=weather_condition)
    return render_template('weather.html')

# Forecast route
@app.route('/forecast', methods=['GET'])
def forecast():
    location = session.get('location')
    if location:
        weather_forecast = get_weather_forecast(location)
        forecast_list = weather_forecast['list']
        return render_template('forecast.html', location=location, forecast_list=forecast_list)
    return render_template('forecast.html')

if __name__ == '__main__':
    app.run(debug=True)
