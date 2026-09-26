import numpy as np
# Assentos marcados pelo site antes da abertura do check-in
reservados = ["1A","1B","2F","4C","4D","6A","7E","9F","10A","10B"]
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

def definirAssentos():
    controle = {}
    for i in range(10):
        for j in letras:
            controle[f"{i+1}{j}"] = False
    if reservados:
        for i in reservados:
            controle[i] = True
    return controle


def validar_localizador(userInput, genInput):
    if userInput != genInput:
        response = input("Digite novamente o localizador: ").upper()
        if response == genInput:
            return response


def gerarVisual(assentos):
    length = 1
    controle = []
    print("       A  B  C    D  E  F")
    for i,j in enumerate(assentos):
        if len(j) == 3:
            length = 2
        if not controle:
            controle.append([])
        elif len(controle) <= int(j[:length])-1:
            controle.append([])
        controle[int(j[:length])-1].append(j)
        print(controle)
        if i%6 != 0:
            #falta fazer o negocio desenrolar mas as saidas ate entao estao oks
            print(f"{j[:length]}      ")
def converter_assento(codigo):
    length = 1
    if len(codigo) == 3:
        length = 2
    if codigo[-1] in letras and int(codigo[:length]) <= 10:
        return [letras[codigo[-1]],int(codigo[:length])-1] , f"{codigoLocalizador['NUM'][codigo[:length]]}{codigoLocalizador['LET'][codigo[-1]]}"
    else:
        print("Assento inválido")
        return [-1,-1], None

assentos = definirAssentos()
gerarVisual(assentos)
codigoAssento = input("Qual o código do assento?").upper()
#localizador = validar_localizador(codigoAssento)
assentoConvertido, a = converter_assento(codigoAssento)
print(assentoConvertido)
print(a)
print(assentos)

loops = int(input("Quantos passageiros terão no voo?"))

for i in range(loops):
    nome = input("Nome completo: ").upper()
    localizador = input("Localizador da reserva: ").upper()
    assento = input("Assento desejado: ").upper()
    kg_bag = input("Peso da bagagem em Kg: ").upper()
    if kg_bag.isdigit():
        if float(kg_bag) <= 45:
            pass
        else:
            kg_bag = float(input("remaneje suas bagagens e digite o novo peso em Kgs: "))
    else:
        kg_bag = float(input("Digite novamente o peso da bagagem em kg: "))
