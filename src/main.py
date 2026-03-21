#Integrantes: 

#Alexandre Faisst 
#Bruno Teider 
#Luiz Mathias 
#Rafaela Vecchi 
 
# #Grupo RA1 1

import sys
import parseExpressao
import executarExpressao
import exibirResultados
from utils import lerArquivo, resetJson

def main(argv=None):
    argv = argv if argv is not None else sys.argv

    if len(argv) < 2:
        print("Uso: python src/main.py <nome_arquivo>")
        sys.exit(1)

    try:
        arquivo = argv[1]
        linhas = lerArquivo(arquivo)
    except Exception as e:
        print(f"\033[31m{e}\033[0m")
        sys.exit(1)

    print("\n=== Analisador Léxico ===")
    for idx, linha in enumerate(linhas, start=1):
        if not linha.strip(): continue

        try: parseExpressao.parseExpressao(linha, idx)
        except Exception as e:
            print(f"Linha {idx}: erro ao analisar: {e}")
            continue
    
    resultados = executarExpressao.executarExpressao()
    exibirResultados.exibirResultados(resultados) 

if __name__ == "__main__":
    resetJson() # Garantir que sempre começamos com um JSON vazio
    main()