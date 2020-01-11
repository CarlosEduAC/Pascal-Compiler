# -*- coding: utf-8 -*-
#Importa a biblioteca usada para tratar possíveis erros
import Error
#Importa a biblioteca usada para realizar a análise léxica
import SemanticAnalyzer as SA

# Função que realiza a Análise Sintática
def SyntacticAnalyzer (tokens):
    global tipo
    global escopo
    global flagparametro
    global numParametro
    global classificadores
    global tipos
    global listaMesmoTipo
    listaMesmoTipo = []
    tipo = ''
    tipos = ''
    escopo = 'global'
    flagparametro = False
    numParametro = 0
    classificadores = []
    SemanticTable = Programa(tokens, 0, First())
    return SemanticTable

#Função que cria o conjunto de elementos terminais
def First ():
    first = {'Declaracoes':['const','type','var','function'],
    'Constante':['Identificador'],
    'Exp_Matematica': ['Identificador','Número'],
    'Tipo':['Identificador'],
    'Variavel':['Identificador'],
    'Tipo_Dado':['integer','real','array','record','Identificador'],
    'Funcao':['function'],
    'Bloco':['begin'],
    'Def_Variaveis':['var'],
    'Comando':['while','if','write','read','Identificador'],
    'Op_Matematico':['Operador Matemático'],
    'Op_Logico':['Operador Relacional'],
    'Nome':['Identificador'],
    'Lista_Parametro':['Identificador','Número'],
    'Nome_Numero':['Identificador','Número']}
    return first

# Função que
def Programa (tokens, i, first):
    SemanticTable = []
    if (tokens[i][0] == 'program'):
        i += 1
    else:
        Error.SyntaticError (tokens[i])
    i = Identificador (tokens, i, first, SemanticTable)
    if (tokens[i][0] == 'PontoEVirgula'):
        i += 1
    else:
        Error.SyntaticError (tokens[i])
    Corpo (tokens, i, first, SemanticTable)
    return SemanticTable

# Função que
def Corpo (tokens, i, first, SemanticTable):
    if (tokens[i][0] in first['Declaracoes']):
        i = Declaracoes (tokens, i, first, SemanticTable)
    if (tokens[i][0] == 'begin'):
        i += 1
    else:
        Error.SyntaticError (tokens[i])
    i = Comandos (tokens, i, first, SemanticTable)
    if (tokens[i][0] == 'end'):
        i += 1
    else:
        Error.SyntaticError (tokens[i])

    return i

# Função que
def Declaracoes (tokens, i, first, SemanticTable):
    i = Def_Constantes (tokens, i, first, SemanticTable)
    i = Def_Tipos (tokens, i, first, SemanticTable)
    i = Def_Variaveis (tokens, i, first, SemanticTable)
    i = Funcoes (tokens, i, first, SemanticTable)
    return i

# Função que
def Def_Constantes (tokens, i, first, SemanticTable):
    if (tokens[i][0] == 'const'):
        i += 1
        i = Constantes (tokens, i, first, SemanticTable)
    return i

# Função que
def Def_Tipos (tokens, i, first, SemanticTable):
    if (tokens[i][0] == 'type'):
        i += 1
        i = Tipos (tokens, i, first, SemanticTable)
    return i

# Função que
def Def_Variaveis (tokens, i, first, SemanticTable):
    if (tokens[i][0] == 'var'):
        i += 1
        i = Variaveis (tokens, i, first, SemanticTable)
    return i

# Função que
def Constantes (tokens, i, first, SemanticTable):
    if (tokens[i][0] in first['Constante']):
        while (tokens[i][0] in first['Constante']):
            i = Constante (tokens, i, first, SemanticTable)
    else:
        Error.SyntaticError (tokens[i])
    return i

# Função que
def Constante (tokens, i, first, SemanticTable):
    classificador = tokens[i][1]
    linha = tokens[i][2]
    i = Identificador (tokens, i, first, SemanticTable)
    if (tokens[i][1] == '='):
        i += 1
    else:
        Error.SyntaticError (tokens[i])
    i = Const_Valor (tokens,i,first,SemanticTable)
    if (tokens[i-1][0] == 'Número'):
        if (tokens[i-1][0].isdecimal()):
            SemanticTable.append([classificador,linha,escopo,'inteiro','const'])
        else:
            SemanticTable.append([classificador,linha,escopo,'real','const'])
    else:
        SemanticTable.append([classificador,linha,escopo,tokens[i-1][0],'const'])
    if (tokens[i][0] == 'PontoEVirgula'):
        i += 1
    else:
        Error.SyntaticError (tokens[i])
    return i

