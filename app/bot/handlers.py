import logging
from telegram import Update
from telegram.ext import ContextTypes
from app.bot.keyboards import main_keyboard, flight_keyboard
from app.services.openai_service import analyze_sentiment
from app.bot.commands import process_airport_flights, process_weather, process_count, process_analysis

logger = logging.getLogger(__name__)

async def on_start(update: Update, context: ContextTypes.DEFAULT_TYPE) -> None:
    chat_id = update.effective_chat.id
    await context.bot.send_message(
        chat_id=chat_id,
        text="😁 ¡Bienvenido a NimbusBot! Selecciona una opción:",
        reply_markup=main_keyboard()
    )

async def on_help(update: Update, context: ContextTypes.DEFAULT_TYPE) -> None:
    chat_id = update.effective_chat.id
    await context.bot.send_message(
        chat_id=chat_id,
        text=(
            "🆘 *Comandos disponibles en NimbusBot:* 🚀\n\n"
            "`/clima [ciudad]` → Consulta el clima 🌍\n"
            "`/vuelos` → Consulta vuelos ✈️\n"
            "`/analisis [texto]` → Analiza el sentimiento de un mensaje 📊\n"
            "`/contador` → Ve cuántas veces has interactuado con el bot 🔢"
        ),
        parse_mode="Markdown"
    )

async def on_button(update: Update, context: ContextTypes.DEFAULT_TYPE) -> None:
    query = update.callback_query
    await query.answer()
    chat_id = update.effective_chat.id
    data = query.data

    if data == "flights":
        await context.bot.send_message(chat_id=chat_id, text="✈️ ¿Qué deseas consultar?", reply_markup=flight_keyboard())
    elif data == "arrivals":
        context.user_data["flight_mode"] = "arrivals"
        await context.bot.send_message(
            chat_id=chat_id,
            text=(
                "✈️ *¿Desde qué aeropuerto quieres buscar vuelos?*\n\n"
                "🔹 Puedes ingresar el *nombre de la ciudad* o el *código del aeropuerto*.\n"
                "❓ Si no sabes el código, puedes buscarlo aquí:\n"
                "🔹 [Búsqueda IATA](https://www.iata.org/en/publications/directories/code-search/)\n"
                "🔹 [Lista de aeropuertos](https://www.world-airport-codes.com/)"
            ),
            parse_mode="Markdown"
        )
    elif data == "departures":
        context.user_data["flight_mode"] = "departures"
        await context.bot.send_message(
            chat_id=chat_id,
            text=(
                "✈️ *¿Desde qué aeropuerto salen los vuelos?*\n\n"
                "🔹 Puedes ingresar el *nombre de la ciudad* o el *código del aeropuerto*.\n"
                "❓ Si no sabes el código, puedes buscarlo aquí:\n"
                "🔹 [Búsqueda IATA](https://www.iata.org/en/publications/directories/code-search/)\n"
                "🔹 [Lista de aeropuertos](https://www.world-airport-codes.com/)"
            ),
            parse_mode="Markdown"
        )
    elif data == "weather":
        await context.bot.send_message(chat_id=chat_id, text="🌍 ¿En qué ciudad deseas consultar el clima?")
        context.user_data["state"] = "weather"
    elif data == "count":
        await process_count(update, context)
    elif data == "analyze":
        await context.bot.send_message(chat_id=chat_id, text="🧐 Envía un mensaje y analizaré su sentimiento:")
        context.user_data["state"] = "analyze"

async def on_message(update: Update, context: ContextTypes.DEFAULT_TYPE) -> None:
    message_text = update.message.text.strip()
    if "flight_mode" in context.user_data:
        await process_airport_flights(update, context)
    elif "state" in context.user_data:
        state = context.user_data.pop("state")
        if state == "weather":
            await process_weather(update, context, message_text)
        elif state == "analyze":
            await process_analysis(update, context)
    else:
        await update.message.reply_text("❌ No entendí tu mensaje. Usa `/help` para ver los comandos.")

async def on_error(update: object, context: ContextTypes.DEFAULT_TYPE) -> None:
    logger.error(f"❌ Error: {context.error} en update {update}")
    if isinstance(update, Update):
        await update.message.reply_text("⚠️ Ocurrió un error inesperado. Por favor, intenta nuevamente.")

async def on_weather_command(update: Update, context: ContextTypes.DEFAULT_TYPE) -> None:
    chat_id = update.effective_chat.id
    user_input = " ".join(context.args) if context.args else None
    if user_input:
        await process_weather(update, context, user_input)
    else:
        await context.bot.send_message(chat_id=chat_id, text="🌍 Ingresa el nombre de la ciudad para consultar el clima:")
        context.user_data["state"] = "weather"

async def on_flight_command(update: Update, context: ContextTypes.DEFAULT_TYPE) -> None:
    chat_id = update.effective_chat.id
    await context.bot.send_message(chat_id=chat_id, text="✈️ ¿Qué deseas consultar?", reply_markup=flight_keyboard())

async def on_analysis_command(update: Update, context: ContextTypes.DEFAULT_TYPE) -> None:
    user_text = " ".join(context.args) if context.args else None
    if not user_text:
        await update.message.reply_text("❌ Debes ingresar un texto para analizar.\nEjemplo: `/analisis Me siento feliz hoy.`", parse_mode="Markdown")
        return
    sentiment = analyze_sentiment(user_text)
    response = f"📊 *Análisis de Sentimiento:*\n\n{sentiment}\n\n💡 *Nota:* Este análisis se basa en el tono general del mensaje."
    await update.message.reply_text(response, parse_mode="Markdown")

async def on_count_command(update: Update, context: ContextTypes.DEFAULT_TYPE) -> None:
    await process_count(update, context)
