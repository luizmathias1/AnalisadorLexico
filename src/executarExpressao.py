import json
import os
import math
from utils import ler_json

def _is_zero(x):
    return x == 0.0

def calcularIEEE754(a, b, operador):
    try:
        # NaN deve se propagar em operações aritméticas.
        if math.isnan(a) or math.isnan(b):
            return float('nan')

        if operador == "+":
            # (+inf) + (-inf) e (-inf) + (+inf) -> NaN
            if math.isinf(a) and math.isinf(b) and (a > 0) != (b > 0): return float('nan')
            return a + b
        if operador == "-":
            # (+inf) - (+inf) e (-inf) - (-inf) -> NaN
            if math.isinf(a) and math.isinf(b) and (a > 0) == (b > 0): return float('nan')
            return a - b
        if operador == "*":
            # (+-inf) * (+-0) -> NaN
            if (math.isinf(a) and _is_zero(b)) or (math.isinf(b) and _is_zero(a)):return float('nan')
            return a * b
        if operador == "/":
            # (+-inf) / (+-inf) -> NaN
            if math.isinf(a) and math.isinf(b): return float('nan')
            if _is_zero(b):
                # (+-0) / (+-0) -> NaN
                if _is_zero(a): return float('nan')
                # (+-!=0) / (+-0) -> +-inf
                return float('inf') if a > 0 else float('-inf')
            return a / b
        if operador == "//":
            return a // b
        if operador == "%":
            # resto por zero é indefinido -> NaN
            if _is_zero(b):return float('nan')
            # infinito não possui resto definido -> NaN
            if math.isinf(a): return float('nan')
            # x % inf = x para x finito
            if math.isinf(b): return a
            return a % b
        if operador == "^":
            return math.pow(a, b)
    except OverflowError: return float('inf')
    except ValueError: return float('nan')
    except ZeroDivisionError: return float('nan')
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
                pass
                # if len(pilha) > 1:
                #     pilha = [pilha[0]]
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