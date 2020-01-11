# -*- coding: utf-8 -*-
#Importa a biblioteca usada para realizar a análise léxica
import LexicalAnalyzer as LA
#Importa a biblioteca usada para realizar a análise sintática e chama a biblioteca usada para realizar a análise semântica
import SyntacticAnalyzer as SA

# Função Inicial
def Main ():
	tokens = LA.LexicalAnalyzer ()
	#LA.PrintTokens (tokens)
	SemanticTable = SA.SyntacticAnalyzer(tokens)
	#SA.PrintTable (SemanticTable)

# Inicio do programa
Main ()