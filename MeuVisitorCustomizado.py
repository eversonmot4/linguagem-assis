"""
Visitor de análise semântica da linguagem Assis
(porte de SemanticVisitor.dart, adaptado à gramática Assis.g4).

Verificações:
  * variável/função usada sem declaração; redeclaração no mesmo escopo
  * tipo da expressão x tipo declarado (varDecl, atribuição, argumentos,
    retorno): permitido apenas o alargamento int -> float
  * operadores aritméticos exigem int/float; ordenação (< > <= >=) exige
    int/float; == e != exigem tipos iguais (ou ambos numéricos)
  * chamada de função: existência, nº de argumentos e tipos
  * 'redire' fora de função ou com tipo diferente do retorno declarado

Cada visit* de expressão devolve o TIPO da expressão ('int', 'float',
'char', 'bool', 'String') ou None quando há erro (o erro já foi
reportado, então não se reporta em cascata).
"""
from AssisParser import AssisParser
from AssisVisitor import AssisVisitor
from TabelaDeSimbolos import TabelaDeSimbolos

NUMERICOS = {"int", "float"}


class MeuVisitorCustomizado(AssisVisitor):
    def __init__(self):
        self.tabela = TabelaDeSimbolos()
        self.erros: list[str] = []
        self._retorno_atual: str | None = None   # tipo de retorno da função em análise

    @property
    def com_erros(self) -> bool:
        return len(self.erros) > 0

    # ---- utilitários -----------------------------------------------
    def _erro(self, linha, mensagem: str) -> None:
        texto = f"Erro Semântico [Linha {linha if linha is not None else '?'}]: {mensagem}"
        print(texto)
        self.erros.append(texto)

    @staticmethod
    def _compativel(destino: str, origem: str) -> bool:
        """origem pode ser usada onde se espera destino? (int -> float ok)"""
        return destino == origem or (destino == "float" and origem == "int")

    @staticmethod
    def _tipo_numerico(a: str, b: str) -> str:
        return "float" if "float" in (a, b) else "int"

    # ---- 1. declarações e escopos ----------------------------------
    def visitVarDecl(self, ctx: AssisParser.VarDeclContext):
        tipo_decl = ctx.type_().getText()
        tok = ctx.ID().getSymbol()
        nome, linha = tok.text, tok.line

        tipo_expr = self.visit(ctx.expr())      # visita antes de declarar

        if not self.tabela.adicionar(nome, tipo_decl):
            self._erro(linha, f"A variável '{nome}' já foi declarada neste escopo.")
            return None
        if tipo_expr is not None and not self._compativel(tipo_decl, tipo_expr):
            self._erro(linha, f"Incompatibilidade de tipos na declaração de '{nome}': "
                              f"esperado '{tipo_decl}', mas recebeu '{tipo_expr}'.")
        return None

    def visitFunctionDecl(self, ctx: AssisParser.FunctionDeclContext):
        retorno = ctx.type_().getText()
        tok = ctx.ID().getSymbol()
        nome, linha = tok.text, tok.line

        params = []
        if ctx.paramList() is not None:
            params = [p.type_().getText() for p in ctx.paramList().param()]

        # declara ANTES de visitar o corpo (permite recursão)
        if not self.tabela.adicionar_funcao(nome, retorno, params):
            self._erro(linha, f"A função '{nome}' já foi declarada.")

        self.tabela.entrar_escopo()
        anterior, self._retorno_atual = self._retorno_atual, retorno

        if ctx.paramList() is not None:
            self.visit(ctx.paramList())          # declara os parâmetros
        for stmt in ctx.block().statement():     # corpo no mesmo escopo dos parâmetros
            self.visit(stmt)

        self._retorno_atual = anterior
        self.tabela.sair_escopo()
        return None

    def visitParam(self, ctx: AssisParser.ParamContext):
        tipo = ctx.type_().getText()
        tok = ctx.ID().getSymbol()
        if not self.tabela.adicionar(tok.text, tipo):
            self._erro(tok.line, f"Parâmetro duplicado '{tok.text}'.")
        return None

    def visitBlock(self, ctx: AssisParser.BlockContext):
        self.tabela.entrar_escopo()
        self.visitChildren(ctx)
        self.tabela.sair_escopo()
        return None

    def visitReturnStmt(self, ctx: AssisParser.ReturnStmtContext):
        tipo = self.visit(ctx.expr())
        linha = ctx.RETURN().getSymbol().line
        if self._retorno_atual is None:
            self._erro(linha, "'redire' usado fora de uma função.")
        elif tipo is not None and not self._compativel(self._retorno_atual, tipo):
            self._erro(linha, f"A função retorna '{self._retorno_atual}', "
                              f"mas 'redire' devolve '{tipo}'.")
        return None

    # ---- 2. expressões ---------------------------------------------
    # As condições de si/alitersi/dum são 'exprLog', que a gramática já
    # garante ser uma comparação (bool); basta visitá-las (visitChildren).

    def visitComparacao(self, ctx: AssisParser.ComparacaoContext):
        return self.visit(ctx.exprLog())

    def visitExpressaoAritmetica(self, ctx: AssisParser.ExpressaoAritmeticaContext):
        return self.visit(ctx.additiveExpr())

    def visitAtribuicao(self, ctx: AssisParser.AtribuicaoContext):
        tok = ctx.ID().getSymbol()
        nome, linha = tok.text, tok.line
        tipo_expr = self.visit(ctx.expr())
        tipo_var = self.tabela.get_tipo(nome)

        if tipo_var is None:
            self._erro(linha, f"A variável '{nome}' foi usada na atribuição sem ter sido declarada.")
            return None
        if tipo_var == "funct":
            self._erro(linha, f"'{nome}' é uma função e não pode receber atribuição.")
            return None
        if tipo_expr is not None and not self._compativel(tipo_var, tipo_expr):
            self._erro(linha, f"Não é possível atribuir '{tipo_expr}' à variável "
                              f"'{nome}' do tipo '{tipo_var}'.")
            return None
        return tipo_var                          # permite a = b = 10

    def visitExprLog(self, ctx: AssisParser.ExprLogContext):
        esq = self.visit(ctx.additiveExpr(0))
        dir_ = self.visit(ctx.additiveExpr(1))
        if esq is None or dir_ is None:
            return None
        op = ctx.getChild(1).getText()
        linha = ctx.start.line

        if op in ("==", "!="):
            ok = esq == dir_ or (esq in NUMERICOS and dir_ in NUMERICOS)
            if not ok:
                self._erro(linha, f"Operadores '==' e '!=' exigem tipos compatíveis "
                                  f"(recebeu '{esq}' e '{dir_}').")
                return None
        else:
            if esq not in NUMERICOS or dir_ not in NUMERICOS:
                self._erro(linha, f"O operador '{op}' exige operandos int ou float "
                                  f"(recebeu '{esq}' e '{dir_}').")
                return None
        return "bool"

    def _aritmetica(self, ctx):
        """Dobra (a op b op c ...) da esquerda para a direita."""
        tipo = self.visit(ctx.getChild(0))
        for i in range(1, ctx.getChildCount(), 2):
            op = ctx.getChild(i).getText()
            dir_ = self.visit(ctx.getChild(i + 1))
            if tipo is None or dir_ is None:
                tipo = None
                continue
            if tipo not in NUMERICOS or dir_ not in NUMERICOS:
                self._erro(ctx.start.line, f"O operador '{op}' exige operandos int ou "
                                           f"float (recebeu '{tipo}' e '{dir_}').")
                tipo = None
            else:
                tipo = self._tipo_numerico(tipo, dir_)
        return tipo

    def visitAdditiveExpr(self, ctx: AssisParser.AdditiveExprContext):
        return self._aritmetica(ctx)

    def visitMultiplicativeExpr(self, ctx: AssisParser.MultiplicativeExprContext):
        return self._aritmetica(ctx)

    def visitEntreParenteses(self, ctx: AssisParser.EntreParentesesContext):
        return self.visit(ctx.expr())

    def visitEntreChaves(self, ctx: AssisParser.EntreChavesContext):
        return self.visit(ctx.expr())

    def visitChamadaFuncao(self, ctx: AssisParser.ChamadaFuncaoContext):
        tok = ctx.ID().getSymbol()
        nome, linha = tok.text, tok.line
        tipos_args = [self.visit(e) for e in (ctx.expr() or [])]   # visita sempre

        if not self.tabela.existe(nome):
            self._erro(linha, f"A função '{nome}' foi chamada sem ter sido declarada.")
            return None
        assinatura = self.tabela.get_funcao(nome)
        if assinatura is None:
            self._erro(linha, f"'{nome}' não é uma função.")
            return None

        retorno, params = assinatura
        if len(tipos_args) != len(params):
            self._erro(linha, f"A função '{nome}' espera {len(params)} argumento(s), "
                              f"mas recebeu {len(tipos_args)}.")
            return retorno
        for i, (esperado, recebido) in enumerate(zip(params, tipos_args), 1):
            if recebido is not None and not self._compativel(esperado, recebido):
                self._erro(linha, f"Argumento {i} de '{nome}': esperado '{esperado}', "
                                  f"mas recebeu '{recebido}'.")
        return retorno

    # ---- 3. folhas -------------------------------------------------
    def visitIdentificador(self, ctx: AssisParser.IdentificadorContext):
        tok = ctx.ID().getSymbol()
        tipo = self.tabela.get_tipo(tok.text)
        if tipo is None:
            self._erro(tok.line, f"A variável '{tok.text}' foi usada sem ter sido declarada.")
            return None
        if tipo == "funct":
            self._erro(tok.line, f"'{tok.text}' é uma função; use '{tok.text}(...)' para chamá-la.")
            return None
        return tipo

    def visitInteiroLiteral(self, ctx):  return "int"
    def visitFloatLiteral(self, ctx):    return "float"
    def visitCharLiteral(self, ctx):     return "char"
    def visitTextoLiteral(self, ctx):    return "String"
    def visitTrueLiteral(self, ctx):     return "bool"
    def visitFalseLiteral(self, ctx):    return "bool"