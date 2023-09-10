# ChatBot
Template simples para um ChatBot.

O ficheiro intents.json contém as intenções de perguntas e respostas.

A pasta ipo_model contém o modelo já treinado. Para experimentar basta correr o evaluation.py
## Deploy

1. Python instalado e criar ambiente virtual:
```python 
python -m venv chatbot_env
```

2. Activar ambiente virtual em windows: 
```python
chatbot_env/Scripts/activate
```

2. Em Linux: 
```python
source chatbot_env/Scripts/activate
```

3. Instalar dependências: 
```python
pip install -r requirements.txt
```

4. Na pasta do projecto:
```python
python .\chatapp.py
```
