import numpy as np
# Assentos marcados pelo site antes da abertura do check-in
reservados = np.array(["1A","1B","2F","4C","4D","6A","7E","9F","10A","10B"])
localizadores = np.array([])
#numero de total linhas do aviao
fileiras = 10
#numero de linhas premium do aviao
#o codigo aceita até 99 linhas sendo possivel que todas sejam premium
fileirasPremium = 2
letras = np.array(("A","B","C","D","E","F")) #é tambem utilizado como numero de colunas
#caso o numero de letras seja alterado o codigo dara erro

#meu dicionario de assentos talvez tenha sido meio inutil
"""
EXEMPLO DE LOCALIZADORES VALIDOS
EC03D1
VP01E2
ec03d1
 EC 0 3  D1 
EXEMPLO DE LOCALIZADORES RECUSADOS
EC03D12
EC03DE2
EC01E1 => por ter o assento ja reservado caso retire o reservado ele passa
EC03@1
"""


mapa_assentos_numpy = np.zeros((fileiras,6), dtype=int)

def gerarBaseLocalizador(linhas:int, colunas:list, linhasPremium:int):
    baseColunas = np.array(["EC","VP"])
    baseLinhas = np.array(["E","D"])
    
    codigoLocalizador = {"NUM":{},"LET":{}}
    controle = 0
    for i in range(linhas):
        if linhasPremium:
            if i <= linhasPremium-1:
                controle = 1
            else:
                controle = 0
        codigoLocalizador["NUM"].setdefault(str(i+1),f"{baseColunas[controle]}{str(i+1).zfill(2)}")
    for i,j in enumerate(colunas):
        if i < len(colunas)/2:
            controle = baseLinhas[0]
            formulaControle = i%3+1
        else:
            controle = baseLinhas[1]
            formulaControle = 4 - (i%3+1)
        codigoLocalizador["LET"].setdefault(j.tolist(),f"{controle}{formulaControle}")
    return codigoLocalizador

def definirAssentos(localizadores):
    controle = {}
    for i in range(fileiras):
        for j in letras:
            controle[f"{i+1}{j}"] = False
    if reservados.size > 0:
        for i in reservados:
            localizador = gerar_localizador(i)
            assento = converter_assento(i)
            mapa_assentos_numpy[tuple(assento)] = True
            localizadores = np.append(localizadores, localizador)
            controle[i] = True
    return controle, localizadores

def atualizarAssentos(assentos, new, localizadores):
    #função para atualizar os assentos ocupados
    #tanto o dict quanto o array numpy
    #além de atualizar o localizadores ocupados
    assentos[new] = True
    mapa_assentos_numpy[tuple(converter_assento(new))] = True
    localizadores = np.append(localizadores, gerar_localizador(new))
    return assentos, localizadores

def validar_localizador(userInput):
    classe = ["EC","VP"]
    for i in classe:
        lenght = fileiras
        if i == classe[1]:
            lenght = fileirasPremium
        if i in userInput:
            try:
                teste = int(userInput[2:4])
                teste = int(userInput[-1])
            except ValueError:
                return False
            if 1 <= int(userInput[2:4]) <= lenght:
                if 1 <= int(userInput[-1]) <= 3:
                    if userInput[-2] == "D" or userInput[-2] == "E":
                        return True
    return False                    

