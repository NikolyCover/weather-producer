# Sistema de Monitoramento Climático (Pub/Sub com RabbitMQ Streams)

Este projeto é uma implementação de um sistema de monitoramento climático em tempo real, desenvolvido como parte da disciplina de Sistemas Distribuídos. Ele utiliza o paradigma Publicar-Assinar (Publish/Subscribe) através do **RabbitMQ Streams** para demonstrar a comunicação entre múltiplos produtores (simulando estações meteorológicas) e um múltiplos consumidores.

##  Alunos

* Nikoly Cover Pereira
* Vinicius de Oliveira Jimenez

## Tecnologias Utilizadas

* **Python:** Versão 3.9+ (com `asyncio` para concorrência)
* **RabbitMQ Streams:** Como broker de mensagens, fornecendo um log persistente.
* **Docker:** Para executar o RabbitMQ em um container de forma fácil e configurada.
* **Open-Meteo API:** Fonte gratuita de dados meteorológicos em tempo real.
* **uv:** Gerenciador de pacotes e ambientes virtuais Python.

## Arquitetura

1.  **Produtor:** Um script Python que pode ser executado várias vezes simultanemante para simular diversos produtores
    * Consultam periodicamente (a cada 30 segundos) a API Open-Meteo para obter dados climáticos atualizados.
    * Publicam a mensagem (contendo dados da cidade, timestamps e clima) no *stream* `weather` do RabbitMQ.
2.  **RabbitMQ Stream (`weather`):** Atua como um log persistente onde as mensagens são adicionadas. As mensagens não são removidas quando lidas. Ele foi configurado para armazenar até 100 MB.
3.  **Consumidor:** Uma script Python que pode ser executado várias vezes simultaneamente para simular diversos consumidores e que pode operar em dois modos:
    * **Modo Tempo Real:** Conecta-se ao *stream* lendo a partir do final. Exibe os dados de todas as cidades assim que são publicados.
    * **Modo Histórico:** Conecta-se ao *stream* lendo desde o início.
     Filtra e exibe apenas os dados (históricos e em tempo real) de uma cidade específica escolhida pelo usuário.

## Configuração do Ambiente

Siga estes passos para preparar o ambiente de execução.

### Pré-requisitos

* Git
* Python 3.9 ou superior
* Docker

### Passos

1.  **Clonar o Repositório:**
    ```bash
    git clone https://github.com/NikolyCover/weather-producer-consumer.git
    cd weather-producer 
    ```

2.  **Instalar Dependências Python:**
    Recomendamos usar `uv` (que cria o ambiente virtual `.venv` automaticamente):
    ```bash
    pip install uv #caso o uv ainda não esteja instalado
    uv sync
    ```
    Alternativamente, use `pip` e `venv`:
    ```bash
    python -m venv .venv
    source .venv/bin/activate  # Linux/macOS
    # ou: .\.venv\Scripts\activate  # Windows
    pip install -r requirements.txt 
    ```


3.  **Iniciar o RabbitMQ com Docker Compose:**
    O arquivo `docker-compose.yml` na raiz do projeto já está configurado para iniciar o RabbitMQ .


    Execute o seguinte comando na raiz do projeto:
    ```bash
    docker-compose up -d
    ```
    * Para parar o container: `docker-compose down`.

4.  **Verificar RabbitMQ:**
    * Acesse a interface de gerenciamento no seu navegador: `http://localhost:15672`
    * Login: `admin` / Senha: `admin`

## Executando a Aplicação

### 1. Executar os Produtores

Cada produtor precisa ser executado em um **terminal separado**. Você deve definir as variáveis de ambiente `CITY`, `LATITUDE` e `LONGITUDE` para cada um.

**Exemplo - Terminal 1 (Foz do Iguaçu, publicando a cada 10s):**
```bash
CITY='Foz do Iguaçu' LATITUDE='-25.5469' LONGITUDE='-54.5864' uv run python -m src.producer.main
```

**Exemplo - Terminal 2 (Curitiba):**
```bash
CITY='Curitiba' LATITUDE='-25.4297' LONGITUDE='-49.2719' uv run python -m src.producer.main
```

**Exemplo - Terminal 3 (Cascavel):**
```bash
CITY='Cascavel' LATITUDE='-24.9558' LONGITUDE='-53.455' uv run python -m src.producer.main
```
### 2. Executar Consumidor

Abra um **novo terminal** e execute o consumidor:
```bash
uv run python -m src.consumer.main
```

O consumidor apresentará um menu interativo:

* **Opção 1 (Feed em Tempo Real):** Exibirá os dados de todas as cidades que estão sendo publicadas, a partir do momento em que o consumidor foi iniciado.
* **Opção 2 (Histórico):** Perguntará o nome de uma cidade. Em seguida, exibirá todas as mensagens *passadas* para essa cidade (desde o início do *stream*) e continuará exibindo as *novas* mensagens apenas para ela.
