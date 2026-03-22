import json
import os
import math
from utils import ler_json

def calcularIEEE754(a, b, operador):
    #Regra para norma IEEE 754(float 64 bits):
    
    try:
        if operador == "+": return a + b
        if operador == "-": return a - b
        if operador == "*": return a * b
        if operador == "/":
            if b == 0.0:
                if a == 0.0: return float('nan')
                return float('inf') if a > 0 else float('-inf')
            return a / b
        if operador == "//": return a // b
        if operador == "%": return a % b
        if operador == "^": return math.pow(a, b)
    except OverflowError:
        # Se o número for grande demais para 64 bits, retorna Infinito
        return float('inf')
    except ZeroDivisionError:
        return float('inf')
    return 0.0

def executarExpressao():
    print("\n=== Executar Expressão (Pure Python IEEE 754) ===")

    tokensObjs = ler_json()
    resultados = []

    for linha in tokensObjs:
        tokens = linha['tokens']
        pilha = []
        memoria = ''
        ultimo_token_numero = False
        
        for tokenObj in tokens:
            token = tokenObj['token']
            if token in ["+", "-", "*", "/", "//", "%", "^"]:
                ultimo_token_numero = False
                if len(pilha) >= 2:
                    b = pilha.pop()
                    a = pilha.pop()
                    resultado = calcularIEEE754(a, b, token)
                    pilha.append(resultado)
            elif token == "(":
                pass
            elif token == ")":
                if len(pilha) > 1:
                    pilha = [pilha[0]]
            elif token == "RES":
                if len(pilha) >= 1:
                    n = int(pilha.pop())
                    idx = len(resultados) - n
                    resultado = resultados[idx]["resultado"] if 0 < n <= len(resultados) else 0.0
                    pilha.append(float(resultado))
                    ultimo_token_numero = False
            else:
                try:
                    # Python float é 64-bit por padrão
                    pilha.append(float(token))
                    ultimo_token_numero = True
                except ValueError:
                    if ultimo_token_numero and len(pilha) >= 1:
                        resultado = pilha.pop()
                        memoria = token
                        pilha.append(resultado)
                        ultimo_token_numero = False
                    else:
                        ultimo_token_numero = False
                        for r in reversed(resultados):
                            if r["memoria"] == token:
                                pilha.append(float(r["resultado"]))
                                break

        if pilha:
            res_final = pilha.pop()
            resultados.append({"resultado": res_final, "memoria": memoria})
            linha["resultado"] = res_final
            linha["memoria"] = memoria
        else:
            resultados.append({"resultado": 0.0, "memoria": ''})
            linha["resultado"] = 0.0
            linha["memoria"] = ''

    output_path = os.path.join("results", "tokens.txt")
    with open(output_path, "w", encoding="utf-8") as f:
        json.dump({"entries": tokensObjs}, f, indent=2)

    return tokensObjs