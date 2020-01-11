# -*- coding: utf-8 -*-
#Importa a biblioteca usada para tratar possíveis erros
import Error

#Função que verifica ser o ID foi declarado antes de usado
def CheckID (SemanticTable, token, escopo):
    for linha in SemanticTable:
        #print(escopo)
        if (token[1] in linha):
            if (escopo in linha):
                return True
            elif ('field' in linha):
                return True
        if (token[1] == 'result'): 
            return True
    Error.SemanticError(token)

#Função que verifica se Const aparece do lado esquerdo de uma atribuição
def CheckConst (SemanticTable, token, nextToken):
    for linha in SemanticTable:
        if (token[1] in linha):
            if ( (linha[4] == 'const')  and (nextToken[1] == ':=')):
                Error.SemanticError(token)

#Função que verifica os nomes das funções
def CheckFunction (SemanticTable, token):
    for linha in SemanticTable:
        if (token[1] in linha and 'function' in linha):
            return True
    Error.SemanticError(token)
    return False    

#Função que verifica quantidade de parâmetros e argumentos
def CheckNumberParameters (SemanticTable, numParametro, token):
    for linha in SemanticTable:
        if ('function' in linha):
            if ((token[1] in linha) and (numParametro != linha[5])):
                Error.SemanticError((token))

#Função que verifica tipo de parâmetros e argumentos
def CheckTypeParameters (SemanticTable, tipoParametro, token):
    i = 0
    while (i < len(tipoParametro)):
        for linha in SemanticTable:
            if ('parâmetro' in linha and token[1] in linha and linha[5] == i+1):
                retorno = CheckTable(SemanticTable,tipoParametro[i][1])
                if ( retorno != 'False'):
                    if (retorno not in linha):
                        Error.SemanticError((token))
        i += 1

#Função que verifica se atribuição e comparação são do mesmo tipo
def CheckType (SemanticTable, tokens, escopo):
    tipo = []
    tamTokens = 0
    for token in tokens:
        if (token[0] == 'Identificador' and token[1] != 'result'):
            for linha in SemanticTable:
                if (token[1] in linha and token[2] >= linha[1]):
                    if ('vetor' in linha):
                        tipo.append('integer')
                    elif ('record' in linha):
                        tipo.append('real')
                    else:
                        tipo.append(linha[3])
                    tamTokens += 1
                    break
        else:
            if(token[1] != 'result'):
                tipo.append(Type(token[1]))
                tamTokens += 1
    if (tamTokens == tipo.count('real')):
        return True
    elif (tamTokens == tipo.count('integer')):
        return True
    elif (tamTokens == tipo.count('aluno')):
        return True
    else:
        Error.SemanticError((tokens))
        return False

def CheckTable (SemanticTable, id):
    for linha in SemanticTable:
        if (id in linha):
            return linha[3]
    return 'False'

def Type (num):
    if (type(num) == type(10)):
        return 'integer'
    elif (type(num) == type(10.0)):
        return 'real'
    