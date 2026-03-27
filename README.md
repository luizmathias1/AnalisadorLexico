# AnalisadorLexico

## Informações acadêmicas

- **Instituição:** Pontifícia Universidade Católica do Paraná.
- **Disciplina:** Construção de Interpretadores.
- **Professor:** Frank Coelho de Alcantara.

## Integrantes do grupo

- Alexandre Faisst — GitHub: @faisstzera
- Bruno Teider — GitHub: @bruno-teider
- Luiz Mathias — GitHub: @luizmathias1
- Rafaela Vecchi — GitHub: @RafaelaVecchi

## Como executar

### Executar com um arquivo de teste

```bash
# Navegar até a pasta do projeto
cd AnalisadorLexico

# Executar com um dos arquivos de teste disponíveis
python src/main.py testes/teste_basico.txt
python src/main.py testes/teste_memoria.txt
python src/main.py testes/teste_aninhamento.txt
```

### O que acontece na execução

1. ✅ **Leitura**: Arquivo de entrada é lido linha por linha
2. ✅ **Parse**: Cada linha é tokenizada e validada
3. ✅ **Execução**: Tokens são executados em pilha (RPN)
4. ✅ **Assembly**: Código ARM é gerado
5. ✅ **Exibição**: Tabela colorida é mostrada no console
6. ✅ **Saída**: Resultados são salvos em `tokens.txt` e `assembly.txt`

## Como testar

### Usar testes inclusos

O projeto fornece 4 arquivos de teste:

```bash
# Teste básico
python src/main.py testes/teste_basico.txt

# Teste com memória
python src/main.py testes/teste_memoria.txt

# Teste com aninhamento 
python src/main.py testes/teste_aninhamento.txt

# Teste de erros 
python src/main.py testes/expressoes_erro.txt
# Esperado: mensagens de erro para expressões inválidas
```

## Descrição do projeto

AnalisadorLexico é um sistema desenvolvido para analisar, validar e avaliar expressões matemáticas em Notação Polonesa Reversa (RPN), com geração de código assembly para arquitetura ARMv7 DEC1-SOC(v16.1). O sistema implementa:

1. **Análise léxica** com validação de sintaxe e balanceamento de parênteses
2. **Execução de expressões** em pilha (stack) seguindo norma IEEE 754 (64-bit floating point)
3. **Geração de código assembly** compilável para processadores ARM com unidade de ponto flutuante (VFP)
4. **Sistema de memória** que permite armazenar e recuperar resultados em variáveis nomeadas
5. **Comando RES** para acesso a resultados de expressões anteriores
6. **Apresentação formatada** em tabela colorida com suporte a IEEE 754 binário


## Funcionalidades

### Operações matemáticas suportadas

| Operador | Descrição |
|----------|-----------|
| `+` | Adição |
| `-` | Subtração |
| `*` | Multiplicação |
| `/` | Divisão real |
| `//` | Divisão inteira |
| `%` | Módulo (resto da divisão) |
| `^` | Potenciação |

### Funcionalidades especiais

- **Variáveis de memória**: Armazena resultados com nomes customizados (Ex: `(10.0 MEM)` armazena 10.0 na variável MEM)
- **Comando RES**: Recupera resultado de expressão anterior (Ex: `(1 RES)` recupera resultado da expressão anterior; `(2 RES)` recupera de 2 expressões atrás, etc)
- **Expressões aninhadas**: Suporta parênteses aninhados (Ex: `((2.0 3.0 +) 4.0 *)`)
- **Tratamento de casos extremos**: NaN (operações indefinidas), Inf (overflow), -Inf (underflow)
- **Divisão por zero**: Retorna Inf ou -Inf conforme sinal do dividendo; 0/0 retorna NaN

### Validações implementadas

- Parênteses balanceados
- Quantidade de operandos suficientes para cada operador
- Detecção de caracteres inválidos
- Números malformados (múltiplos pontos, sinais incorretos)
- Índices de RES válidos

## Tecnologias utilizadas

### Linguagem e ambiente

- **Python** 3.6
- Biblioteca padrão apenas (sem dependências externas):
  - `json` - Armazenamento de tokens e resultados
  - `os` - Manipulação de arquivos e diretórios
  - `math` - Operações matemáticas (potência)
  - `struct` - Conversão para representação binária IEEE 754
  - `sys` - Argumentos de linha de comando

