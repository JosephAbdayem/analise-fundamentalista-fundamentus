- # Fundamentus
Esta é uma pequena API feita em python3 para análise de ações da BOVESPA utilizando o site fundamentus (www.fundamentus.com.br), que retorna os
principais indicadores fundamentalistas em formato JSON.
A API utiliza o microframework Flask.
Também é possível utilizar via linha de comando.

# Linha de comando
    $ python3 fundamentus.py

# API
Execute o server.py e conecte no endereço (ex.: http://127.0.0.1:5000/) com seu browser

# Requirements
    Flask
    lxml

Install with:
    pip3 install -r required.txt


Melhore meu readme.md em markdown com varios emojis e descrevendo melhor como rodar meu projeto onde é necessario rodar a classe fundamentus.py e depois create_csv.py para gerar os dados em planilhas

ChatGPT: 
- # Fundamentus 📊📈

Este é um poderoso e compacto projeto Python3 🐍 desenvolvido para análise de ações da BOVESPA 📈 utilizando o site [Fundamentus](http://www.fundamentus.com.br/) . Ele retorna os principais indicadores fundamentalistas em um formato conveniente e fácil de usar - JSON.

A API foi desenvolvida com a utilização do microframework Flask e pode ser facilmente executada tanto via API como linha de comando. Vamos te mostrar como! 👇
## Como usar via linha de comando 💻 
1. Abra o terminal e navegue até o diretório onde o arquivo `fundamentus.py` está localizado. 
2. Execute o seguinte comando:

```bash

$ python3 fundamentus.py
```
## Como usar via API 🌐 
1. Execute o arquivo `server.py`. 
2. Abra seu navegador preferido e digite o seguinte endereço:

```http

http://127.0.0.1:5000/
```

Pronto, você está conectado à API!
## Gerando dados em planilhas 📑

Para gerar os dados em formato de planilha, siga os passos: 
1. Após executar `fundamentus.py`, execute o arquivo `create_csv.py`. 
2. Isso irá gerar um arquivo CSV com os dados coletados.
## Requisitos 📋

Os seguintes pacotes são necessários para o funcionamento correto da aplicação:
- Flask
- lxml
## Instalação 🔧

Instale os pacotes necessários com o comando:

```bash

pip3 install -r requirements.txt
```



Agora, você está pronto para analisar ações da BOVESPA como um profissional! 💼💰

Nota: Por favor, certifique-se de ter a versão correta do Python (Python 3) e pip instalados em seu sistema antes de começar.---

Esperamos que você aproveite esta ferramenta e faça ótimos investimentos! 💪💲
