import os
import sys

CITY = os.environ.get("CITY")
LATITUDE = os.environ.get("LATITUDE")
LONGITUDE = os.environ.get("LONGITUDE")

if not all([CITY, LATITUDE, LONGITUDE]):
    print("MB: As variáveis de ambiente CITY, LATITUDE, e LONGITUDE devem ser definidas.", file=sys.stderr)
    print("Exemplo: CITY='Curitiba' LATITUDE='-25.42' LONGITUDE='-49.27' uv run python main.py", file=sys.stderr)
    sys.exit(1)

RABBITMQ_HOST = os.environ.get("RABBITMQ_HOST", "localhost")
RABBITMQ_PORT = int(os.environ.get("RABBITMQ_PORT", 5552))
RABBITMQ_USER = os.environ.get("RABBITMQ_USER", "admin")
RABBITMQ_PASS = os.environ.get("RABBITMQ_PASS", "admin")
RABBITMQ_STREAM = os.environ.get("RABBITMQ_STREAM", "weather")

API_URL = f"https://api.open-meteo.com/v1/forecast?latitude={LATITUDE}&longitude={LONGITUDE}&current_weather=true"
INTERVALO_SEG = int(os.environ.get("INTERVALO_SEG", 30))