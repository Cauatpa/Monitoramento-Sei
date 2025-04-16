import requests
from bs4 import BeautifulSoup
import pandas as pd
import hashlib
import time
import re

# LINKS (Para adicionar links e so por = "", / e o link dento das aspas segueguindo da "," )
links = [
    "https://sei.rj.gov.br/sei/modulos/pesquisa/md_pesq_processo_exibir.php?rhvLNMLonhi2QStBSsTZGiGoQmCrLQaX2XhbnBMJ8pkwCR3ymzAH-pH3jSIrZ5qWOweyB9pzdjQy283MIK0o50gXlkN-lO6rQyFvnyCed29IcXRH92um7LYd48_9rBuW",
    "https://sei.rj.gov.br/sei/modulos/pesquisa/md_pesq_processo_exibir.php?rhvLNMLonhi2QStBSsTZGiGoQmCrLQaX2XhbnBMJ8pkwCR3ymzAH-pH3jSIrZ5qWOweyB9pzdjQy283MIK0o55Wx-ibG0KZDu_-KZal1Szwg9CiLvm0pexfWKcqAVPnx",
]

# Function para gerar o Hash
def gerar_id(link):
    return hashlib.md5(link.encode()).hexdigest()

# Extrai o Link e o número do processo
def extrair_dados(link):
    headers = {
        "User-Agent": "Mozilla/5.0"
    }
    resp = requests.get(link, headers=headers)
    if resp.status_code != 200:
        return None, None, None

    soup = BeautifulSoup(resp.text, "html.parser")
    tabelas = soup.find_all("table")

    texto = soup.get_text()
    match = re.search(r"SEI-\d{6}/\d{6}/\d{4}", texto)
    numero_processo = match.group() if match else "Número não encontrado"

    # Procura a data da ultima atualização
    for tabela in tabelas:
        linhas = tabela.find_all("tr")
        for linha in linhas[1:]:
            colunas = linha.find_all("td")
            if len(colunas) >= 2:
                data = colunas[0].get_text(strip=True)
                tipo = colunas[1].get_text(strip=True)
                if re.match(r"\d{2}/\d{2}/\d{4}", data):
                    return numero_processo, data, tipo
    return numero_processo, "Data não encontrada", "Tipo não encontrado"

# Armazenamento de dados
dados = []
print("\n🔍 Verificando processos SEI:")
for link in links:
    numero, data, tipo = extrair_dados(link)
    print(f"- {numero} | Última movimentação: {data} ({tipo})")
    dados.append({
        "numero_processo": numero,
        "data_ultima_movimentacao": data,
        "tipo_movimentacao": tipo,
        "url": link
    })
    time.sleep(1)