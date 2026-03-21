import json
import os

def lerArquivo(arquivo):
    with open(arquivo, 'r') as f:
        linhas = f.readlines()
    
    print(f"Arquivo '{arquivo}' lido com sucesso. Total de linhas: {len(linhas)}")

    formatado = []
    for linha in linhas:
        formatado.append(linha.strip("\n"))

    return formatado

def resetJson():
    output_path = os.path.join("results", "tokens.txt")
    os.makedirs(os.path.dirname(output_path), exist_ok=True)  # garante que 'results/' exista
    with open(output_path, "w", encoding="utf-8") as f:
        json.dump({"entries": []}, f, ensure_ascii=False, indent=2)


def ler_json():
    output_path = os.path.join("results", "tokens.txt")
    with open(output_path, "r", encoding="utf-8") as f:
        data = json.load(f)
    return data["entries"]

def addJson(linha, tokens, line_number=None):
    output_path = os.path.join("results", "tokens.txt")

    # Ler arquivo JSON completo
    with open(output_path, "r", encoding="utf-8") as f:
        data = json.load(f)

    # adicionar token na lista
    data["entries"].append({"line_number": line_number, "line": linha, "tokens": tokens})

    # adicionar tudo no json
    with open(output_path, "w", encoding="utf-8") as f:
        json.dump(data, f, ensure_ascii=False, indent=2)