### Arquitetura alvo (para assembly gerado)

- **Processador**: ARMv7 DEC1-SOC(v16.1)
- **Coprocessador**: VFP (Vector Floating Point)
- **Padrão**: IEEE 754 (64-bit em Python; assembly gera operações em 32-bit VFP single precision para cálculos)

## Estrutura do projeto

```
AnalisadorLexico/
├── src/
│   ├── main.py                    # Ponto de entrada principal
│   ├── parseExpressao.py          # Análise léxica com máquina de estados
│   ├── executarExpressao.py       # Execução RPN em pilha com IEEE 754
│   ├── gerarAssembly.py           # Gerador de código assembly ARM v7 VFP
│   ├── exibirResultados.py        # Formatação e exibição colorida de resultados
│   ├── utils.py                   # Utilitários (leitura de arquivo, JSON, reset)
│   ├── __pycache__/               # Cache Python (gerado automaticamente)
│   └── results/                   # Saída interna
│       ├── assembly.txt           # Código assembly gerado
│       └── tokens.txt             # Tokens e resultados em JSON
├── testes/
│   ├── teste_basico.txt           # Operações simples (adição, variáveis)
│   ├── teste_memoria.txt          # Variáveis de memória e comando RES
│   ├── teste_aninhamento.txt      # Expressões com parênteses aninhados
│   └── expressoes_erro.txt        # Expressões com erros (para validação)
├── README.md                      # Documentação
```


### Validação manual

Após a execução dos testes, recomenda-se realizar uma validação manual:

1. **`tokens.txt`**: verifique se o arquivo foi gerado corretamente, no formato esperado, contendo o array `entries` com as informações correspondentes a cada expressão processada.

2. **`assembly.txt`**: confirme se o arquivo de saída foi criado corretamente e se as instruções geradas são compatíveis com a arquitetura **ARMv7**.

3. **CPUlator**: após a geração do código assembly, recomenda-se abrir o simulador **CPUlator** na configuração **ARMv7 DE1-SoC** para inspecionar a execução do programa. Durante essa etapa, observe especialmente:
   - o comportamento geral do programa no ambiente simulado;
   - os registradores utilizados ao longo da execução;
   - a interação com a interface da placa e com os leds.

**Simulador:** `https://cpulator.01xz.net/?sys=arm-de1soc&d_audio=48000`


## Formato de entrada e saída

### Formato de entrada (TXT)

Cada linha deve conter **uma expressão RPN**:

```
(operando1 operando2 ... operadorN)
```

**Regras:**
- Operandos e operadores separados por espaço
- Números podem ser inteiros ou decimais (ex: `5`, `5.0`, `3.14`)
- Variáveis são nomes em MAIÚSCULAS (ex: `MEM`, `X`, `VALOR`)
- Operadores: `+`, `-`, `*`, `/`, `//`, `%`, `^`
- Comando especial: `RES` (para resultado anterior)

**Exemplos de entrada válida:**

```
(4.0 2.0 +)                      # Resultado: 6.0
(20.0 BALANCO)                   # Armazena 20.0 em BALANCO
((BALANCO) 5.0 +)                # Soma BALANCO + 5.0
(1 RES)                          # Recupera resultado da expressão anterior
((1 RES) (2 RES) +)              # Soma de resultados de 1 e 2 expressões anteriores
```

### Formato de saída: JSON (tokens.txt)

```json
{
  "entries": [
    {
      "line_number": 1,
      "line": "(4.0 2.0 +)",
      "tokens": [
        {"token": "(", "type": "parenthesis", "position": 0},
        {"token": "4.0", "type": "number", "position": 1},
        {"token": "2.0", "type": "number", "position": 5},
        {"token": "+", "type": "operator", "position": 9},
        {"token": ")", "type": "parenthesis", "position": 10}
      ],
      "resultado": 6.0,
      "memoria": ""
    }
  ]
}
```

**Campos:**
- `line_number`: Número da linha no arquivo de entrada
- `line`: Expressão original 
- `tokens`: Array de tokens com tipo e posição
- `resultado`: Resultado da avaliação 
- `memoria`: Nome da variável que armazenou o resultado (vazio se nenhuma)

### Formato de saída: Assembly (assembly.txt)

