# -*- coding: utf-8 -*-
#Importa a biblioteca usada para usar funções do sistema operacional
import os

def LexicalError (token):
	if (token[2] != 0):
		print('\n***Erro Léxico na linha ', token[2],'. Problema com o ', token[0], '***\n')
	else:
		print('\n***Erro na Abertura do Arquivo***\n')

def SyntaticError (token):
	print('\n***Erro Sintático na linha ', token[2],'. Problema com o ', token[0], '***\n')

def SemanticError (token):
	print('\n***Erro Semântico na linha ', token[2],'. Problema com o ', token, '***\n')