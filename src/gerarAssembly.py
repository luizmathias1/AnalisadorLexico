import os
from utils import ler_json

def adicionarCabecalho(instrucoes):
    # Cabeçalho pro codigo
    instrucoes.append(".syntax unified")
    instrucoes.append(".arch armv7-a")
    instrucoes.append(".fpu vfp")
    instrucoes.append(".text")
    instrucoes.append(".global main")
    instrucoes.append("main:")
    
    # Habilitar o VFP (funcionar float)
    instrucoes.append("\n    // Habilitar o VFP")
    instrucoes.append("    MRC p15, 0, r0, c1, c0, 2")
    instrucoes.append("    ORR r0, r0, #0xF00000")
    instrucoes.append("    MCR p15, 0, r0, c1, c0, 2")
    instrucoes.append("    ISB\n")
    instrucoes.append("    MOV r0, #0x40000000")
    instrucoes.append("    VMSR FPEXC, r0")

def mostrarBinario(instrucoes, reg_esq):
    instrucoes.append(f"\n// -- Mostrar resultado em binário (pisca MSB/LSB do double) --")
    instrucoes.append(f"    VCVT.F64.F32 d1, s{reg_esq}")
    instrucoes.append(f"    VMOV r4, r5, d1")

    instrucoes.append(f"\n    // Pisca 1: upper 32 bits (MSB)")
    instrucoes.append(f"    LDR r1, =0xFF200000")
    instrucoes.append(f"    STR r5, [r1]")

    instrucoes.append(f"\n    // Apaga")
    instrucoes.append(f"    MOV r0, #0")
    instrucoes.append(f"    LDR r1, =0xFF200000")
    instrucoes.append(f"    STR r0, [r1]")

    instrucoes.append(f"\n    // Pisca 2: lower 32 bits (LSB)")
    instrucoes.append(f"    LDR r1, =0xFF200000")
    instrucoes.append(f"    STR r4, [r1]")

    instrucoes.append(f"\n    // Apaga")
    instrucoes.append(f"    MOV r0, #0")
    instrucoes.append(f"    LDR r1, =0xFF200000")
    instrucoes.append(f"    STR r0, [r1]")


def gerarRes(instrucoes, contador_reg, linha_idx, literais):
    if contador_reg >= 1:
        reg_top = contador_reg - 1
        lbl_ok = f"res_ok_{linha_idx}_{contador_reg}"
        lbl_end = f"res_end_{linha_idx}_{contador_reg}"
        instrucoes.append(f"\n// -- Comando: (N RES) --")
        instrucoes.append(f"    VCVT.S32.F32 s{reg_top}, s{reg_top}") # Transforma N em int
        instrucoes.append(f"    VMOV r1, s{reg_top}")                 # r1 = N
        instrucoes.append(f"    LDR r2, ={linha_idx}")                # r2 = índice da linha atual
        instrucoes.append(f"    SUB r1, r2, r1")                      # r1 = linha_atual - N
        instrucoes.append(f"    CMP r1, #0")                          
        instrucoes.append(f"    BGE {lbl_ok}")                        # Se índice válido >= 0
        # Caso inválido, seta para 0.0
        label_0 = f"num_{len(literais)}"
        literais.append((label_0, "0.0"))
        instrucoes.append(f"    LDR r2, ={label_0}")
        instrucoes.append(f"    VLDR s{reg_top}, [r2]")
        instrucoes.append(f"    B {lbl_end}")
        instrucoes.append(f"{lbl_ok}:")
        instrucoes.append(f"    LDR r2, =res_array")
        instrucoes.append(f"    ADD r2, r2, r1, LSL #2")              # Endereço: res_array + (idx)*4 (numero de bytes por float)
        instrucoes.append(f"    VLDR s{reg_top}, [r2]")               # Carrega o resultado anterior
        instrucoes.append(f"{lbl_end}:")