def gerarVisual(assentos):
    #função para gerar mapa de assentos do avião
    controle = np.full((fileiras, 6), "", dtype=str)
    print("        A    B    C       D    E    F")
    for i,j in enumerate(assentos):
        if assentos[j] == True:
            controle[i//6][i%6] = "X"
        else:
            controle[i//6][i%6] = "."
    for i in range(fileiras):
        if i <= fileirasPremium - 1:
            print(f"{i+1}       {controle[i][0]}    {controle[i][1]}    {controle[i][2]}       {controle[i][3]}    {controle[i][4]}    {controle[i][5]}   Premium")
        else:
            if i >= 9:
                print(f"{i+1}      {controle[i][0]}    {controle[i][1]}    {controle[i][2]}       {controle[i][3]}    {controle[i][4]}    {controle[i][5]}   Econômica")
            else:
                print(f"{i+1}       {controle[i][0]}    {controle[i][1]}    {controle[i][2]}       {controle[i][3]}    {controle[i][4]}    {controle[i][5]}   Econômica")

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
        return [int(codigo[:length])-1, np.where(letras == codigo[-1])[0][0].tolist()]
    else:
        return [-1,-1]

def calcular_taxa_assento(linha, coluna):
    if linha <= fileirasPremium-1:
        return 0
    if coluna == 0 or coluna == 5:
        return 35
    elif coluna == 1 or coluna == 4:
        return 0
    else:
        return 25

def calcular_taxa_bagagem(peso:float, premium:bool): 
    if premium:
        pesoIncluso =  32
    else:
        pesoIncluso = 23
    if peso-pesoIncluso <= 0:
        return 0
    elif peso <= 45:
        return (peso-pesoIncluso)*15
    else:
        return ""

def definir_grupo(linha, coluna):
    if linha <= fileirasPremium-1:
        return 1
    else:
        if coluna == 0 or coluna == 5:
            return 2
        elif coluna == 1 or coluna == 4:
            return 3
        else:
            return 4

def formatar_nome_cartao(nome:str):
    nome = nome.strip()
    nome = nome.split()
    prenome = ""
    for i in nome:
        if i != nome[-1]:
            if i == nome[0]:
                prenome += f"{i}"
            else:
                prenome += f" {i}"
    return f"{nome[-1]}/{prenome}"

def verifyLocalizadores(localizador):
    #verifica se o localizador enviado ja foi utilizado
    if localizador not in localizadores:
        return True
    else:
        return False

def tipo_assento(localizador):
    if localizador[-1] == "1":
        return "Janela"
    elif localizador[-1] == "2":
        return "Meio"
    else:
        return "Corredor"
    
def verificar_janelas(assentos):
    janelas = []
    for i in assentos:
        if i[-1] == "A" or i[-1] == "F":
            if not assentos[i]:
                janelas.append(i)
    janelas = np.array(janelas)
    return janelas
            
#gera a base para os localizadores com limitação a 99 linha podendo ser as 99 premium
codigoLocalizador = gerarBaseLocalizador(fileiras, letras, fileirasPremium)
#pega um dict com todos os asentos e se o assento esta ocupado ou não
#e um array com todos os localizadores utilizado até então
assentos, localizadores = definirAssentos(localizadores)
gerarVisual(assentos)
loops = int(input("Quantos passageiros terão no voo?"))
#loop pela quantidade de passageiros

#variaveis para controle dos passageiros
nomes = np.array([])
localizadorUsuario = np.array([])
pesoBagagem = np.array([], dtype=float)
tarifaBagagem = np.array([])
assentoDesejado = np.array([])
grupoEmbarque = np.array([], dtype=int) #em ordem de chegada de cada passageiro
taxaAssento = np.array([], dtype=int) 
ordemEmbarque = [[],[],[],[]]
for i in range(loops):
    #recebe o nome e formata ele
    nome = input("Nome completo: ").upper()
    
    #pega informaçoes localizador, asento e peso da bagagem
    localizador = input("Localizador da reserva: ").upper().replace(" ", "")
    assento = input("Assento desejado: ").upper().replace(" ", "")
    kg_bag = input("Peso da bagagem em Kg: ").upper().replace(" ", "")
    
    #loop que roda até todas informaçoes serem validas
    valido = False
    while not valido:
        localizadorValidado = validar_localizador(localizador)
        assentoConvertido = converter_assento(assento)
        if assentoConvertido == [-1,-1]:
            assento = input("Codigo de assento inválido tente novamente: ").upper().replace(" ", "")
        else:
            if len(nome.split(" ")) > 1:
                if not mapa_assentos_numpy[tuple(assentoConvertido)]:
                    if localizadorValidado:
                        localizadorGerado = gerar_localizador(assento)
                        if localizadorGerado == localizador:  
                            try:
                                if assentoConvertido[0] <= fileirasPremium-1:
                                    premium = True
                                else:
                                    premium = False
                                taxa_bagagem = calcular_taxa_bagagem(float(kg_bag), premium)
                                if taxa_bagagem == "":
                                    kg_bag = input("Você excedeu o peso reditribua sua bagagem e digite novamente: ").upper().replace(" ", "")
                            except ValueError:
                                kg_bag = input("Redigite o peso da sua bagagem: ").upper().replace(" ", "")
                            if taxa_bagagem != "":
                                assentos, localizadores = atualizarAssentos(assentos, assento, localizadores)
                                nomes = np.append(nomes, formatar_nome_cartao(nome))
                                localizadorUsuario = np.append(localizadorUsuario, localizador)
                                assentoDesejado = np.append(assentoDesejado, assento)
                                grupo = definir_grupo(assentoConvertido[0],assentoConvertido[1])
                                ordemEmbarque[grupo-1].append(localizador)
                                grupoEmbarque = np.append(grupoEmbarque, grupo)
                                taxaAssento = np.append(taxaAssento, calcular_taxa_assento(assentoConvertido[0], assentoConvertido[1]))
                                pesoBagagem = np.append(pesoBagagem, kg_bag)
                                tarifaBagagem = np.append(tarifaBagagem, taxa_bagagem)
                                
                                valido = True
                        else:
                            localizador = input("Seu localizador não está de acordo com seu assento redigite seu localizador: ").upper().replace(" ", "")
                    else:
                        localizador = input("Seu localizador está errado redigite ele: ").upper().replace(" ", "")
                else:
                    assento = input("Este assento já foi ocupado escolha outro: ").upper().replace(" ", "")
            else:
                nome = input("Digite o nome completo: ").upper()

    total = float(tarifaBagagem[i])+float(taxaAssento[i])
    print()
    print("=" * 50)
    print("AEROVALE | VOO AV2026 | VCP - REC")
    print("-" * 50)
    print(f"Passageiro: {nomes[i]}")
    print(
        f"Localizador: {localizadorUsuario[i]}   Assento: {assentoDesejado[i]} ({tipo_assento(localizadorUsuario[i])})")
    print(f"Grupo de embarque: {grupoEmbarque[i]}")
    print(f"Taxa de assento: R$ {float(taxaAssento[i]):.2f}")
    print(
        f"Bagagem: {float(pesoBagagem[i]):.1f} kg "
        f"Excesso: R$ {float(tarifaBagagem[i]):.2f}"
    )
    print(f"Total a pagar no balcão: R$ {total:.2f}")
    print("=" * 50)
    print()

print("=" * 50)
print("MAPA DO AVIÃO")
gerarVisual(assentos)
print("=" * 50)

ocupacaoLinhas = []
for i in mapa_assentos_numpy:
    ocupacaoLinhas.append(np.sum(i))
ocupacaoLinhas = np.array(ocupacaoLinhas)
maximoLinhas = np.max(ocupacaoLinhas)
minimoLinhas = np.min(ocupacaoLinhas)
ocupacaoVIP = 0
ocupacaoECO = 0
for i in range(fileiras):
    if i <= fileirasPremium-1:
        ocupacaoVIP += ocupacaoLinhas[i]
    else:
        ocupacaoECO += ocupacaoLinhas[i]
ocupacaoECO = np.array(ocupacaoECO)
ocupacaoVIP = np.array(ocupacaoVIP)
print()
print("="*50)
linhasPrint = []
string = ""
linhasMinimo = np.where(ocupacaoLinhas == maximoLinhas)
print("LINHA MAIS OCUPADA")
string = (linhasMinimo[0][0]+1).tolist()
print(f"LINHA {string}")
print(f"PERCENTUAL DE OCUPAÇÃO: {(maximoLinhas/(len(letras))*100):.2f}")
print(f"OCUPAÇÃO: {maximoLinhas}/{len(letras)}")
print("="*50)
print()
print("="*50)
print("OCUPAÇÃO TOTAL")
print(f"PERCENTUAL DE OCUPAÇÃO TOTAL: {((np.sum(mapa_assentos_numpy)/(fileiras*len(letras)))*100):.2f}")
print(f"OCUPAÇÃO TOTAL: {np.sum(mapa_assentos_numpy)}/{fileiras*len(letras)}")
print("="*50)
print("OCUPAÇÃO PREMIUM")
print(f"PERCENTUAL DE OCUPAÇÃO TOTAL DA CLASSE PREMIUM: {((ocupacaoVIP)/(fileirasPremium*len(letras))*100):.2f}")
print(f"OCUPAÇÃO TOTAL PREMIUM: {ocupacaoVIP}/{fileirasPremium*len(letras)}")
print("="*50)
print("OCUPAÇÃO ECONÔMICA")
print(f"PERCENTUAL DE OCUPAÇÃO TOTAL DA CLASSE ECONÔMICA: {((ocupacaoECO)/((fileiras-fileirasPremium)*len(letras))*100):.2f}")
print(f"OCUPAÇÃO TOTAL ECONÔMICA: {ocupacaoECO}/{(fileiras-fileirasPremium)*len(letras)}")
print("="*50)
print()

print("="*50)
print("JANELAS DISPONIVEIS")
print(f"JANELAS AINDA LIVRES: {verificar_janelas(assentos).tolist()}")
print("="*50)
print()

print("="*50)
print("TOTAL ARRECADADO SEM RESERVAS NA INTERNET")
print(f"TOTAL DE TAXAS DE ASSENTO: {np.sum(taxaAssento)}")
print(f"TOTAL DE TAXAS DE BAGAGEM: {np.sum(tarifaBagagem.astype(float))}")
print(f"TOTAL: {np.sum(taxaAssento)+np.sum(tarifaBagagem)}")
print("="*50)
taxaReservados = []
for i in reservados:
    convertido = converter_assento(i)
    taxaReservados.append(calcular_taxa_assento(convertido[0],convertido[1]))
taxaReservados = np.array(taxaReservados)
print("TOTAL ARRECADADO EM RESERVAS NA INTERNET")
print(f"TOTAL DE TAXAS DE ASSENTO: {np.sum(taxaReservados)}")
print(f"TOTAL DE TAXAS DE BAGAGEM: ?")
print(f"TOTAL: {np.sum(taxaReservados)}")
print("="*50)
print("TOTAL ARRECADADO")
print(f"TOTAL DE TAXAS DE ASSENTO: {np.sum(taxaReservados)+np.sum(taxaAssento)}")
print(f"TOTAL DE TAXAS DE BAGAGEM: {np.sum(tarifaBagagem.astype(float))}")
print(f"TOTAL: {np.sum(taxaAssento)+np.sum(tarifaBagagem.astype(float))+np.sum(taxaReservados)}")
print("="*50)
print()

print("="*50)
print("PESO TOTAL DESPACHADO")
print(f"PESO TOTAL: {np.sum(pesoBagagem.astype(float))}")
maisPesada = np.max(pesoBagagem.astype(float))
indexMaisPesada = np.where(pesoBagagem.astype(float) == maisPesada.astype(float))
print("="*50)
if len(indexMaisPesada[0]) > 1:
    print("EMPATE ENTRE AS BAGAGENS MAIS PESADAS")
    print(f"PESO DAS BAGAGENS MAIS PESADAS: {maisPesada}")
    print(f"PESSOAS COM BAGAGENS MAIS PESADAS:")
    for i in indexMaisPesada[0]:
        print(f"{nomes[i]}")
else:
    print("BAGAGEM MAIS PESADA")
    print(f"PESO DA BAGAGEM MAIS PESADA: {maisPesada}")
    print(f"PESSOA COM A BAGAGEM MAIS PESADA: {nomes[indexMaisPesada[0][0]]}")
print("="*50)
print()
print("="*50)
print("ORDEM DE EMBARQUE")
print(f"GRUPO 1: {len(ordemEmbarque[0])} PASSAGEIRO(S)")
print(f"LOCALIZADORES: {ordemEmbarque[0]}")
print(f"GRUPO 2: {len(ordemEmbarque[1])} PASSAGEIRO(S)")
print(f"LOCALIZADORES: {ordemEmbarque[1]}")
print(f"GRUPO 3: {len(ordemEmbarque[2])} PASSAGEIRO(S)")
print(f"LOCALIZADORES: {ordemEmbarque[2]}")
print(f"GRUPO 4: {len(ordemEmbarque[3])} PASSAGEIRO(S)")
print(f"LOCALIZADORES: {ordemEmbarque[3]}")
print("="*50)
print()

print("="*50)
print("STATUS DO VOO")
if (np.sum(mapa_assentos_numpy)/(fileiras*len(letras)))*100 >= 90:
    print(f"QUASE LOTADO")
elif (np.sum(mapa_assentos_numpy)/(fileiras*len(letras)))*100 < 60:
    print("BAIXA OCUPAÇÃO")
else: 
    print("OCUPAÇÃO NORMAL")
print("="*50)


"""1. Família junta

Para acomodar uma família de três pessoas na mesma fileira e do mesmo lado do corredor, 
seria necessário verificar o mapa de assentos procurando três posições consecutivas livres. 
Como os lados do corredor são A-B-C e D-E-F, o programa deveria percorrer cada fileira e verificar separadamente esses dois conjuntos de assentos.

A primeira combinação encontrada em que os três assentos estejam livres seria escolhida para a família. 
A busca começaria pela primeira fileira e seguiria em ordem crescente, garantindo que a primeira possibilidade disponível fosse utilizada. 
Caso nenhuma fileira possua três assentos livres do mesmo lado, o sistema poderia informar que não é possível acomodar os três passageiros juntos."""

"""
2. Overbooking
No caso de overbooking, em que foram vendidos 64 bilhetes para uma aeronave com 60 assentos, 
seria necessário criar uma lista de espera para os passageiros que não conseguiram um assento.

Os passageiros seriam adicionados à lista conforme fossem chegando, 
mantendo a ordem de chegada. Dessa forma, o primeiro passageiro a entrar na lista seria o primeiro a ser atendido
caso algum passageiro com assento reservado não comparecesse ao embarque.

Quando um assento fosse liberado por uma ausência, 
o primeiro passageiro da lista de espera receberia esse assento e seria removido da lista. 
Esse processo continuaria seguindo a ordem de chegada até que não houvesse mais assentos disponíveis ou passageiros na lista de espera."""

#O desafio 3 foi completamente implementado no codgigo contando com a alteração das variaveis
#fileiras
#fileirasPremium
