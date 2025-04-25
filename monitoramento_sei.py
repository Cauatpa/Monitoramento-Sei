import requests
from bs4 import BeautifulSoup
import time

# LINKS
links = [
    "https://sei.rj.gov.br/sei/modulos/pesquisa/md_pesq_processo_exibir.php?rhvLNMLonhi2QStBSsTZGiGoQmCrLQaX2XhbnBMJ8pkwCR3ymzAH-pH3jSIrZ5qWOweyB9pzdjQy283MIK0o50gXlkN-lO6rQyFvnyCed29IcXRH92um7LYd48_9rBuW",
    "https://sei.rj.gov.br/sei/modulos/pesquisa/md_pesq_processo_exibir.php?rhvLNMLonhi2QStBSsTZGiGoQmCrLQaX2XhbnBMJ8pkwCR3ymzAH-pH3jSIrZ5qWOweyB9pzdjQy283MIK0o55Wx-ibG0KZDu_-KZal1Szwg9CiLvm0pexfWKcqAVPnx",
    "https://sei.rj.gov.br/sei/modulos/pesquisa/md_pesq_processo_exibir.php?IC2o8Z7ACQH4LdQ4jJLJzjPBiLtP6l2FsQacllhUf-duzEubalut9yvd8-CzYYNLu7pd-wiM0k633-D6khhQNZceHqbORsdzzNujFrPDR4FMpG8W2nK9gvJsPYzBnVlF",
]

def extrair_dados(link):
    headers = {
        "User-Agent": "Mozilla/5.0"
    }
    resp = requests.get(link, headers=headers)
    if resp.status_code != 200:
        return "Erro", "Erro", "Erro", "Erro"

    soup = BeautifulSoup(resp.text, "html.parser")

    # Número do processo visível na página
    numero_processo = soup.find(string=lambda s: s and "SEI-" in s)
    numero_processo = numero_processo.strip() if numero_processo else "Número não encontrado"

    tipo_texto = "Tipo não encontrado"
    data_texto = "Data não encontrada"
    unidade_texto = "Unidade não encontrada"

    for tabela in soup.find_all("table"):
        headers = [th.get_text(strip=True) for th in tabela.find_all("th")]
        if "Tipo" in headers:
            idx_tipo = headers.index("Tipo")
            idx_data = headers.index("Data") if "Data" in headers else 0
            idx_unidade = headers.index("Unidade") if "Unidade" in headers else -1

            linhas = tabela.find_all("tr")[1:]
            if linhas:
                ultima_linha = linhas[-1]
                colunas = ultima_linha.find_all("td")
                if len(colunas) > idx_tipo:
                    tipo_texto = colunas[idx_tipo].get_text(strip=True)
                if len(colunas) > idx_data:
                    data_texto = colunas[idx_data].get_text(strip=True)
                if idx_unidade != -1 and len(colunas) > idx_unidade:
                    unidade_texto = colunas[idx_unidade].get_text(strip=True)
            break

    return numero_processo, data_texto, tipo_texto, unidade_texto

# Execução
print("\n🔍 Verificando processos SEI:")
for link in links:
    numero, data, tipo, unidade = extrair_dados(link)
    print(f"- {numero} | Última movimentação: {data} | Descrição: {tipo} | Unidade: {unidade}")
    time.sleep(1)
