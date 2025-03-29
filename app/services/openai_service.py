import openai
from app.config import OPENAI_API_KEY

openai.api_key = OPENAI_API_KEY


def get_additional_weather_advice(city: str, weather_info: dict) -> str:
    """Generates a concise weather-based advice."""
    temp = weather_info.get("temp")
    description = weather_info.get("description", "").lower()
    humidity = weather_info.get("humidity")
    wind_speed = round(weather_info.get("wind_speed", 0) * 3.6, 1)

    prompt = (
        f"Ubicación: {city}. Clima actual: {temp}°C, {description}. "
        f"Humedad: {humidity}%. Viento: {wind_speed} km/h. "
        "Genera un consejo breve y útil (máximo 100 caracteres)."
    )

    try:
        response = openai.ChatCompletion.create(
            model="gpt-4o-mini",
            messages=[{"role": "user", "content": prompt}],
            max_tokens=100
        )
        advice = response.choices[0].message['content'].strip()
        return advice[:97] + "..." if len(advice) > 100 else advice
    except Exception as e:
        return f"⚠️ Error en OpenAI: {e}"


def analyze_sentiment(text: str) -> str:
    """Analyzes sentiment and returns a concise response."""
    try:
        response = openai.ChatCompletion.create(
            model="gpt-4o-mini",
            messages=[
                {
                    "role": "user",
                    "content": (
                        "Analiza el siguiente texto y clasifica su sentimiento en: "
                        "'Positivo 😊', 'Negativo 😞' o 'Neutral 😐'. "
                        "Explica en un tono profesional y accesible. Máximo 150 caracteres.\n\n"
                        f"Texto: \"{text}\""
                    )
                }
            ],
            max_tokens=80
        )
        result = response.choices[0].message['content'].strip()
        return f"📝 {result}"
    except Exception as e:
        return f"⚠️ *Error al procesar el análisis:* {e}"