```asm
.syntax unified
.arch armv7-a
.fpu vfp
.text
.global main
main:
    // Habilitar o VFP
    MRC p15, 0, r0, c1, c0, 2
    ORR r0, r0, #0xF00000
    MCR p15, 0, r0, c1, c0, 2
    ISB
    MOV r0, #0x40000000
    VMSR FPEXC, r0

    // Carrega 4.0
    LDR r0, =num_0
    VLDR s0, [r0]

    // Carrega 2.0
    LDR r0, =num_1
    VLDR s1, [r0]

    // -- Operação: + --
    VADD.F32 s0, s0, s1

    [... mais instruções ...]

.data
num_0: .float 4.0
num_1: .float 2.0

res_array:
    .space 8  // Espaço para resultados das expressões

const_10:
    .float 10.0
const_100:
    .float 100.0

seg7_table:
    .word 0x3F  // 0
    .word 0x06  // 1
    .word 0x5B  // 2
    .word 0x4F  // 3
    .word 0x66  // 4
    .word 0x6D  // 5
    .word 0x7D  // 6
    .word 0x07  // 7
    .word 0x7F  // 8
    .word 0x6F  // 9
```

### Formato de saída: Console (tabela colorida)

```
 Linha | Expressao   | Resultado | IEEE 754 (64-bit)                      | Memoria
 ------+-------------+-----------+----------------------------------------+--------
 1     | (4.0 2.0 +) |      6.00 | 01000000 00011000000000000000000000... | -      
 2     | (1.0 1.0 +) |      2.00 | 01000000 00000000000000000000000000... | -      
 ------+-------------+-----------+----------------------------------------+--------
 Total: 2 expressões processadas.
```

**Colunas:**
- **Linha**: Número da linha no arquivo
- **Expressao**: Texto original 
- **Resultado**: Valor calculado (formatado com 2 casas decimais)
- **IEEE 754 (64-bit)**: Representação binária do float em IEEE 754 (64 bits big-endian): primeiros 32 bits (MSB), espaço, últimos 32 bits (LSB)
- **Memoria**: Nome da variável armazenada (ou `-` se nenhuma)


## Funcionamento das Funções

### `main.py`

Este arquivo é o ponto de entrada do programa. Contém a função **main(argv=None)** que orquestra o fluxo completo.

**main(argv=None)**

Recebe argumentos de linha de comando; se não fornecidos, usa `sys.argv`. Valida se foi fornecido exatamente um argumento adicional (o nome do arquivo de entrada); caso contrário, imprime mensagem de uso e encerra com código 1. Chama `resetFiles()` do módulo `utils` para inicializar o estado. Chama `lerArquivo(arquivo)` para ler todas as linhas do arquivo de entrada. Itera sobre cada linha não-vazia e chama `parseExpressao.parseExpressao(linha, idx)` para gerar tokens, capturando exceções e imprimindo mensagens de erro por linha. Ao fim da análise, chama `executarExpressao.executarExpressao()` para processar os tokens em pilha e obter resultados. Chama `exibirResultados.exibirResultados(resultados)` para exibir uma tabela formatada no console. Chama `gerarAssembly.gerarAssembly()` para traduzir os tokens em código ARM assembly. A execução é protegida por `if __name__ == "__main__"`, garantindo que o módulo foi executado diretamente e não importado.

### `parseExpressao.py`

Este módulo implementa uma máquina de estados finita para análise léxica de expressões RPN. O módulo utiliza variáveis globais `balance` (rastreia balanceamento de parênteses) e `qnt_operandos` (conta operandos disponíveis na pilha) para controlar validações.

**parseExpressao(linha, line_number=None)**

Função principal que tokeniza uma expressão RPN recebida como string. Recebe a expressão e um número de linha opcional. Retorna uma lista de tokens (cada token é um dicionário com chaves `token`, `type` e `position`). Reseta as variáveis globais `balance` e `qnt_operandos` a cada chamada. Inicializa a máquina de estados em `estadoInicial` e itera caractere por caractere pela expressão. Adiciona um espaço fictício ao final para forçar o processamento do último token. Passa o controle entre estados conforme o tipo de caractere. Ao final, chama `estadoFinal()` para validação completa (balanceamento, expressão não-vazia) e persistência em JSON via `addJson()`. Levanta exceção `ValueError` se houver erros de sintaxe.

**estadoInicial(char, lista, tokens, linha, index)**

