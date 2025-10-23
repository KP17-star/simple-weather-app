
from flask import Flask, render_template, request
import requests

app = Flask(__name__)

@app.route('/')
def home():
    return render_template('index.html')

@app.route('/weather', methods=['POST'])
def weather():
    city = request.form['city']
    try:
        geo_url = f"https://geocoding-api.open-meteo.com/v1/search?name={city}&count=1"
        geo_response = requests.get(geo_url).json()

        if "results" not in geo_response:
            return render_template("result.html", city=city, error="City not found!", weather=None)

        latitude = geo_response['results'][0]['latitude']
        longitude = geo_response['results'][0]['longitude']

        weather_url = f"https://api.open-meteo.com/v1/forecast?latitude={latitude}&longitude={longitude}&current_weather=true"
        weather_response = requests.get(weather_url).json()

        weather_data = weather_response['current_weather']

        return render_template("result.html", city=city, weather=weather_data, error=None)
    except Exception:
        return render_template("result.html", city=city, weather=None, error="Unable to fetch data")

if __name__ == "__main__":
    app.run(debug=True)
