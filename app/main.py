import os
import logging
from telegram.ext import (
    Application, CommandHandler, CallbackQueryHandler, MessageHandler, filters
)
from app.bot.handlers import (
    on_start, on_button, on_message, on_error, on_weather_command,
    on_flight_command, on_analysis_command, on_count_command, on_help, process_airport_flights
)

# Logging configuration
logging.basicConfig(
    format="%(asctime)s - %(name)s - %(levelname)s - %(message)s", 
    level=logging.INFO
)

def main():
    """Initialize the bot and register handlers."""
    TELEGRAM_TOKEN = os.getenv("TELEGRAM_TOKEN")
    if not TELEGRAM_TOKEN:
        raise ValueError("TELEGRAM_TOKEN is not set in environment variables.")

    application = Application.builder().token(TELEGRAM_TOKEN).build()

    # Register command handlers
    application.add_handler(CommandHandler("start", on_start))
    application.add_handler(CommandHandler("help", on_help))
    application.add_handler(CommandHandler("clima", on_weather_command))
    application.add_handler(CommandHandler("vuelos", on_flight_command))
    application.add_handler(CommandHandler("analisis", on_analysis_command))
    application.add_handler(CommandHandler("contador", on_count_command))
    application.add_handler(CallbackQueryHandler(on_button))

    # Handle non-command messages
    application.add_handler(MessageHandler(filters.TEXT & ~filters.COMMAND, on_message))

    # Error handling
    application.add_error_handler(on_error)

    # Start polling
    application.run_polling()

if __name__ == "__main__":
    main()
