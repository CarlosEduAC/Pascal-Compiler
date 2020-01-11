# -*- coding: utf-8 -*-
#Importa a biblioteca usada para manipular cadeias de caracteres
import re
#Importa a biblioteca usada para tratar possíveis erros
import Error

# Função que realiza a Análise Léxica
def LexicalAnalyzer ():
	code = RemoveComments (ReadCode ('Fonte.pas'))
	tokens = CreateTokens (code)
	return tokens
	
# Função Para Ler Código Fonte Pascal
def ReadCode (path):
	try:
		arq = open(path, 'r', encoding = 'utf8')
		code = arq.read()
		arq.close()
	except:
		Error.LexicalError(('','',0))
	return code

# Função Para Remover Comentários e Tabulações no Código Fonte Pascal
def RemoveComments (code):
	#newcode = re.sub(r'//.*\n','', code)
	#newcode = re.sub(r'{(?<=\{)[^\}]+?(?=\})}','', newcode)
	newcode = re.sub(r'\t','', code)
	#newcode = re.sub(r'\n{2,}','\n', newcode)
	return newcode

# Função Para Criação da Lista de Tokens
def CreateTokens (code):
	tokens = []
	numLine = 1
	i = 0
	try:
		while (i < len(code)):
			token = ''
			#Ignora espaços
			if (code[i] == ' '):
				i += 1
			#Ignora comentários //	
			elif (code[i] == '/'):
				while (code[i] != '\n'):
					i += 1
			#Ignora comentários {}	
			elif (code[i] == '{'):
				while (code[i] != '}'):
					if (code[i] == '\n'):
						numLine += 1
					i += 1
				i += 1
			#Conta número de linhas
			elif (code[i] == '\n'):
				numLine += 1
				i += 1
			#Começa com letra
			elif (code[i].isalpha()):
				try:
					while(code[i].isalnum()):
						token += code[i]
						i += 1
					tokens.append(IdentifyToken(token,0,numLine))
				except:
					tokens.append(IdentifyToken(token,0,numLine))
					i += 1
			#Começa com número
			elif (code[i].isdecimal()):
				try:
					while (code[i].isdecimal()):
						token += code[i]
						i += 1
					if (code[i] == '.'):
						token += code[i]
						i += 1
					while (code[i].isdecimal()):
						token += code[i]
						i += 1
					tokens.append(IdentifyToken(token,1,numLine))
				except:
					i += 1
			#Símbolos reservados
			else:
				if(code[i] == '('):
					tokens.append(('Abreparêntese', '(', numLine))                    
				elif(code[i] == ')'):
					tokens.append(('Fechaparêntese', ')', numLine))                
				elif(code[i] == '['):
					tokens.append(('Abrecolchete', '[', numLine))
				elif(code[i] == ']'):
					tokens.append(('Fechacolchete', ']', numLine))                    
				elif(code[i] == '>' or code[i] == '<' or code[i] == '=' or code[i] == '!'):
					tokens.append(('Operador Relacional', code[i], numLine))  
				elif(code[i] == '+' or code[i] == '-' or code[i] == '*' or code[i] == '/'):
					tokens.append(('Operador Matemático', code[i], numLine))
				elif(code[i] == ':' and code[i+1] == '='):
					tokens.append(('Atribuição', ':=', numLine))
					i += 1
				elif (code[i] == ':'):
					tokens.append(('DoisPontos',':',numLine))
				elif (code[i] == ';'):
					tokens.append(('PontoEVirgula',';',numLine))
				elif (code[i] == ','):
					tokens.append(('Virgula',',',numLine))
				elif (code[i] == '.'):
					tokens.append(('Ponto','.',numLine))
				elif (code[i] == '"'):
					token += '"'
					i += 1
					while(code[i] != '"'):
						token += code[i]
						i += 1
					token += '"'
					tokens.append(('Sequência',token,numLine))
				else:
					token = code[i]
					tokens.append(('Erro',token,numLine))
					Error.LexicalError(('',token,numLine))

				i += 1
	except:
		Error.LexicalError(token)
	return tokens

# Função para Identificar Token
def IdentifyToken (token,flag,numLine):
	if(flag == 0):
		if(token == 'program'):
			return (token,'program',numLine)
		elif(token == 'begin'):
			return (token,'begin',numLine)
		elif(token == 'end'):
			return (token,'end',numLine)
		elif(token == 'const'):
			return (token,'const',numLine)
		elif(token == 'type'):
			return (token,'type',numLine)
		elif(token == 'var'):
			return (token,'var',numLine)
		elif(token == 'integer'):
			return (token,'integer',numLine)
		elif(token == 'real'):
			return (token,'real',numLine)
		elif(token == 'array'):
			return (token,'array',numLine)
		elif(token == 'of'):
			return (token,'of',numLine)
		elif(token == 'record'):
			return (token,'record',numLine)
		elif(token == 'function'):
			return (token,'function',numLine)
		elif(token == 'while'):
			return (token,'while',numLine)
		elif(token == 'if'):
			return (token,'if',numLine)
		elif(token == 'then'):
			return (token,'then',numLine)
		elif(token == 'write'):
			return (token,'write',numLine)
		elif(token == 'read'):
			return (token,'read',numLine)
		elif(token == 'else'):
			return (token,'else',numLine)
		else:
			return ('Identificador',token,numLine)
	else:
		if(token.isdecimal()):
			return ('Número',int(token),numLine)
		else:
			return ('Número',float(token),numLine)
			
# Função para Imprimir Tokens
def PrintTokens (tokens):
	for i in tokens:	
		print(i)