Estado de repouso que determina o tipo do próximo token. Ignora espaços em branco. Se encontra `(` ou `)`, delega para `estadoParenteses()`. Se encontra dígito ou ponto, inicia `estadoNumero()`. Se encontra `-`, verifica o próximo caractere: se for dígito, inicia `estadoNumero()` com o sinal; caso contrário, delega para `estadoOperador()`. Se encontra `+`, `*`, `/`, `^` ou `%`, valida se há pelo menos dois operandos (`qnt_operandos >= 2`) antes de processar, caso contrário levanta `ValueError`. Se encontra letra, inicia `estadoComando()`. Levanta `ValueError` para caracteres desconhecidos. Retorna `(próximo_estado, lista_acumuladora)`.

**estadoNumero(char, lista, tokens, linha, index)**

Acumula dígitos e ponto decimal para formar números. Enquanto recebe dígitos, continua recursivamente. Se recebe ponto, verifica se já existe ponto no acumulador (erro: múltiplos pontos); se válido, acumula. Se recebe letra, repassa para `estadoComando()` com a sequência acumulada (ex: "5X"). O `estadoComando()` então valida se contém apenas letras maiúsculas; se houver dígitos misturados, levanta `ValueError`. Se recebe caractere fora dessa categoria, salva o número como token (incrementa `qnt_operandos`), valida que o acumulador não é apenas `-` ou `.` (evita tokens malformados), e repassa o caractere atual a `estadoInicial()`. Levanta `ValueError` para números inválidos.

**estadoOperador(char, lista, tokens, linha, index)**

Processa operadores aritméticos. Caso especial: se o acumulador é `/` e o caractere é `/`, salva `//` (divisão inteira) e decrementa `qnt_operandos`. Se o acumulador só tem `/`, salva `/` (divisão real) e decrementa `qnt_operandos`. Se o acumulador está vazio e o caractere é `/`, continua recursivamente para checagem de `//`. Para outros caracteres em `+-*^%`, salva o operador, decrementa `qnt_operandos` (pois consome 2 operandos e gera 1), retorna a `estadoInicial()`.

**estadoComando(char, lista, tokens, linha, index)**

Acumula caracteres alfabéticos maiúsculos para formar comandos especiais (`RES`) ou nomes de variáveis (`MEM`, `BALANCO`, `X`, etc.). Enquanto recebe letras, continua acumulando. Quando recebe caractere não-alfabético (espaço, operador, parêntese), valida que a lista contém apenas letras maiúsculas (`lista.isalpha() and lista.isupper()`), salva como token com tipo `command`, incrementa `qnt_operandos` (comandos contam como operandos), e repassa o caractere a `estadoInicial()`. Levanta `ValueError` se o comando contém letras minúsculas ou dígitos.

**estadoParenteses(char, tokens, index)**

Processa parênteses de abertura e fechamento. Levanta `ValueError` se encontra `)` no início (nenhum token anterior). Incrementa `balance` para `(` e decrementa para `)`. Salva o parêntese como token com tipo `parenthesis`. Retorna a `estadoInicial()`. É crucial para rastrear balanceamento de parênteses.

**estadoFinal(tokens, linha, line_number=None)**

Valida a expressão completa após tokenização. Levanta `ValueError` se nenhum token foi reconhecido (expressão vazia). Verifica se `balance == 0` (parênteses mal balanceados). Se válido, chama `addJson()` para persistir os tokens em JSON no arquivo `results/tokens.txt`. Retorna a lista de tokens.

### `executarExpressao.py`

Este módulo implementa a execução de expressões RPN usando uma pilha e conformidade com a norma IEEE 754 para valores em ponto flutuante.

**calcularIEEE754(a, b, operador)**

Executa uma operação aritmética binária entre dois operandos `a` (esquerdo) e `b` (direito) e retorna o resultado conforme IEEE 754. Trata sete operadores: `+` (adição com verificação de ±inf ± ∓inf = NaN), `-` (subtração com verificação de ±inf ∓ ±inf = NaN), `*` (multiplicação com verificação de inf × 0 = NaN), `/` (divisão real: se b=0 e a=0 retorna NaN; se b=0 e a≠0 retorna ±inf conforme sinal de a; se ambos infinitos retorna NaN), `//` (divisão inteira via operador `//` do Python), `%` (módulo com verificações: b=0 retorna NaN, a=inf retorna NaN, b=inf retorna a), `^` (potência via `math.pow(a, b)`). Captura `OverflowError` e retorna infinito. Captura `ValueError` e retorna NaN. Retorna `0.0` como fallback.

