import httpx
from typing import Dict, Any

class WeatherClient:    
    def __init__(self, http_client: httpx.AsyncClient, api_url: str):
        self._http_client = http_client
        self._api_url = api_url

    async def fetch_current_weather(self) -> Dict[str, Any]:
        try:
            response = await self._http_client.get(self._api_url)
            response.raise_for_status() 
            
            api_data = response.json()
            current_weather = api_data.get("current_weather", {})
            
            return {
                "api_timestamp": current_weather.get("time"),
                "temperature_c": current_weather.get("temperature"),
                "wind_speed_kmh": current_weather.get("windspeed"),
                "weathercode": current_weather.get("weathercode")
            }
        except httpx.RequestError as e:
            print(f"Erro ao consultar API: {e}", file=sys.stderr)
            raise