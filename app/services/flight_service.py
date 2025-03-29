import requests
import logging
from datetime import datetime
from app.config import FLIGHTAWARE_API_KEY

logger = logging.getLogger(__name__)
BASE_URL = "https://aeroapi.flightaware.com/aeroapi"

IATA_LOOKUP_URL = "https://www.iata.org/en/publications/directories/code-search/"
WORLD_AIRPORT_CODES_URL = "https://www.world-airport-codes.com/"

def format_datetime(iso_datetime):
    """Converts ISO 8601 datetime to a user-friendly format."""
    if not iso_datetime or iso_datetime == "None":
        return "No disponible"
    try:
        return datetime.strptime(iso_datetime, "%Y-%m-%dT%H:%M:%SZ").strftime("%d %b %Y, %H:%M UTC")
    except ValueError:
        return iso_datetime

def get_airport_name(airport_data):
    """Extracts the airport name or returns 'Desconocido' if not found."""
    return airport_data.get("name", "Desconocido") if isinstance(airport_data, dict) else "Desconocido"

def fetch_flights(endpoint: str, airport_code: str, flight_type: str) -> str:
    """Fetches and formats flight data from the FlightAware API."""
    try:
        url = f"{BASE_URL}/airports/{airport_code}/flights/{endpoint}"
        headers = {"x-apikey": FLIGHTAWARE_API_KEY}
        response = requests.get(url, headers=headers)

        # Handle API errors
        if response.status_code != 200:
            logger.error(f"API Error: {response.status_code} - {response.text}")
            return (
                f"⚠️ *No se encontraron vuelos {flight_type}.*\n\n"
                f"Si no conoces el código del aeropuerto, puedes buscarlo aquí:\n"
                f"🔹 [Búsqueda IATA]({IATA_LOOKUP_URL})\n"
                f"🔹 [Lista de aeropuertos]({WORLD_AIRPORT_CODES_URL})"
            )

        flights = response.json().get(endpoint, [])
        if not flights:
            return (
                f"⚠️ *No hay vuelos {flight_type} disponibles.*\n\n"
                f"Si no conoces el código del aeropuerto, puedes buscarlo aquí:\n"
                f"🔹 [Búsqueda IATA]({IATA_LOOKUP_URL})\n"
                f"🔹 [Lista de aeropuertos]({WORLD_AIRPORT_CODES_URL})"
            )

        # Generate flight summary
        summary = f"🛬 *{len(flights)} vuelos {flight_type}.*" if flight_type == "llegando" else f"🛫 *{len(flights)} vuelos {flight_type}.*"

        # Format flight details
        details = [
            f"✈️ {flight.get('ident', 'Desconocido')} ({flight.get('operator', 'Desconocido')})\n"
            f"📍 {'Desde' if flight_type == 'llegando' else 'Destino'}: {get_airport_name(flight.get('origin', {}) if flight_type == 'llegando' else flight.get('destination', {}))}\n"
            f"⏰ Hora estimada: {format_datetime(flight.get('estimated_in' if flight_type == 'llegando' else 'estimated_out', 'No disponible'))}\n"
            f"📌 Estado: {translate_status(flight.get('status', 'Desconocido'))}\n"
            f"---------------------------------"
            for flight in flights[:5]
        ]

        return f"{summary}\n\n" + "\n".join(details)

    except requests.exceptions.RequestException as e:
        logger.error(f"API Connection Error: {e}")
        return "⚠️ *No se pudo conectar con el servicio de vuelos.*"
    except Exception as e:
        logger.error(f"Unexpected Error: {e}")
        return "⚠️ *Error inesperado al obtener los vuelos.*"

def translate_status(status: str) -> str:
    """Translates flight status into a more user-friendly format with emojis."""
    status_mapping = {
        "On Time": "🟢 A tiempo",
        "Delayed": "🟡 Retrasado",
        "Scheduled": "🔵 Programado",
        "Cancelled": "🔴 Cancelado"
    }
    return status_mapping.get(status, "⚪ Desconocido")

def get_scheduled_departures(airport_code: str) -> str:
    """Retrieves scheduled departures for a given airport."""
    return fetch_flights("scheduled_departures", airport_code, "programados")

def get_scheduled_arrivals(airport_code: str) -> str:
    """Retrieves scheduled arrivals for a given airport."""
    return fetch_flights("scheduled_arrivals", airport_code, "llegando")