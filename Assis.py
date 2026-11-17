import sys
from antlr4 import *
from gen.MiniCLexer import MiniCLexer
from gen.MiniCParser import MiniCParser

def main(argv):
    # Abre o arquivo de entrada
    input_stream = FileStream(argv[1])
    
    # Cria o Lexer e o fluxo de tokens
    lexer = MiniCLexer(input_stream)
    stream = CommonTokenStream(lexer)
    
    # Cria o Parser e executa a regra inicial (ex: 'program')
    parser = MiniCParser(stream)
    tree = parser.program()  # Substitua 'program' pelo nome da sua regra inicial
    
    # A partir daqui, você pode percorrer a árvore com um Visitor
    visitor = MeuVisitorCustomizado()
    visitor.visit(tree)

if __name__ == '__main__':
    main(sys.argv)