"""
main.py — PROGRAMA PRINCIPAL: liga as três fases do front-end do compilador.

    FASE 1  ANÁLISE LÉXICA      lexer_aluno.py   (executado ANTES, separadamente)
              texto-fonte --> tokens.tsv
    FASE 2  ANÁLISE SINTÁTICA   AssisParser.py   (gerado pelo ANTLR a partir do Assis.g4)
              tokens.tsv --> árvore sintática                       [este arquivo]
    FASE 3  ANÁLISE SEMÂNTICA   MeuVisitorCustomizado.py + TabelaDeSimbolos.py
              árvore sintática --> tabela de símbolos + erros de tipo/escopo
                                                                    [este arquivo chama]

Neste arquivo ficam:
  * a PONTE entre a fase léxica e a sintática (ListaTokenSource, ler_tokens):
    em vez de usar o AssisLexer gerado pelo ANTLR, o parser recebe os tokens
    produzidos pelo NOSSO lexer, lidos de tokens.tsv;
  * a execução do parser e do visitor semântico (função main);
  * a gravação do relatorio_saida.txt.

Uso:
    python lexer_aluno.py exemplo.txt     # fase 1 -> gera tokens.tsv
    python main.py                        # fases 2 e 3 -> gera relatorio_saida.txt
"""
import base64
import os
import sys

# --- Runtime do ANTLR (biblioteca usada pelo parser gerado) ---------------
from antlr4 import CommonTokenStream
from antlr4.Token import CommonToken, Token
from antlr4.Lexer import TokenSource
from antlr4.CommonTokenFactory import CommonTokenFactory

# --- FASE 2: o parser gerado pelo ANTLR a partir de Assis.g4 --------------
from AssisParser import AssisParser
# --- FASE 3: o visitor que faz a análise semântica ------------------------
from MeuVisitorCustomizado import MeuVisitorCustomizado


# =====================================================================
# PONTE FASE 1 -> FASE 2  (léxica -> sintática)
# ---------------------------------------------------------------------
# O parser do ANTLR pede tokens a uma "fonte de tokens" (TokenSource).
# Normalmente essa fonte é o AssisLexer gerado pelo ANTLR; aqui criamos
# uma fonte própria que apenas devolve, um a um, os tokens que o NOSSO
# lexer já calculou. É assim que o lexer do aluno substitui o do ANTLR.
# =====================================================================
class ListaTokenSource(TokenSource):
    """TokenSource que devolve uma lista de tokens pronta (o runtime
    Python não traz ListTokenSource; os de Java e Dart trazem)."""

    def __init__(self, tokens):
        self._tokens = tokens
        self._i = 0
        # O parser usa a fábrica do TokenSource para criar tokens "faltando"
        # quando se recupera de um erro de sintaxe (ex.: ';' ausente).
        self._factory = CommonTokenFactory.DEFAULT

    def nextToken(self):
        # Chamado pelo parser sempre que precisa do próximo token.
        tok = self._tokens[min(self._i, len(self._tokens) - 1)]
        self._i += 1                  # depois do EOF continua devolvendo o EOF
        return tok

    def getSourceName(self):
        return "tokens.tsv"

    @property
    def line(self):
        return self._tokens[min(self._i, len(self._tokens) - 1)].line

    @property
    def column(self):
        return self._tokens[min(self._i, len(self._tokens) - 1)].column

    @property
    def inputStream(self):
        return None


# O TSV guarda o tipo como TEXTO ("TP_INT"), mas o parser trabalha com
# NÚMEROS (cada token da gramática ganha um inteiro quando o ANTLR gera o
# parser). Este dicionário faz a tradução nome -> número. É por isso que os
# nomes em lexer_aluno.py precisam ser idênticos aos de Assis.g4.
def mapa_tipos():
    """nome simbólico -> número do token, pelo vocabulário do parser."""
    return {nome: i for i, nome in enumerate(AssisParser.symbolicNames)
            if nome and not nome.startswith("<")}


