import asyncio
import json
import sys
import httpx
from rstream import Producer

import config

from weather_client import WeatherClient

async def start_producer():    
    print(f"\nProdutor '{config.CITY}' iniciando...")
    print(f"Conectando a RabbitMQ no host {config.RABBITMQ_HOST}:{config.RABBITMQ_PORT}")
    print(f"Publicando no stream '{config.RABBITMQ_STREAM}'")

    try:
        async with httpx.AsyncClient() as http_client:
            
            weather_service = WeatherClient(http_client, config.API_URL)
            
            async with Producer(
                host=config.RABBITMQ_HOST,
                port=config.RABBITMQ_PORT,
                username=config.RABBITMQ_USER,
                password=config.RABBITMQ_PASS,
            ) as producer:

                stream_args = {"max-length-bytes": 1_000_000_000} # 1GB
                await producer.create_stream(
                    config.RABBITMQ_STREAM, exists_ok=True, arguments=stream_args
                )
                print(f"Stream '{config.RABBITMQ_STREAM}' pronto.")
                print(f"Publicando dados a cada {config.INTERVALO_SEG}s.\n")

                msg_count = 1

                while True:
                    try:
                        weather_data = await weather_service.fetch_current_weather()
                        
                        message = {
                            "city": config.CITY,
                            "latitude": config.LATITUDE,
                            "longitude": config.LONGITUDE,
                            **weather_data 
                        }
                        
                        mensagem_bytes = json.dumps(message).encode('utf-8')

                        await producer.send(stream=config.RABBITMQ_STREAM, message=mensagem_bytes)
                        
                        print(f"\n[Msg {msg_count}] Publicado: {message}")
                        msg_count += 1

                    except httpx.RequestError:
                        print(f"[{config.CITY}] Falha ao buscar dados. Tentando novamente em {config.INTERVALO_SEG}s...")
                    except Exception as e:
                        print(f"[{config.CITY}] Erro inesperado no loop: {e}", file=sys.stderr)
                        await asyncio.sleep(30)

                    await asyncio.sleep(config.INTERVALO_SEG)

    except ConnectionError as e:
        print(f"Erro fatal de conexão com RabbitMQ: {e}", file=sys.stderr)
        sys.exit(1)
    except KeyboardInterrupt:
        print(f"\nProdutor '{config.CITY}' encerrando...")
    except Exception as e:
        print(f"Erro fatal inesperado: {e}", file=sys.stderr)

if __name__ == "__main__":
    try:
        asyncio.run(start_producer())
    except KeyboardInterrupt:
        print("\nProdutor encerrado...")