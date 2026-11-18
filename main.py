import base64
import os
import sys

from antlr4 import CommonTokenStream
from antlr4.Token import CommonToken, Token
from antlr4.Lexer import TokenSource
from antlr4.CommonTokenFactory import CommonTokenFactory

from AssisParser import AssisParser
from MeuVisitorCustomizado import MeuVisitorCustomizado


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


def mapa_tipos():
    """nome simbólico -> número do token, pelo vocabulário do parser."""
    return {nome: i for i, nome in enumerate(AssisParser.symbolicNames)
            if nome and not nome.startswith("<")}


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
            tipo_num = tipos.get(tipo)
            if tipo_num is None:
                print(f"Tipo de token desconhecido: {tipo} ({caminho}:{n})")
                sys.exit(1)
            t = CommonToken(type=tipo_num)
            t.text = base64.b64decode(b64).decode("utf-8")
            t.line = int(linha)
            t.column = int(coluna) - 1               # ANTLR: coluna 0-based
            t.tokenIndex = len(tokens)
            tokens.append(t)

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


def main(argv):
    caminho = argv[1] if len(argv) > 1 else "tokens.tsv"
    if not os.path.exists(caminho):
        print(f"Erro: o arquivo {caminho} não foi encontrado. Rode antes o lexer_aluno.py.")
        sys.exit(1)

    # Em vez de AssisLexer + FileStream:
    stream = CommonTokenStream(ListaTokenSource(ler_tokens(caminho)))
    parser = AssisParser(stream)
    tree = parser.program()
    erros_sintaxe = parser.getNumberOfSyntaxErrors()

    relatorio = ["ÁRVORE DE SINTAXE (AST)",
                 tree.toStringTree(recog=parser), "", ""]

    if erros_sintaxe > 0:
        relatorio += ["RESULTADO",
                      f"{erros_sintaxe} erro(s) de sintaxe; análise semântica não executada."]
    else:
        visitor = MeuVisitorCustomizado()
        visitor.visit(tree)

        relatorio += ["TABELA DE SÍMBOLOS", visitor.tabela.dump(), ""]
        relatorio += ["RESULTADO SEMÂNTICO"]
        if not visitor.com_erros:
            relatorio += ["Análise semântica concluída sem erros!"]
        else:
            relatorio += [f"Análise semântica finalizada com {len(visitor.erros)} erro(s):"]
            relatorio += visitor.erros

    with open("relatorio_saida.txt", "w", encoding="utf-8") as f:
        f.write("\n".join(relatorio) + "\n")
    print("Análise concluída. Relatório salvo em: relatorio_saida.txt")


if __name__ == "__main__":
    main(sys.argv)