# Função que
def Const_Valor (tokens, i, first, SemanticTable):
    if (tokens[i][0] in first['Exp_Matematica']):
        i = Exp_Matematica (tokens, i, first, SemanticTable)
    elif (tokens[i][0] == 'Sequência'):
            i += 1
    else:
        Error.SyntaticError (tokens[i])
    return i

# Função que
def Numero (tokens, i, first, SemanticTable):
    if (tokens[i][0] == 'Número'):
        i += 1
    else:
        Error.SyntaticError (tokens[i])
    return i

# Função que
def Tipos (tokens, i, first, SemanticTable):
    if (tokens[i][0] in first['Tipo']):
        while (tokens[i][0] in first['Tipo']):
            i = Tipo (tokens, i, first, SemanticTable)
    else:
        Error.SyntaticError (tokens[i])
    return i 

# Função que
def Tipo (tokens, i, first, SemanticTable): 
    classificador = tokens[i][1]
    linha = tokens[i][2]
    global tipo
    global tipos
    i = Identificador (tokens, i, first, SemanticTable)
    if (tokens[i][1] == '='):
        i += 1
    else:
        Error.SyntaticError (tokens[i])
    i = Tipo_Dado (tokens, i, first, SemanticTable)
    SemanticTable.append([classificador,linha,escopo,tipo,tipos])
    tipos = ''
    if (tokens[i][0] == 'PontoEVirgula'):
        i += 1
    else:
        Error.SyntaticError (tokens[i])
    return i

# Função que
def Variaveis (tokens, i, first, SemanticTable):
    if (tokens[i][0] in first['Variavel']):
        while (tokens[i][0] in first['Variavel']):
            i = Variavel (tokens, i, first, SemanticTable)
            if (tokens[i][0] == 'PontoEVirgula'):
                i += 1
            else:
                Error.SyntaticError (tokens[i])
    return i

# Função que
def Variavel (tokens, i, first, SemanticTable):
    classificador = tokens[i][1]
    linha = tokens[i][2]
    global classificadores
    classificadores = []
    i = Lista_Id (tokens, i, first, SemanticTable)
    if (tokens[i][0] == 'DoisPontos'):
        i += 1
    else:
        Error.SyntaticError (tokens[i])
    i = Tipo_Dado (tokens, i, first, SemanticTable)
    global flagparametro
    if (flagparametro):
        global tipo
        global numParametro
        global tipos
        numParametro += 1
        SemanticTable.append([classificador,linha,escopo,tipo,'parâmetro',numParametro])
    else:
        if (len(classificadores) > 1):
            j = 0
            while (j < len(classificadores)):
                if (tipos == 'record'):
                    SemanticTable.append([classificadores[j][1],linha,escopo,tipo,'field'])
                else:
                    SemanticTable.append([classificadores[j][1],linha,escopo,tipo,'var'])
                j += 1
        else: 
            SemanticTable.append([classificador,linha,escopo,tipo,'var'])
    return i

# Função que
def Lista_Id (tokens, i, first, SemanticTable):
    global classificadores
    classificadores.append(tokens[i])
    i = Identificador (tokens, i, first, SemanticTable)
    if (tokens[i][0] == 'Virgula'):
        i += 1
        i = Lista_Id (tokens, i, first, SemanticTable)
    return i
    
# Função que
def Tipo_Dado (tokens, i, first, SemanticTable):
    if (tokens[i][0] in first['Tipo_Dado']):
        global tipo
        global tipos
        if (tokens[i][0] == 'integer' or tokens[i][0] == 'real'):
            tipo = tokens[i][0]
            i += 1
        elif (tokens[i][0] == 'array'):
            tipos = 'array'
            i += 1
            if (tokens[i][0] == 'Abrecolchete'):
                i += 1
            else:
                Error.SyntaticError (tokens[i])
            i = Numero (tokens, i, first, SemanticTable)
            if (tokens[i][0] == 'Fechacolchete'):
                i += 1
            else:
                Error.SyntaticError (tokens[i])
            if (tokens[i][0] == 'of'):
                i += 1
            else:
                Error.SyntaticError (tokens[i])
            tipo = tokens[i][0]
            i = Tipo_Dado (tokens, i, first, SemanticTable)
        elif (tokens[i][0] == 'record'):
            tipos = 'record'
            i += 1
            i = Variaveis (tokens, i, first, SemanticTable)
            if (tokens[i][0] == 'end'):
                i += 1
            else:
                Error.SyntaticError (tokens[i])
        elif (tokens[i][0] == 'Identificador'):
            tipo = tokens[i][1]
            i = Identificador (tokens, i, first, SemanticTable)
        return i
    else:
        Error.SyntaticError (tokens[i])

