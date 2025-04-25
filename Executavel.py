import requests
from bs4 import BeautifulSoup
import pandas as pd
import hashlib
import time
import re

url = "https://raw.githubusercontent.com/Cauatpa/MonitoramentoSei/main/monitoramento_sei.py"

try:
    resposta = requests.get(url)
    if resposta.status_code == 200:
        print("✅ Script atualizado encontrado. Executando...\n")
        exec(resposta.text)
    else:
        print(f"❌ Erro ao baixar o script. Código: {resposta.status_code}")
except Exception as e:
    print(f"❌ Ocorreu um erro durante a execução: {e}")

input("\n🔁 Pressione ENTER para sair...")

