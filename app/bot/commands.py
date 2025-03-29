import logging
import random
from telegram import Update
from telegram.ext import ContextTypes
from app.services.weather_service import get_weather
from app.services.openai_service import get_additional_weather_advice, analyze_sentiment
from app.services.flight_service import get_scheduled_arrivals, get_scheduled_departures
from app.config import redis_client

logger = logging.getLogger(__name__)
logging.basicConfig(level=logging.INFO)

async def on_start(update: Update, context: ContextTypes.DEFAULT_TYPE) -> None:
    chat_id = update.effective_chat.id
    await context.bot.send_message(
        chat_id=chat_id,
        text=(
            "😁 ¡Bienvenido a *NimbusBot*! 🚀\n\n"
            "🔹 Usa los siguientes comandos:\n"
            "`/clima [ciudad]` → Consulta el clima 🌍\n"
            "`/vuelos [código aeropuerto / número de vuelo]` → Consulta vuelos ✈️\n"
            "`/analisis [texto]` → Analiza el sentimiento 📊\n"
            "`/contador` → Ve cuántas veces has interactuado 🔢\n\n"
            "❓ Escribe `/help` si necesitas ayuda."
        ),
        parse_mode="Markdown"
    )

async def on_help(update: Update, context: ContextTypes.DEFAULT_TYPE) -> None:
    chat_id = update.effective_chat.id
    await context.bot.send_message(
        chat_id=chat_id,
        text=(
            "🆘 *Comandos disponibles:* 🚀\n\n"
            "`/clima [ciudad]` → Consulta el clima 🌍\n"
            "`/vuelos [código aeropuerto / número de vuelo]` → Consulta vuelos ✈️\n"
            "`/analisis [texto]` → Analiza el sentimiento 📊\n"
            "`/contador` → Ve cuántas veces has interactuado 🔢\n\n"
            "🔹 Usa los botones interactivos del menú principal."
        ),
        parse_mode="Markdown"
    )

async def on_message(update: Update, context: ContextTypes.DEFAULT_TYPE) -> None:
    message_text = update.message.text.strip()
    
    if message_text.startswith("/"):
        await update.message.reply_text("⚠️ Comando no reconocido. Usa `/help`. ")
    else:
        await update.message.reply_text("🤖 Usa `/help` para ver los comandos disponibles.")

async def on_error(update: object, context: ContextTypes.DEFAULT_TYPE) -> None:
    logger.error(f"Error: {context.error} en update {update}")
    if isinstance(update, Update):
        await update.message.reply_text("⚠️ Ocurrió un error inesperado. Intenta nuevamente.")

async def process_weather(update: Update, context: ContextTypes.DEFAULT_TYPE, city: str) -> None:
    city = city.title()
    logger.info(f"Procesando solicitud de clima para: {city}")
    weather_info = get_weather(city)
    
    if "error" in weather_info:
        await update.message.reply_text(
            f"⚠️ No se encontró la ciudad '{city}'.\n\n"
            "🔄 Usa `/clima [ciudad]` y prueba nuevamente.\n"
            "Ejemplo: `/clima Montevideo`",
            parse_mode="Markdown"
        )
        return
    
    location = weather_info["full_data"].get("name", city).title()
    wind_kmh = round(weather_info["wind_speed"] * 3.6, 1)
    advice = get_additional_weather_advice(city, weather_info)
    
    response = (
        f"🌍 *Ubicación:* {location}\n"
        f"🌡️ *Temperatura:* {weather_info['temp']}°C\n"
        f"💨 *Viento:* {wind_kmh} km/h\n"
        f"💧 *Humedad:* {weather_info['humidity']}%\n"
        f"🌥️ *Condiciones:* {weather_info['description'].capitalize()}\n\n"
        f"📝 *Consejo:* {advice}"
    )
    
    logger.info(f"Enviando mensaje a Telegram:\n{response}")
    await update.message.reply_text(response, parse_mode="Markdown")

async def process_count(update: Update, context: ContextTypes.DEFAULT_TYPE) -> None:
    user_id = update.effective_user.id
    count = redis_client.incr(f"count:{user_id}")
    chat_id = update.effective_chat.id
    
    messages = [
        "🎉 ¡Tu primera interacción! 🚀",
        f"💡 Has interactuado *{count}* veces. ¡Sigue explorando! ✨",
        f"🔥 Ya llevas *{count}* interacciones. ¡Gracias por usar NimbusBot! 🚀",
        f"💪 *{count}* interacciones... ¡Te estás volviendo un experto! 😎"
    ]
    
    response = messages[min(count - 1, len(messages) - 1)]
    await context.bot.send_message(chat_id=chat_id, text=response, parse_mode="Markdown")

async def process_analysis(update: Update, context: ContextTypes.DEFAULT_TYPE) -> None:
    user_text = update.message.text.strip()
    if not user_text:
        await update.message.reply_text("🤔 Envíame un mensaje y analizaré su sentimiento.", parse_mode="Markdown")
        return
    
    sentiment = analyze_sentiment(user_text)
    response = f"📊 *Análisis de Sentimiento:*\n\n{sentiment}\n\n💡 *Nota:* Basado en el tono general del mensaje."
    await update.message.reply_text(response, parse_mode="Markdown")

async def process_airport_flights(update: Update, context: ContextTypes.DEFAULT_TYPE) -> None:
    user_input = update.message.text.strip().upper()
    chat_id = update.effective_chat.id
    
    if "flight_mode" not in context.user_data:
        await update.message.reply_text("⚠️ Primero selecciona si deseas ver arribos o salidas.")
        return
    
    mode = context.user_data.pop("flight_mode")
    flights = get_scheduled_arrivals(user_input) if mode == "arrivals" else get_scheduled_departures(user_input)
    title = f"🛬 *Arribos programados en {user_input}:*" if mode == "arrivals" else f"🛫 *Salidas programadas desde {user_input}:*"
    
    if isinstance(flights, str):
        await update.message.reply_text(f"{title}\n\n{flights}", parse_mode="Markdown")
    elif isinstance(flights, dict) and "error" in flights:
        await update.message.reply_text(f"❌ {flights['error']}")
    else:
        await update.message.reply_text(f"{title}\n\n⚠️ No se pudo procesar la información de los vuelos.", parse_mode="Markdown")