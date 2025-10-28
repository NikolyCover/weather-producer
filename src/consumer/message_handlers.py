import json
import sys
from typing import Dict, Any, Optional
from datetime import datetime

def _translate_weathercode(code: Optional[int]) -> str:
    if code is None:
        return "N/A"
    
    wmo_codes = {
        0: "Céu Limpo",
        1: "Quase Limpo",
        2: "Parcialmente Nublado",
        3: "Nublado",
        45: "Nevoeiro",
        48: "Nevoeiro (c/ gelo)",
        51: "Garoa Leve",
        53: "Garoa Moderada",
        55: "Garoa Forte",
        61: "Chuva Leve",
        63: "Chuva Moderada",
        65: "Chuva Forte",
        71: "Neve Leve",
        73: "Neve Moderada",
        75: "Neve Forte",
        80: "Pancadas de Chuva Leves",
        81: "Pancadas de Chuva Moderadas",
        82: "Pancadas de Chuva Violentas",
        95: "Trovoada",
        96: "Trovoada (c/ granizo leve)",
        99: "Trovoada (c/ granizo forte)",
    }
    
    return wmo_codes.get(code, f"Código {code}")

def _parse_message(message: bytes) -> Optional[Dict[str, Any]]:
    try:
        data_str = message.decode('utf-8')
        return json.loads(data_str)
    except (json.JSONDecodeError, UnicodeDecodeError):
        print("Erro: Mensagem recebida não é um JSON válido.", file=sys.stderr)
    except Exception as e:
        print(f"Erro: Falha ao decodificar mensagem: {e}", file=sys.stderr)
    return None

def _format_output(data: Dict[str, Any]) -> str:
    city = data.get("city", "N/A").upper()
    temp = data.get("temperature_c", "N/A")
    wind = data.get("wind_speed_kmh", "N/A")
    
    api_timestamp_str = data.get("api_timestamp", "")
    producer_timestamp_str = data.get("producer_timestamp", "")
    
    weather_code_num = data.get("weathercode")
    weather_desc = _translate_weathercode(weather_code_num)

    try:
        api_dt = datetime.fromisoformat(api_timestamp_str)
        api_time = api_dt.strftime("%d/%m/%Y %H:%M")
    except (ValueError, TypeError):
        api_time = "data API inv." 

    try:
        producer_dt = datetime.fromisoformat(producer_timestamp_str)
        producer_time = producer_dt.strftime("%d/%m/%Y %H:%M:%S") 
    except (ValueError, TypeError):
        producer_time = "data Prod. inv."

    return f"[{producer_time}] [{city}] {api_time}, {temp}°C, Vento: {wind} km/h - {weather_desc}"

def create_realtime_handler():
    print("\n=======================================================================")
    print("\nExibindo informações climáticas em tempo real...")
    
    async def on_message_realtime(message, message_context):
        data = _parse_message(message)
        
        if data:
            print(_format_output(data))

    return on_message_realtime


def create_history_handler(city_filter: str):
    print("\n=======================================================================")
    print(f"\nExibindo todas as informações climáticas de: {city_filter.upper()}")
    city_filter_lower = city_filter.lower()
    
    async def on_message_history(message, message_context):
        data = _parse_message(message)
        
        if data and data.get("city", "").lower() == city_filter_lower:
            print(_format_output(data))
            
    return on_message_history