# Função que
def Funcoes (tokens, i, first, SemanticTable):
    if (tokens[i][0] in first['Funcao']):
        i = Funcao (tokens, i, first, SemanticTable)
        global escopo
        escopo = 'global'
        i = Funcoes (tokens, i, first, SemanticTable)
    return i

# Função que
def Funcao (tokens, i, first, SemanticTable):
    i = Nome_Funcao (tokens, i, first, SemanticTable)
    i = Bloco_Funcao (tokens, i, first, SemanticTable)
    return i

# Função que
def Nome_Funcao (tokens, i, first, SemanticTable):
    linha = tokens[i][2]
    if (tokens[i][0] == 'function'):
        i += 1
    else:
        Error.SyntaticError (tokens[i])
    global escopo
    escopo = tokens[i][1]
    classificador = tokens[i][1]
    i = Identificador (tokens, i, first, SemanticTable)
    if (tokens[i][0] == 'Abreparêntese'):
        i += 1
    else:
        Error.SyntaticError (tokens[i])
    global flagparametro
    global numParametro
    flagparametro = True
    numParametro = 0
    i = Variaveis (tokens, i, first, SemanticTable)
    flagparametro = False
    if (tokens[i][0] == 'Fechaparêntese'):
        i += 1
    else:
        Error.SyntaticError (tokens[i])
    if (tokens[i][0] == 'DoisPontos'):
        i += 1
    else:
        Error.SyntaticError (tokens[i])
    i = Tipo_Dado (tokens, i, first, SemanticTable)
    SemanticTable.append([classificador,linha,'global',tipo,'function',numParametro])
    return i

# Função que
def Bloco_Funcao (tokens, i, first, SemanticTable):
    if (tokens[i][0] in first['Bloco']):
        i = Bloco (tokens, i, first, SemanticTable)
    elif (tokens[i][0] in first['Def_Variaveis']):
        i = Def_Variaveis (tokens, i, first, SemanticTable)
        i = Bloco (tokens, i, first, SemanticTable)
    else:
        Error.SyntaticError (tokens[i])
    return i

# Função que
def Bloco (tokens, i, first, SemanticTable):
    if (tokens[i][0] in first['Bloco']):
        if (tokens[i][0] == 'begin'):
            i += 1
        else:
            Error.SyntaticError (tokens[i])
        i = Comandos (tokens, i, first, SemanticTable)
        if (tokens[i][0] == 'end'):
            i = Comandos (tokens, i, first, SemanticTable)
            i += 1
        else:
            Error.SyntaticError (tokens[i])
    elif (tokens[i][0] in first['Comando']):
        i = Comando (tokens, i, first, SemanticTable)
    else:
        Error.SyntaticError (tokens[i])
    return i

# Função que
def Comandos (tokens, i, first, SemanticTable):
    if (tokens[i][0] in first['Comando']):
        i = Comando (tokens, i, first, SemanticTable)
        if (tokens[i][0] == 'PontoEVirgula'):
            i += 1
        elif (tokens[i][0] != 'end'):
            Error.SyntaticError (tokens[i])
        i = Comandos (tokens, i, first, SemanticTable)
    return i

#Função que 
def Comando (tokens, i, first, SemanticTable):
    global listaMesmoTipo
    global escopo
    if (tokens[i][0] in first['Nome']):
        tokenEsq = tokens[i]
        i = Nome (tokens, i, first, SemanticTable)
        if (tokens[i][0] == 'Atribuição'):
            i += 1
        else:
            Error.SyntaticError (tokens[i])
        tokenDir = tokens[i]
        i = Valor (tokens, i, first, SemanticTable)
        SA.CheckType (SemanticTable, [tokenEsq,tokenDir], escopo)
    elif (tokens[i][0] == 'while'):
        listaMesmoTipo = []
        i += 1
        i = Expressao_Logica (tokens, i, first, SemanticTable)
        SA.CheckType (SemanticTable, listaMesmoTipo, escopo)
        i = Bloco (tokens, i, first, SemanticTable)
    elif (tokens[i][0] == 'if'):
        listaMesmoTipo = []
        i += 1
        i = Expressao_Logica (tokens, i, first, SemanticTable)
        SA.CheckType (SemanticTable, listaMesmoTipo, escopo)
        if (tokens[i][0] == 'then'):
            i += 1
        else:
            Error.SyntaticError (tokens[i])
        i = Bloco (tokens, i, first, SemanticTable)
        i = Else (tokens, i, first, SemanticTable)
    elif (tokens[i][0] == 'write'):
        i += 1
        i = Const_Valor (tokens, i, first, SemanticTable)
    elif (tokens[i][0] == 'read'):
        i += 1
        i = Nome (tokens, i, first, SemanticTable)
    else:
        Error.SyntaticError (tokens[i])
    return i

