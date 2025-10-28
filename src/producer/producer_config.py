import os
import sys

CITY = os.environ.get("CITY")
LATITUDE = os.environ.get("LATITUDE")
LONGITUDE = os.environ.get("LONGITUDE")

if not all([CITY, LATITUDE, LONGITUDE]):
    print("Erro: As variáveis de ambiente CITY, LATITUDE, e LONGITUDE devem ser definidas.", file=sys.stderr)
    sys.exit(1)

API_URL = f"https://api.open-meteo.com/v1/forecast?latitude={LATITUDE}&longitude={LONGITUDE}&current_weather=true&timezone=auto"
INTERVALO_SEG = int(os.environ.get("INTERVALO_SEG", 30))