import numpy as np
# Assentos marcados pelo site antes da abertura do check-in
reservados = ["1A","1B", "2F", "4C", "4D", "6A", "7E", "9F", "10A", "10B"]
codigoLocalizador = {
    "NUM":{
        "10":"DEZ",
        "9":"NOV",
        "8":"OIT",
        "7":"SET",
        "6":"SEI",
        "5":"CIN",
        "4":"QUA",
        "3":"TRE",
        "2":"DOI",
        "1":"UMM"
    },
    "LET":{
        "A":"121",
        "B":"122",
        "C":"123",
        "D":"221",
        "E":"222",
        "F":"223",
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
    controle = []
    for i in range(10):
        controle.append([])
        for j in letras:
            controle[i].append(f"{i+1}{j}")
    return controle


def validar_localizador(localizador):
    #if localizador in 
    print(localizador)

def converter_assento(codigo):
    length = 1
    if len(codigo) == 3:
        length = 2
    if codigo[-1].upper() in letras and int(codigo[:length]) <= 10:
        return [letras[codigo[-1]],int(codigo[:length])-1] , f"{codigoLocalizador['NUM'][codigo[:length]]}{codigoLocalizador['LET'][codigo[-1]]}"
    else:
        print("Assento inválido")
        return [-1,-1]

assentos = definirAssentos()
codigoAssento = input("Qual o código do assento?")
localizador = validar_localizador(codigoAssento)
assentoConvertido, a = converter_assento(codigoAssento)
print(assentoConvertido)
print(a)
print(assentos)

loops = int(input("Quantos passageiros terão no voo?"))