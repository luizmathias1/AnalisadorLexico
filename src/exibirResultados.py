import struct

RESET = "\033[0m"
BOLD = "\033[1m"
DIM = "\033[2m"

COR_NUMERO   = "\033[96m"  # Ciano claro
COR_OPERADOR = "\033[93m"  # Amarelo
COR_COMANDO  = "\033[92m"  # Verde
COR_HEADER   = "\033[1;37m"  # Branco bold

CORES_PARENTESES = [
    "\033[35m",  # Magenta
    "\033[33m",  # Amarelo escuro
    "\033[36m",  # Ciano
    "\033[31m",  # Vermelho
    "\033[34m",  # Azul
    "\033[32m",  # Verde
]


def formatarResultado(res):
    if res != res:  # NaN check (IEEE 754)
        return "NaN"
    elif res == float('inf'):
        return "Inf"
    elif res == float('-inf'):
        return "-Inf"
    else:
        return f"{res:.1f}"


def formatarIEEE754(res):
    bytes_ieee = struct.pack('>d', res)
    return bytes_ieee.hex().upper()


def colorirExpressao(expressao, tokens):
    cores_pos = {}
    profundidade = 0

    for tokenObj in tokens:
        token = tokenObj["token"]
        tipo = tokenObj.get("type", "")
        pos = tokenObj.get("position", -1)
        if pos < 0:
            continue

        if tipo == "parenthesis" and token == "(":
            cor = f"{BOLD}{CORES_PARENTESES[profundidade % len(CORES_PARENTESES)]}"
            for j in range(len(token)):
                cores_pos[pos + j] = cor
            profundidade += 1
        elif tipo == "parenthesis" and token == ")":
            profundidade = max(0, profundidade - 1)
            cor = f"{BOLD}{CORES_PARENTESES[profundidade % len(CORES_PARENTESES)]}"
            for j in range(len(token)):
                cores_pos[pos + j] = cor
        elif tipo == "number":
            for j in range(len(token)):
                cores_pos[pos + j] = COR_NUMERO
        elif tipo == "operator":
            for j in range(len(token)):
                cores_pos[pos + j] = f"{BOLD}{COR_OPERADOR}"
        elif tipo == "command":
            for j in range(len(token)):
                cores_pos[pos + j] = f"{BOLD}{COR_COMANDO}"

    resultado = []
    cor_atual = None
    for i, ch in enumerate(expressao):
        cor = cores_pos.get(i)
        if cor != cor_atual:
            if cor_atual is not None:
                resultado.append(RESET)
            if cor is not None:
                resultado.append(cor)
            cor_atual = cor
        resultado.append(ch)
    if cor_atual is not None:
        resultado.append(RESET)

    return "".join(resultado)


def exibirResultados(resultados):
    if not resultados:
        print("\nNenhuma expressao processada.")
        return

    linhas_tabela = []
    for entry in resultados:
        num_linha = str(entry.get("line_number", ""))
        tokens = entry.get("tokens", [])
        expr_plana = entry.get("line", "")
        expr_colorida = colorirExpressao(expr_plana, tokens)
        res = entry.get("resultado", 0.0)
        memoria = entry.get("memoria", "")
        res_fmt = formatarResultado(res)
        ieee_fmt = formatarIEEE754(res)
        mem_fmt = f"{COR_COMANDO}{memoria}{RESET}" if memoria else f"{DIM}-{RESET}"
        mem_plana = memoria if memoria else "-"
        linhas_tabela.append({
            "num": num_linha,
            "expr_cor": expr_colorida,
            "expr_plana": expr_plana,
            "res": res_fmt,
            "ieee": ieee_fmt,
            "mem_cor": mem_fmt,
            "mem_plana": mem_plana,
        })

    h = ("Linha", "Expressao", "Resultado", "IEEE 754 (64-bit)", "Memoria")

    col_widths = [len(x) for x in h]
    for row in linhas_tabela:
        vals = (row["num"], row["expr_plana"], row["res"], row["ieee"], row["mem_plana"])
        for i, val in enumerate(vals):
            col_widths[i] = max(col_widths[i], len(val))

    def fmt_row_colorida(row):
        campos = [
            (row["num"], row["num"], False),
            (row["expr_cor"], row["expr_plana"], False),
            (row["res"], row["res"], True),
            (row["ieee"], row["ieee"], True),
            (row["mem_cor"], row["mem_plana"], False),
        ]
        parts = []
        for i, (texto_cor, texto_plano, alinhar_dir) in enumerate(campos):
            largura = col_widths[i]
            padding = largura - len(texto_plano)
            if alinhar_dir:
                parts.append(" " * padding + texto_cor)
            else:
                parts.append(texto_cor + " " * padding)
        return " | ".join(parts)

    def fmt_header(vals):
        parts = []
        for i, val in enumerate(vals):
            if i in (2, 3):
                parts.append(val.rjust(col_widths[i]))
            else:
                parts.append(val.ljust(col_widths[i]))
        return " | ".join(parts)

    separador = "-+-".join("-" * w for w in col_widths)

    # Exibir tabela
    print(f"\n{BOLD}=== Resultados ==={RESET}\n")
    print(f" {COR_HEADER}{fmt_header(h)}{RESET}")
    print(f" {separador}")
    for row in linhas_tabela:
        print(f" {fmt_row_colorida(row)}")
    print(f" {separador}")
    print(f" Total: {len(resultados)} expressoes processadas.")