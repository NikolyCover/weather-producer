import asyncio
from rstream import OffsetType, ConsumerOffsetSpecification

from .consumer_service import StreamConsumer
from . import message_handlers

def get_user_choice() -> tuple[ConsumerOffsetSpecification, callable]:
    print("========================= Consumidor de Clima =========================")
    print("[1] Feed em Tempo Real (Todas as cidades)")
    print("[2] Histórico de uma cidade específica")
    
    while True:
        choice = input("\nEscolha uma opção (1 ou 2): ").strip()
        
        if choice == '1':
            offset = ConsumerOffsetSpecification(OffsetType.NEXT)
            callback = message_handlers.create_realtime_handler()
            return offset, callback
            
        elif choice == '2':
            city = input("\nDigite o nome da cidade para filtrar (ex: Curitiba): ").strip()
            if not city:
                print("Nome da cidade não pode ser vazio.")
                continue
                
            offset = ConsumerOffsetSpecification(OffsetType.FIRST)
            callback = message_handlers.create_history_handler(city)
            return offset, callback
            
        else:
            print("Opção inválida. Tente novamente.")

async def main():
    offset_spec, callback_func = get_user_choice()
    
    consumer_service = StreamConsumer()
    
    await consumer_service.run(offset_spec, callback_func)

if __name__ == "__main__":
    try:
        asyncio.run(main())
    except KeyboardInterrupt:
        print("\nPrograma encerrado.")