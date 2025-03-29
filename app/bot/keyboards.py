from telegram import InlineKeyboardMarkup, InlineKeyboardButton

def main_keyboard():
    """Main menu keyboard."""
    return InlineKeyboardMarkup([
        [InlineKeyboardButton("☀️ Quiero ver el clima", callback_data="weather")],
        [InlineKeyboardButton("🧐 Quiero analizar un mensaje", callback_data="analyze")],
        [InlineKeyboardButton("✈️ Quiero buscar vuelos", callback_data="flights")],
        [InlineKeyboardButton("🔢 Quiero contar!", callback_data="count")]
    ])

def flight_keyboard():
    """Flight options keyboard."""
    return InlineKeyboardMarkup([
        [InlineKeyboardButton("🛬 Arribos", callback_data="arrivals")],
        [InlineKeyboardButton("🛫 Salidas", callback_data="departures")]
    ])
