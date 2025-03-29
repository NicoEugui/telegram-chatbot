import requests
import logging
from app.config import OPENWEATHER_API_KEY

logger = logging.getLogger(__name__)

def get_weather(city: str) -> dict:
    """Fetches weather data from OpenWeatherMap and returns it as a dictionary."""
    city = city.title()  # Capitalize city name

    try:
        url = (
            f"http://api.openweathermap.org/data/2.5/weather?"
            f"q={city}&appid={OPENWEATHER_API_KEY}&units=metric&lang=es"
        )
        response = requests.get(url)
        data = response.json()
        
        logger.info(f"📡 OpenWeather response for {city}: {response.text}")

        if response.status_code == 200:
            return {
                "temp": round(data["main"]["temp"], 1),
                "description": data["weather"][0]["description"],
                "humidity": data["main"]["humidity"],
                "wind_speed": data["wind"]["speed"],
                "full_data": data
            }
        
        error_message = data.get("message", "Error desconocido.")
        logger.error(f"❌ Weather API error for {city}: {error_message}")
        return {"error": f"No se pudo obtener la información del clima para {city}."}

    except requests.exceptions.RequestException as e:
        logger.error(f"🚨 OpenWeather connection error: {e}")
        return {"error": "No se pudo conectar con el servicio de clima."}

    except Exception as e:
        logger.error(f"⚠️ Unexpected error: {e}")
        return {"error": f"Error inesperado: {e}"}
