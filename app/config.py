import os
import redis

# Environment variables
TELEGRAM_TOKEN = os.getenv("TELEGRAM_TOKEN")
OPENWEATHER_API_KEY = os.getenv("OPENWEATHER_API_KEY")
OPENAI_API_KEY = os.getenv("OPENAI_API_KEY")
FLIGHTAWARE_API_KEY = os.getenv("FLIGHTAWARE_API_KEY")
REDIS_URL = os.getenv("REDIS_URL", "redis://redis:6379/0")

redis_client = redis.Redis.from_url(REDIS_URL, decode_responses=True)