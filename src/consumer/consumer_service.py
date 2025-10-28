import asyncio
import sys
from rstream import Consumer, ConsumerOffsetSpecification

from .. import config

class StreamConsumer:
    def __init__(self):
        self.host = config.RABBITMQ_HOST
        self.port = config.RABBITMQ_PORT
        self.user = config.RABBITMQ_USER
        self.password = config.RABBITMQ_PASS
        self.stream = config.RABBITMQ_STREAM
        print(f"Conectando a RabbitMQ no host {self.host}:{self.port}")

    async def run(self, offset_spec: ConsumerOffsetSpecification, callback_func):
        try:
            consumer = Consumer(
                host=self.host,
                port=self.port,
                username=self.user,
                password=self.password
            )
            
            await consumer.subscribe(
                stream=self.stream,
                callback=callback_func,
                offset_specification=offset_spec
            )
            
            print("\nConsumidor conectado. Aguardando dados...\n")
            
            while True:
                await asyncio.sleep(3600)
                
        except ConnectionError as e:
            print(f"Erro de conexão: {e}", file=sys.stderr)
            sys.exit(1)
        except KeyboardInterrupt:
            print("\n\nEncerrando consumidor...")
        except Exception as e:
            print(f"Erro: {e}", file=sys.stderr)