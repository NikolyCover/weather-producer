import asyncio
import json
import sys
import httpx
from rstream import Producer

from .. import config
from . import producer_config
from .weather_client import WeatherClient
from datetime import datetime

class StreamProducer:

    def __init__(self):
        self.host = config.RABBITMQ_HOST
        self.port = config.RABBITMQ_PORT
        self.user = config.RABBITMQ_USER
        self.password = config.RABBITMQ_PASS
        self.stream = config.RABBITMQ_STREAM
        print(f"Conectando a RabbitMQ no host {self.host}:{self.port}")
        print(f"Publicando no stream '{self.stream}'")

    async def run(self, weather_service: WeatherClient):
        try:
            async with Producer(
                host=self.host,
                port=self.port,
                username=self.user,
                password=self.password,
            ) as producer:

                stream_args = {"max-length-bytes": 1_000_000_000} # 1GB
                await producer.create_stream(
                    self.stream, exists_ok=True, arguments=stream_args
                )
                print(f"Stream '{self.stream}' pronto.")
                print(f"Publicando dados a cada {producer_config.INTERVALO_SEG}s.\n")

                msg_count = 1

                while True:
                    try:
                        producer_req_time = datetime.now().isoformat()
                        weather_data = await weather_service.fetch_current_weather()
                        
                        message = {
                            "city": producer_config.CITY,
                            "latitude": producer_config.LATITUDE,
                            "longitude": producer_config.LONGITUDE,
                            "producer_timestamp": producer_req_time,
                            **weather_data 
                        }
                        
                        mensagem_bytes = json.dumps(message).encode('utf-8')
                        await producer.send(stream=self.stream, message=mensagem_bytes)
                        
                        print(f"\n[Msg {msg_count}] Publicado: {message}")
                        msg_count += 1

                    except httpx.RequestError:
                        print(f"Erro: falha ao buscar dados. Tentando novamente em {producer_config.INTERVALO_SEG}s...")
                    except Exception as e:
                        print(f"Erro: {e}", file=sys.stderr)
                        await asyncio.sleep(30)

                    await asyncio.sleep(producer_config.INTERVALO_SEG)

        except ConnectionError as e:
            print(f"Erro de conexão com RabbitMQ: {e}", file=sys.stderr)
            sys.exit(1)
        except KeyboardInterrupt:
            pass 
        except Exception as e:
            print(f"Erro: {e}", file=sys.stderr)