# Lê o tokens.tsv (TIPO <TAB> LINHA <TAB> COLUNA <TAB> TEXTO_EM_BASE64) e
# monta a lista de tokens no formato que o ANTLR entende.
def ler_tokens(caminho):
    """Lê o TSV e devolve a lista de CommonToken, com o EOF no final."""
    tipos = mapa_tipos()
    tokens = []
    with open(caminho, "r", encoding="utf-8") as f:
        for n, linha_tsv in enumerate(f, 1):
            linha_tsv = linha_tsv.rstrip("\n")
            if not linha_tsv.strip():
                continue
            tipo, linha, coluna, b64 = linha_tsv.split("\t")
            tipo_num = tipos.get(tipo)       # nome simbólico -> número do token
            if tipo_num is None:                 # nome que a gramática não conhece
                print(f"Tipo de token desconhecido: {tipo} ({caminho}:{n})")
                sys.exit(1)
            t = CommonToken(type=tipo_num)   # token do ANTLR com o tipo numérico
            t.text = base64.b64decode(b64).decode("utf-8")
            t.line = int(linha)
            t.column = int(coluna) - 1               # ANTLR: coluna 0-based
            t.tokenIndex = len(tokens)
            tokens.append(t)

    # O lexer não grava o EOF (fim de arquivo), mas a regra `program` da
    # gramática termina em EOF; então ele é acrescentado aqui, no fim da lista.
    eof = CommonToken(type=Token.EOF)
    eof.text = "<EOF>"
    if tokens:
        eof.line = tokens[-1].line
        eof.column = tokens[-1].column + len(tokens[-1].text)
    else:
        eof.line, eof.column = 1, 0
    eof.tokenIndex = len(tokens)
    tokens.append(eof)
    return tokens


# =====================================================================
# EXECUÇÃO: FASE 2 (sintática) e FASE 3 (semântica)
# =====================================================================
def main(argv):
    caminho = argv[1] if len(argv) > 1 else "tokens.tsv"
    if not os.path.exists(caminho):
        print(f"Erro: o arquivo {caminho} não foi encontrado. Rode antes o lexer_aluno.py.")
        sys.exit(1)

    # ---------------- FASE 2: ANÁLISE SINTÁTICA ----------------
    # Em vez de AssisLexer + FileStream (que leriam o código-fonte direto),
    # o parser é alimentado pelos tokens do nosso lexer.
    stream = CommonTokenStream(ListaTokenSource(ler_tokens(caminho)))
    parser = AssisParser(stream)
    # `program` é a regra inicial da gramática. O parser confere se a sequência
    # de tokens obedece às regras do Assis.g4 e devolve a ÁRVORE SINTÁTICA.
    # Erros de sintaxe (ex.: ';' faltando) são impressos pelo ANTLR e contados.
    tree = parser.program()
    erros_sintaxe = parser.getNumberOfSyntaxErrors()

    # A árvore é exibida em formato de lista aninhada: (regra filho filho ...)
    relatorio = ["ÁRVORE DE SINTAXE (AST)",
                 tree.toStringTree(recog=parser), "", ""]

    # A semântica só faz sentido sobre uma árvore válida: se houve erro de
    # sintaxe, ela é pulada para não gerar erros em cascata.
    if erros_sintaxe > 0:
        relatorio += ["RESULTADO",
                      f"{erros_sintaxe} erro(s) de sintaxe; análise semântica não executada."]
    else:
        # ---------------- FASE 3: ANÁLISE SEMÂNTICA ----------------
        # O visitor percorre a árvore nó a nó, preenchendo a tabela de símbolos
        # e conferindo declarações, escopos e tipos (ver MeuVisitorCustomizado.py).
        visitor = MeuVisitorCustomizado()
        visitor.visit(tree)

        relatorio += ["TABELA DE SÍMBOLOS", visitor.tabela.dump(), ""]
        relatorio += ["RESULTADO SEMÂNTICO"]
        if not visitor.com_erros:
            relatorio += ["Análise semântica concluída sem erros!"]
        else:
            relatorio += [f"Análise semântica finalizada com {len(visitor.erros)} erro(s):"]
            relatorio += visitor.erros

    # Resultado das fases 2 e 3 gravado em arquivo.
    with open("relatorio_saida.txt", "w", encoding="utf-8") as f:
        f.write("\n".join(relatorio) + "\n")
    print("Análise concluída. Relatório salvo em: relatorio_saida.txt")


if __name__ == "__main__":
    main(sys.argv)