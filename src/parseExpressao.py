# Exemplo de fluxo: 4.2 1.0 +
# Lê número 4.2, entra no estado número, recebe o ponto, continua no estado número, recebe o 2, continua no estado número, 
# recebe o espaço, sai do estado número e salva o token "4.2", volta pro estado inicial, recebe o 1, entra no estado número, 
# recebe o ponto, continua no estado número, recebe o 0, continua no estado número, recebe o espaço, sai do estado número e 
# salva o token "1.0", volta pro estado inicial, recebe o +, reconhece como operador e salva o token "+", volta pro estado inicial 
# e termina a leitura da linha.

from utils import addJson

# -- Informações para Debug --
RESET = "\033[0m"
RED = "\033[31m"
GREEN = "\033[32m"
YELLOW = "\033[33m"
BLUE = "\033[34m"
MAGENTA = "\033[35m"
CYAN = "\033[36m"
WHITE = "\033[37m"
erroText = f"{RED}Erro:"

# -- Execução principal --
balance = 0 # Usado para fazer balanceamento de parênteses, incrementa para '(' e decrementa para ')'

def printEstado(state_name, char, lista, index, color):
    print(f"{color}[{state_name}] index={index} char={repr(char)} lista={repr(lista)}{RESET}")

def printTokenConcluido(tokens):
    print(f"{GREEN}lista concluida -> tokens: {tokens}{RESET}")

def parseExpressao(linha, line_number=None):
    print(f'\n-- Processing line "{linha}"')
    global balance, qnt_operandos
    balance, qnt_operandos = 0, 0

    tokens = []
    if not isinstance(linha, str): raise TypeError("parseExpressao espera uma string como 'linha'")

    linha = linha.strip()
    if not linha: return tokens

    estado = estadoInicial
    lista = ""
    index = 0
    
    # Caso final, coloca um espaco para forçar o processamento do último token
    while index <= len(linha):
        char = linha[index] if index < len(linha) else ' '
        estado, lista = estado(char, lista, tokens, linha, index)
        index += 1

    return estadoFinal(tokens, linha, line_number)

def estadoInicial(char, lista, tokens, linha, index):        
    printEstado("estadoInicial", char, lista, index, BLUE)
    if char.isspace(): 
        return estadoInicial, ""

    if char == '(' or char == ')':
        return estadoParenteses(char, tokens, index)

    # Quando ponto, estadoNúmero que irá validar caracter
    if char.isdigit() or char == '.':
        return estadoNumero, char

    # Verifica se menos é subtração ou negativo, checando proximo char
    if char == '-':
        prox = linha[index + 1] if index + 1 < len(linha) else ''
        
        if prox.isdigit():
            return estadoNumero, char
        else:
            return estadoOperador(char, lista, tokens, linha, index)

    # Tratamento de operadores. É esperado ter dois operandos antes do operador.
    if char in "+*/^%":
        global qnt_operandos
        if qnt_operandos >= 2:
            return estadoOperador(char, lista, tokens, linha, index)
        else:
            raise ValueError(f"{erroText} operador '{char}'. Esperado dois operandos antes do operador na posição {index}{RESET}")

    # As letras formam os comandos especiais (RES) ou variveis de memória (MEM, X, Y)
    if char.isalpha():
        return estadoComando, char

    raise ValueError(f"{erroText} caractere desconhecido ou não esperado '{char}' na posição {index}{RESET}")

def estadoNumero(char, lista, tokens, linha, index):
    print('estadoNumero', char, lista, index)

def estadoComando(char, lista, tokens, linha, index):
    print('estadoComando', char, lista, index)
    
def estadoOperador(char, lista, tokens, linha, index):
    print('estadoOperador', char, lista, index)

def estadoParenteses(char, tokens, index):
    if len(tokens) == 0 and char == ')':
        raise ValueError(f"{erroText} parêntese de fechamento ')' no inicio da linha{RESET}")

    global balance
    if char == '(': balance += 1
    elif char == ')': balance -= 1
       
    tokens.append({"token": char, "type": "parenthesis", "position": index})
    printTokenConcluido(tokens)
    return estadoInicial, ""

def estadoFinal(tokens, linha, line_number=None):
    if not tokens: raise ValueError(f"{erroText} expressão vazia ou malformada, nenhum tokeIn reconhecido{RESET}")
    
    global balance
    if balance != 0: raise ValueError(f"{erroText} parênteses mal balanceados{RESET}")

    print(f"{GREEN}Adicionando tokens ao JSON...{RESET}")

    addJson(linha, tokens, line_number)
    return tokens