import asyncio
import sys
import httpx

from . import producer_config
from .weather_client import WeatherClient
from .producer_service import StreamProducer

async def main():    
    print(f"\nProdutor '{producer_config.CITY}' iniciando...")
    
    try:
        async with httpx.AsyncClient() as http_client:
            
            weather_service = WeatherClient(http_client, producer_config.API_URL)
            
            stream_producer = StreamProducer()
            
            await stream_producer.run(weather_service)
            
    except KeyboardInterrupt:
        print(f"\nProdutor '{producer_config.CITY}' encerrando...")
    except Exception as e:
        print(f"Erro fatal no main: {e}", file=sys.stderr)

if __name__ == "__main__":
    try:
        asyncio.run(main())
    except KeyboardInterrupt:
        print("\nProdutor encerrado...")