**executarExpressao()**

Função principal que orquestra a execução de todas as expressões. Lê os tokens do JSON em `results/tokens.txt` via `ler_json()`. Para cada expressão, instancia uma pilha vazia. Itera pelos tokens: operadores (`+`, `-`, `*`, `/`, `//`, `%`, `^`) desempilham dois operandos, executam via `calcularIEEE754()` e empilham resultado; parênteses `(` e `)` são ignorados (marcadores de sintaxe); o comando `RES` desempilha um índice `n` e carrega o resultado da `n`-ésima expressão anterior do histórico (se inválido, carrega 0.0); números são convertidos para `float` e empilhados; strings não-numéricas (nomes de variáveis) são armazenadas em `memoria` se precedidas por um número, ou carregadas de resultados anteriores caso contrário. Ao fim de cada expressão, o topo da pilha é armazenado como resultado final. Atualiza cada entrada JSON com campos `resultado` e `memoria`. Persiste os dados em `results/tokens.txt`. Retorna a lista de objetos (tokens + resultados).

### `gerarAssembly.py`

Este módulo traduz tokens em instruções de linguagem de montagem ARMv7 com suporte a operações em ponto flutuante (VFP).

**adicionarCabecalho(instrucoes)**

Adiciona o cabeçalho padrão para código assembly ARM. Declara sintaxe unificada (`.syntax unified`), arquitetura ARMv7-A (`.arch armv7-a`) e suporte a coprocessador VFP (`.fpu vfp`). Define seção de texto (`.text`) e função global `main` (`.global main`, `main:`). Gera sequência de instruções para habilitar o VFP no processador: configura registros de controle coprocessador (MRC/MCR p15), sincroniza instrução (ISB), e ativa exceções de ponto flutuante (VMSR FPEXC). Recebe lista de strings `instrucoes` e a modifica in-place com append.

**mostrarBinario(instrucoes, reg_esq)**

Gera instruções ARM que piscam os bits do resultado armazenado em um registrador VFP no periférico de LEDs via I/O. Converte o float do registrador VFP para double (64 bits), extrai os 32 bits superiores (MSB) e 32 bits inferiores (LSB) para registradores de propósito geral (r4 e r5). Escreve cada metade separadamente no endereço I/O `0xFF200000` (periférico de LED), com pausa entre elas. Recebe o índice do registrador VFP que contém o valor a exibir.

**gerarRes(instrucoes, contador_reg, linha_idx, literais)**

Gera instruções para o comando especial `RES`. Converte o topo da pilha (registrador `s{reg_top}`) para inteiro de 32 bits (o índice da linha anterior). Calcula o índice absoluto subtraindo `n` do índice da linha atual. Se o índice é inválido (< 0), carrega o literal 0.0; caso contrário, carrega o resultado da linha anterior do array `res_array` em memória. Recebe lista de instruções, contador de registrador, índice da linha atual e lista de literais (pode ser estendida com 0.0 se necessário).

**gerarAssembly()**

Função principal que traduz os tokens JSON em código assembly compilável. Lê tokens de `results/tokens.txt` via `ler_json()`. Chama `adicionarCabecalho()` para inicializar. Itera sobre cada token: para números, cria rótulo literal (ex: `num_0`), carrega endereço em registrador geral, carrega valor float em registrador VFP sequencial (s0, s1, ..., incrementa contador); para operadores, valida que há ≥2 registradores, executa operação VFP correspondente (`VADD.F32`, `VSUB.F32`, `VMUL.F32`, `VDIV.F32`, divisão inteira com conversão, módulo float como A - int(A/B)*B, potência com loop), armazena resultado no registrador esquerdo, decrementa contador; para parênteses, não gera código; para `RES`, delega a `gerarRes()`; para outros comandos (variáveis de memória), armazena (se precedido por número) ou carrega (caso contrário). Ao fim de cada expressão, salva o resultado em `res_array` e chama `mostrarBinario()` para exibição. Finaliza com `BX LR` (retorno ARM). Gera seção `.data` com literais numéricos, variáveis de memória, array de resultados, constantes (10.0, 100.0) e tabela de 7-segmentos (`seg7_table` com padrões de 0-9). Escreve código assembly completo em `results/assembly.txt`. Retorna o caminho do arquivo.

### `exibirResultados.py`