#Função que 
def Else (tokens, i, first, SemanticTable):
    if (tokens[i][0] == 'else'):
        i += 1 
        i = Bloco (tokens, i, first, SemanticTable)
    return i

#Função que 
def Valor (tokens, i, first, SemanticTable):
    if (tokens[i][0] == 'Identificador' and tokens[i+1][0] == 'Abreparêntese'):
        SA.CheckFunction (SemanticTable, tokens[i])
        i = Identificador (tokens, i, first, SemanticTable)
        i = Parametros (tokens, i, first, SemanticTable)
    else:
        i = Exp_Matematica (tokens, i, first, SemanticTable)
    return i

#Função que 
def Parametros (tokens, i, first, SemanticTable):
    global listaParam
    listaParam = []
    token = tokens[i-1]
    if (tokens[i][0] == 'Abreparêntese'):
        i += 1
    else:
        Error.SyntaticError (tokens[i])
    i = Parametro (tokens, i, first, SemanticTable)
    global numParametro
    SA.CheckNumberParameters (SemanticTable, numParametro,token)
    SA.CheckTypeParameters (SemanticTable,listaParam,token)
    if (tokens[i][0] == 'Fechaparêntese'):
        i += 1
    else:
        Error.SyntaticError (tokens[i])
    return i

#Função que 
def Parametro (tokens, i, first, SemanticTable):
    global numParametro
    numParametro = 0
    if (tokens[i][0] in first['Lista_Parametro']):
        i = Lista_Parametro (tokens, i, first, SemanticTable)
    return i

#Função que 
def Lista_Parametro (tokens, i, first, SemanticTable):
    if (tokens[i][0] in first['Nome_Numero']):
        global numParametro
        global listaParam
        numParametro += 1
        listaParam.append(tokens[i])
        i = Nome_Numero (tokens, i, first, SemanticTable)
    if (tokens[i][0] == 'Virgula'):
        i += 1 
        i = Lista_Parametro (tokens, i, first, SemanticTable)
    return i

#Função que 
def Expressao_Logica (tokens, i, first, SemanticTable):
    if (tokens[i][0] in first['Exp_Matematica']):
        global listaMesmoTipo
        listaMesmoTipo.append(tokens[i])
        i = Exp_Matematica (tokens, i, first, SemanticTable)
    if (tokens[i][0] in first['Op_Logico']):
        i = Op_Logico (tokens, i, first, SemanticTable)
        i = Expressao_Logica (tokens, i, first, SemanticTable)
    return i

#Função que 
def Exp_Matematica (tokens, i, first, SemanticTable):
    if (tokens[i][0] in first['Nome_Numero']):
        i = Nome_Numero (tokens, i, first, SemanticTable)
    if (tokens[i][0] in first['Op_Matematico']): 
        i = Op_Matematico (tokens, i, first, SemanticTable)
        i = Exp_Matematica (tokens, i, first, SemanticTable)
    return i

#Função que 
def Nome_Numero (tokens, i, first, SemanticTable):
    if (tokens[i][0] in first['Nome']):
        i = Nome (tokens, i, first, SemanticTable) 
    elif (tokens[i][0] == 'Número'):
        i = Numero (tokens, i, first, SemanticTable)
    else:
        Error.SyntaticError (tokens[i])
    return i

#Função que 
def Op_Logico (tokens, i, first, SemanticTable):
    if (tokens[i][0] in first['Op_Logico']):
        i += 1
    else:
        Error.SyntaticError (tokens[i])
    return i

#Função que 
def Op_Matematico (tokens, i, first, SemanticTable):
    if (tokens[i][0] in first['Op_Matematico']):
        i += 1
    else:
        Error.SyntaticError (tokens[i])
    return i

#Função que 
def Nome (tokens, i, first, SemanticTable):
    global escopo
    SA.CheckID (SemanticTable,tokens[i],escopo)
    SA.CheckConst (SemanticTable,tokens[i],tokens[i+1])
    i = Identificador (tokens, i, first, SemanticTable)
    if (tokens[i][0] == 'Ponto'):
        i +=1
        i = Nome (tokens, i, first, SemanticTable)
    elif (tokens[i][0] == 'Abrecolchete'):
        i += 1
        i = Nome_Numero (tokens, i, first, SemanticTable)
        if (tokens[i][0] == 'Fechacolchete'):
            i += 1
    return i

# Função que
def Identificador (tokens, i, first, SemanticTable):
    if (tokens[i][0] == 'Identificador'):
        i += 1
    else:
        Error.SyntaticError (tokens[i])
    return i

# Função que 
def PrintTable (SemanticTable):
    for i in SemanticTable:
        print(i)