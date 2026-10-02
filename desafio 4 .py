import numpy as np
# Assentos marcados pelo site antes da abertura do check-in
reservados = np.array(["1A","1B","2F","4C","4D","6A","7E","9F","10A","10B"])
localizadores = np.array([])
#o ideal de resservados seria um dicionario carregando informaçoes de cada um dos asssentos
codigoLocalizador = {
    "NUM":{
        "10":"ECO8",
        "9":"ECO7",
        "8":"ECO6",
        "7":"ECO5",
        "6":"ECO4",
        "5":"ECO3",
        "4":"ECO2",
        "3":"ECO1",
        "2":"VIP2",
        "1":"VIP1"
    },
    "LET":{
        "A":"E1",
        "B":"E2",
        "C":"E3",
        "D":"D3",
        "E":"D2",
        "F":"D1",
    }
}
letras = {"A":0,
          "B":1,
          "C":2,
          "D":3,
          "E":4,
          "F":5,
          }

fileiras = 10

def definirAssentos(localizadores):
    controle = {}
    for i in range(fileiras):
        for j in letras:
            controle[f"{i+1}{j}"] = False
    if reservados.size > 0:
        for i in reservados:
            localizadores = np.append(localizadores, gerar_localizador(i))
            controle[i] = True
    return controle, localizadores

def atualizarAssentos(assentos, new):
    assentos[new] = True
    return assentos

def validar_localizador(userInput):
    classe = ["ECO","VIP"]
    for i in classe:
        lenght = 8
        if i == classe[1]:
            lenght = 2
        if i in userInput:
            if 1 <= int(userInput[-1]) <= 3:
                if userInput[-2] == "D" or userInput[-2] == "E":
                    if 1 <= int(userInput[3]) <= lenght:
                        return True
                    else:
                        return False
                else:
                    return False
            else:
                return False

def gerarVisual(assentos):
    controle = np.full((fileiras, 6), "", dtype=str)
    mapaNumpy = np.full((fileiras,6), 0)
    print("        A    B    C       D    E    F")
    for i,j in enumerate(assentos):
        if assentos[j] == True:
            controle[i//6][i%6] = "X"
            mapaNumpy[i//6][i%6] = 1
        else:
            controle[i//6][i%6] = "."
    for i in range(fileiras):
        if i >= 9:
            print(f"{i+1}      {controle[i][0]}    {controle[i][1]}    {controle[i][2]}       {controle[i][3]}    {controle[i][4]}    {controle[i][5]}")
        else:
            print(f"{i+1}       {controle[i][0]}    {controle[i][1]}    {controle[i][2]}       {controle[i][3]}    {controle[i][4]}    {controle[i][5]}")
    return mapaNumpy

def gerar_localizador(assento):
    length = 1
    if len(assento) == 3:
        length = 2
    if assento[-1] in letras and int(assento[:length]) <= fileiras:
        return f"{codigoLocalizador['NUM'][assento[:length]]}{codigoLocalizador['LET'][assento[-1]]}"
    
def converter_assento(codigo):
    length = 1
    if len(codigo) == 3:
        length = 2
    if codigo[-1] in letras and int(codigo[:length]) <= fileiras:
        return [int(codigo[:length])-1,letras[codigo[-1]]]
    else:
        print("Assento inválido")
        return [-1,-1]

def calcular_taxa_assento(linha, coluna):
    if coluna == 0 or coluna == 5:
        return 35
    elif coluna == 1 or coluna == 4:
        return 25

def calcular_taxa_bagagem(peso:float, premium:bool): 
    if premium:
        pesoIncluso =  32
    else:
        pesoIncluso = 23
    if peso > 45:
        print("mala pesada demais")
        peso = float(input("Realoque as malas e digite o novo peso: "))
        if peso > 45:
            print("error")

    if peso-pesoIncluso < 0:
        return 0
    else:
        return (peso-pesoIncluso)*15

def definir_grupo(linha, coluna):
    if linha == 1 or linha == 0:
        return 1
    else:
        if coluna == 0 or coluna == 5:
            return 2
        elif coluna == 1 or coluna == 4:
            return 3
        else:
            return 4

def formatar_nome_cartao(nome:str):
    nome = nome.split(" ")
    return f"{nome[-1]}/{nome[0]}"

def validar_assento(userLocalizador, userAssento):
    pass

def verifyLocalizadores(localizador):
    pass



assentos, localizadores = definirAssentos(localizadores)
mapaNumpy = gerarVisual(assentos)
localizador = input("digite seu localizador: ").upper().replace(" ", "")
codigoAssento = input("Qual o código do assento?").upper().replace(" ", "")
assentoConvertido = converter_assento(codigoAssento)
if assentoConvertido == [-1,-1]:
    assentoConvertido = converter_assento(input("Codigo de assento inválido tente novamente: ").upper().replace(" ", ""))
else:
    localizadorGerado = gerar_localizador(codigoAssento)
print(assentoConvertido)
localizador = validar_localizador(localizador)
loops = int(input("Quantos passageiros terão no voo?"))

for i in range(loops):
    nome = input("Nome completo: ").upper()
    nomeSplit = formatar_nome_cartao(nome)
    localizador = input("Localizador da reserva: ").upper().replace(" ", "")
    assento = input("Assento desejado: ").upper().replace(" ", "")

    kg_bag = input("Peso da bagagem em Kg: ").upper().replace(" ", "")