Este módulo formata e exibe os resultados em uma tabela colorida no console com suporte a cores ANSI.

**formatarResultado(res)**

Converte um valor numérico em string formatada para exibição. Se é NaN (detectado por `res != res`, idioma IEEE 754), retorna `"NaN"`. Se é infinito positivo, retorna `"Inf"`. Se é infinito negativo, retorna `"-Inf"`. Caso contrário, formata o número com **duas casas decimais** (`f"{res:.2f}"`). Retorna a string formatada.

**formatarIEEE754(res)**

Converte um float 64-bit para sua representação binária conforme IEEE 754. Usa `struct.pack('>d', res)` para empacotar como big-endian double (8 bytes). Itera sobre cada byte, converte para 8 dígitos binários (0 ou 1), concatena todos (64 dígitos no total). Retorna uma string de 65 caracteres: 32 dígitos binários (MSB), um espaço, 32 dígitos binários (LSB).

**colorirExpressao(expressao, tokens)**

Aplica cores ANSI aos caracteres da expressão original baseada no tipo e posição dos tokens. Constrói mapa `cores_pos` que mapeia índices de caracteres para códigos ANSI. Parênteses `(` recebem cores que variam com profundidade de aninhamento (ciclo de 6 cores), `(` em negrito; `)` em negrito conforme profundidade anterior. Números recebem cor ciano. Operadores recebem cor amarela em negrito. Comandos recebem cor verde em negrito. Itera pela expressão original, consulta o mapa para cada caractere, insere códigos ANSI quando a cor muda. Retorna expressão interspersada com códigos de cor.

**exibirResultados(resultados)**

Função principal que formata e exibe uma tabela de resultados no console. Retorna imediatamente se a lista está vazia. Para cada entrada, extrai número de linha, tokens, expressão, resultado, representação IEEE 754 e variável de memória. Calcula larguras de coluna dinamicamente. Formata cabeçalho em branco em negrito. Formata linhas com expressões coloridas e valores alinhados. Desenha separadores. Exibe tabela completa com cores ANSI. Imprime resumo com total de expressões.

### `utils.py`

Este módulo fornece funções utilitárias compartilhadas.

**lerArquivo(arquivo)**

Lê um arquivo de texto e retorna uma lista de linhas. Abre o arquivo, lê todas as linhas com `readlines()`, remove quebra de linha (`\n`) de cada uma com `strip()`. Retorna lista de strings (uma por linha original).

**resetFiles()**

Inicializa ou limpa os arquivos de saída. Cria diretório `results/` se não existir. Inicializa `results/tokens.txt` com JSON vazio: `{"entries": []}`. Cria ou limpa `results/assembly.txt` (deixa vazio). Chamada no início de cada execução para garantir estado limpo.

**ler_json()**

Lê `results/tokens.txt` e retorna a lista de entradas (`data["entries"]`). Abre o arquivo, carrega JSON via `json.load()`, extrai e retorna `data["entries"]`. Usada por `executarExpressao()` e `gerarAssembly()` para acessar tokens.

**addJson(linha, tokens, line_number=None)**

Adiciona nova entrada à lista de tokens no JSON. Lê `results/tokens.txt`, extrai dicionário. Cria objeto com chaves `line_number`, `line` (expressão original) e `tokens` (lista de dicionários). Append à lista `entries`. Escreve arquivo atualizado. Usada por `parseExpressao()` após processar cada linha.

### Resumo do fluxo geral

O programa segue um fluxo linear de cinco estágios. **Estágio 1 — Entrada:** O programa recebe um arquivo contendo expressões RPN, uma por linha. **Estágio 2 — Análise léxica:** Cada linha é processada por máquina de estados que tokeniza caractere a caractere, valida sintaxe (balanceamento de parênteses, quantidade de operandos) e persiste tokens em JSON. **Estágio 3 — Execução:** Tokens são processados em pilha seguindo semântica RPN, com conformidade IEEE 754, suporte a variáveis de memória e comando RES para acesso histórico. **Estágio 4 — Geração de assembly:** Tokens são traduzidos em instruções ARMv7 com suporte a VFP, incluindo carregamento de literais, operações aritméticas, exibição em LEDs e armazenamento de resultados em array. **Estágio 5 — Saída:** Resultados são formatados em tabela colorida no console e persistidos em arquivos estruturados (JSON para tokens, assembly para código compilável).
