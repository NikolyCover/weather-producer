import asyncio
import json
import sys
from rstream import Consumer, OffsetType, ConsumerOffsetSpecification

from .. import config

async def on_message(message, message_context):
    try:
        data_str = message.decode('utf-8')
        data = json.loads(data_str)
        
        city = data.get("city", "N/A").upper()
        temp = data.get("temperature_c", "N/A")
        wind = data.get("wind_speed_kmh", "N/A")
        
        print(f"\n[{city}] {temp}°C, Vento: {wind} km/h")
        
    except json.JSONDecodeError:
        print("[ERRO] Mensagem recebida não é um JSON válido.", file=sys.stderr)
    except Exception as e:
        print(f"[ERRO] Falha ao processar mensagem: {e}", file=sys.stderr)

async def start_consumer():    
    print("\nConsumidor em tempo real Iniciando...")
    print(f"Conectando a RabbitMQ no host {config.RABBITMQ_HOST}:{config.RABBITMQ_PORT}")
    print(f"Lendo do stream '{config.RABBITMQ_STREAM}' (apenas novas mensagens)")

    try:
        consumer = Consumer(
            host=config.RABBITMQ_HOST,
            port=config.RABBITMQ_PORT,
            username=config.RABBITMQ_USER,
            password=config.RABBITMQ_PASS
        )
        
        offset_spec = ConsumerOffsetSpecification(OffsetType.NEXT)
        
        await consumer.subscribe(
            stream=config.RABBITMQ_STREAM,
            callback=on_message,
            offset_specification=offset_spec
        )
        
        print("\nAguardando novos dados...\n")
        
        while True:
            await asyncio.sleep(3600)
            
    except ConnectionError as e:
        print(f"Erro de conexão: {e}", file=sys.stderr)
        sys.exit(1)
    except KeyboardInterrupt:
        print("\n\nEncerrando...")
    except Exception as e:
        print(f"Erro inesperado: {e}", file=sys.stderr)

if __name__ == "__main__":
    try:
        asyncio.run(start_consumer())
    except KeyboardInterrupt:
        pass