def gerarAssembly():
    data = ler_json()

    instrucoes = []
    
    adicionarCabecalho(instrucoes)

    literais = []
    memorias=[] # Para variáveis MEM, se necessário
    
    linha_idx = 0

    for linha_atual in data:
        contador_reg = 0  # Reseta o contador para cada linha/expressão (inicia em s0)
        ultimo_token_numero = False
        
        for token in linha_atual.get('tokens'):
            tipo = token['type']
            valor = str(token['token'])

            if tipo == 'number':
                # Puxamos os valores de .data
                label = f"num_{len(literais)}"
                literais.append((label, valor))
                
                instrucoes.append(f"\n    // Carrega {valor}")
                instrucoes.append(f"    LDR r0, ={label}")
                instrucoes.append(f"    VLDR s{contador_reg}, [r0]")
                contador_reg += 1
                ultimo_token_numero = True
                
            elif tipo == 'operator':
                ultimo_token_numero = False
                if contador_reg >= 2:
                    reg_dir = contador_reg - 1
                    reg_esq = contador_reg - 2
                    
                    instrucoes.append(f"\n// -- Operação: {valor} --")
                    if valor == '+':
                        instrucoes.append(f"    VADD.F32 s{reg_esq}, s{reg_esq}, s{reg_dir}")
                    elif valor == '-':
                        instrucoes.append(f"    VSUB.F32 s{reg_esq}, s{reg_esq}, s{reg_dir}")
                    elif valor == '*':
                        instrucoes.append(f"    VMUL.F32 s{reg_esq}, s{reg_esq}, s{reg_dir}")
                    elif valor == '/':
                        instrucoes.append(f"    VDIV.F32 s{reg_esq}, s{reg_esq}, s{reg_dir}")
                    elif valor == '//':
                        instrucoes.append(f"    VDIV.F32 s{reg_esq}, s{reg_esq}, s{reg_dir}")
                        instrucoes.append(f"    VCVT.S32.F32 s{reg_esq}, s{reg_esq}") # Transforma em int
                        instrucoes.append(f"    VCVT.F32.S32 s{reg_esq}, s{reg_esq}") # Volta para float
                    elif valor == '%':
                        # Modulo Float: A - (int(A / B) * B)
                        s_tmp = contador_reg
                        instrucoes.append(f"    VDIV.F32 s{s_tmp}, s{reg_esq}, s{reg_dir}")
                        instrucoes.append(f"    VCVT.S32.F32 s{s_tmp}, s{s_tmp}") # Transforma em int
                        instrucoes.append(f"    VCVT.F32.S32 s{s_tmp}, s{s_tmp}") # VOlta pra float
                        instrucoes.append(f"    VMUL.F32 s{s_tmp}, s{s_tmp}, s{reg_dir}")
                        instrucoes.append(f"    VSUB.F32 s{reg_esq}, s{reg_esq}, s{s_tmp}")
                    elif valor == '^':
                        # Potência com suporte a expoente fracionário genérico.
                        # Estratégia: separa em parte inteira e fracionária e aproxima
                        # a^frac por decomposição binária da fração com raízes sucessivas.
                        lbl = f"pow_{len(literais)}"
                        s_frac = contador_reg
                        s_one = contador_reg + 1
                        s_two = contador_reg + 2
                        label_1 = f"num_{len(literais)}"
                        literais.append((label_1, "1.0"))
                        label_2 = f"num_{len(literais)}"
                        literais.append((label_2, "2.0"))

                        # Normaliza expoente: usa valor absoluto para calcular e inverte no final se era negativo.
                        instrucoes.append(f"    MOV r3, #0")
                        instrucoes.append(f"    VMOV.F32 s{s_frac}, s{reg_dir}")
                        instrucoes.append(f"    LDR r2, ={label_1}")
                        instrucoes.append(f"    VLDR s{s_one}, [r2]")
                        instrucoes.append(f"    VCMP.F32 s{s_frac}, s{s_one}")
                        instrucoes.append(f"    VMRS APSR_nzcv, FPSCR")
                        instrucoes.append(f"    BGE {lbl}_exp_abs_done")
                        instrucoes.append(f"    MOV r3, #1")
                        instrucoes.append(f"    VNEG.F32 s{s_frac}, s{s_frac}")
                        instrucoes.append(f"{lbl}_exp_abs_done:")

                        # parte inteira
                        instrucoes.append(f"    VCVT.S32.F32 s{reg_dir}, s{s_frac}")
                        instrucoes.append(f"    VMOV r1, s{reg_dir}")
                        instrucoes.append(f"    VCVT.F32.S32 s{reg_dir}, s{reg_dir}")

                        # parte fracionária em s_frac
                        instrucoes.append(f"    VSUB.F32 s{s_frac}, s{s_frac}, s{reg_dir}")

                        # acumulador começa em 1.0 (s_dir)
                        instrucoes.append(f"    LDR r2, ={label_1}")
                        instrucoes.append(f"    VLDR s{reg_dir}, [r2]")

                        # potência inteira
                        instrucoes.append(f"{lbl}_loop:")
                        instrucoes.append(f"    CMP r1, #0")
                        instrucoes.append(f"    BLE {lbl}_end")
                        instrucoes.append(f"    VMUL.F32 s{reg_dir}, s{reg_dir}, s{reg_esq}")
                        instrucoes.append(f"    SUB r1, r1, #1")
                        instrucoes.append(f"    B {lbl}_loop")
                        instrucoes.append(f"{lbl}_end:")

                        # potência fracionária: N bits de precisão binária da fração.
                        instrucoes.append(f"    VSQRT.F32 s{reg_esq}, s{reg_esq}")
                        instrucoes.append(f"    MOV r4, #16")
                        instrucoes.append(f"    LDR r2, ={label_2}")
                        instrucoes.append(f"    VLDR s{s_two}, [r2]")
                        instrucoes.append(f"{lbl}_frac_loop:")
                        instrucoes.append(f"    CMP r4, #0")
                        instrucoes.append(f"    BLE {lbl}_frac_end")
                        instrucoes.append(f"    VMUL.F32 s{s_frac}, s{s_frac}, s{s_two}")
                        instrucoes.append(f"    VCMP.F32 s{s_frac}, s{s_one}")
                        instrucoes.append(f"    VMRS APSR_nzcv, FPSCR")
                        instrucoes.append(f"    BLT {lbl}_frac_skip_mul")
                        instrucoes.append(f"    VMUL.F32 s{reg_dir}, s{reg_dir}, s{reg_esq}")
                        instrucoes.append(f"    VSUB.F32 s{s_frac}, s{s_frac}, s{s_one}")
                        instrucoes.append(f"{lbl}_frac_skip_mul:")
                        instrucoes.append(f"    VSQRT.F32 s{reg_esq}, s{reg_esq}")
                        instrucoes.append(f"    SUB r4, r4, #1")
                        instrucoes.append(f"    B {lbl}_frac_loop")
                        instrucoes.append(f"{lbl}_frac_end:")

                        # Se expoente original era negativo: inverte resultado.
                        instrucoes.append(f"    CMP r3, #0")
                        instrucoes.append(f"    BEQ {lbl}_pow_done")
                        instrucoes.append(f"    VDIV.F32 s{reg_dir}, s{s_one}, s{reg_dir}")
                        instrucoes.append(f"{lbl}_pow_done:")
                        instrucoes.append(f"    VMOV.F32 s{reg_esq}, s{reg_dir}")    # devolve o resultado para reg_esq
                    
                    # Desempilha 1 registrador (o resultado fica em reg_esq)
                    contador_reg -= 1

            elif tipo == 'parenthesis':
                # Parênteses não geram código
                pass
                
            elif tipo == 'command':
                if valor == 'RES': 
                    gerarRes(instrucoes, contador_reg, linha_idx, literais)
                else :
                    var_label = f"{valor}_var"
                    if(f'{var_label}' not in memorias): memorias.append(var_label)
                    if ultimo_token_numero and contador_reg >= 1:
                        # Se houver um número antes, armazenamos em MEM
                        reg_top = contador_reg - 1
                        instrucoes.append(f"\n// -- Comando: Salva em ({valor}) --")
                        instrucoes.append(f"    LDR r1, ={var_label}")
                        instrucoes.append(f"    VSTR s{reg_top}, [r1]")
                    else:
                        # Caso contrário, carrega valor (se não foi inicializada, inicialmente é 0.0)
                        instrucoes.append(f"\n// -- Comando: Carrega de ({valor}) --")
                        instrucoes.append(f"    LDR r1, ={var_label}")
                        instrucoes.append(f"    VLDR s{contador_reg}, [r1]")
                        contador_reg += 1

                ultimo_token_numero = False

        # Ao final de cada linha, o resultado final na pilha fica salvo no res_array (posição s0)
        if contador_reg > 0:
            instrucoes.append(f"\n    // Salva o resultado da expressão da linha {linha_idx} no res_array")
            instrucoes.append(f"    LDR r1, =res_array")
            instrucoes.append(f"    LDR r2, ={linha_idx}")
            instrucoes.append(f"    ADD r1, r1, r2, LSL #2")
            instrucoes.append(f"    VSTR s0, [r1]")

            mostrarBinario(instrucoes, 0)
            
        linha_idx += 1

    instrucoes.append("// -- Fim da execucao --")
    instrucoes.append("    BX LR")
    
    # Adicionando os valores literais em floats num segmento .data para asswmbly ler
    instrucoes.append("\n.data")
    
    # Variável MEM inicializada com 0.0
    for mem in memorias:
        instrucoes.append(f"{mem}:")
        instrucoes.append("    .float 0.0")

    # Array de resultados das expressões
    instrucoes.append("res_array:")
    instrucoes.append(f"    .space {len(data) * 4} // Espaço para {len(data)} resultados float")

    if literais:
        for label, val in literais:
            instrucoes.append(f"{label}:")
            instrucoes.append(f"    .float {val}")
            
    
    instrucoes.append("\nconst_10:")
    instrucoes.append("    .float 10.0")
    instrucoes.append("\nconst_100:")
    instrucoes.append("    .float 100.0")

    instrucoes.append("\nseg7_table:")
    instrucoes.append("    .word 0x3F  // 0")
    instrucoes.append("    .word 0x06  // 1")
    instrucoes.append("    .word 0x5B  // 2")
    instrucoes.append("    .word 0x4F  // 3")
    instrucoes.append("    .word 0x66  // 4")
    instrucoes.append("    .word 0x6D  // 5")
    instrucoes.append("    .word 0x7D  // 6")
    instrucoes.append("    .word 0x07  // 7")
    instrucoes.append("    .word 0x7F  // 8")
    instrucoes.append("    .word 0x6F  // 9")
        
    # Escrevendo no arquivo txt
    output_path = os.path.join("results", "assembly.txt")
    with open(output_path, "w", encoding="utf-8") as f:
        f.write("\n".join(instrucoes) + "\n")
            
    return output_path