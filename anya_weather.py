import requests

API_KEY = "TA_CLE_API_ICI"
URL = "https://api.openweathermap.org/data/2.5/weather"

def get_weather(city):
    try:
        r = requests.get(URL, params={"q": city, "appid": API_KEY, "units": "metric", "lang": "fr"})
        data = r.json()
        return f"{city}: {data['main']['temp']}°C, {data['weather'][0]['description']}"
    except:
        return "Erreur météo."
