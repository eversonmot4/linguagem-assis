"""
MeuVisitorCustomizado.py — FASE 3 DO COMPILADOR: ANÁLISE SEMÂNTICA
===================================================================

As fases anteriores só olham a FORMA do programa:
  * análise léxica    -> "essas palavras existem na linguagem?"
  * análise sintática -> "elas estão na ordem certa?"
A análise semântica olha o SIGNIFICADO: "o programa faz sentido?"
Por exemplo, `int x = "abc";` é sintaticamente correto (tipo, nome, '=',
valor, ';'), mas semanticamente errado, porque um texto não cabe em int.

Como funciona
-------------
Este arquivo implementa o padrão VISITOR sobre a árvore sintática que o
ANTLR monta. O método `visit(árvore)` desce pela árvore e, em cada nó,
chama o método `visitXxx` correspondente a uma regra (ou rótulo `# nome`)
de Assis.g4: visitVarDecl para a regra varDecl, visitChamadaFuncao para o
rótulo `# chamadaFuncao`, e assim por diante. Nós sem método próprio
usam o padrão (visitChildren), que apenas visita os filhos.

Duas ideias sustentam tudo:
  1. TABELA DE SÍMBOLOS (TabelaDeSimbolos.py): lembra o que já foi
     declarado (nome, tipo, escopo) e é consultada a cada uso.
  2. TIPO COMO RESULTADO: cada visit* de EXPRESSÃO devolve o tipo da
     expressão ('int', 'float', 'char', 'bool', 'String') ou None quando
     há erro (o erro já foi reportado; None evita erros em cascata).

Verificações:
  * variável/função usada sem declaração; redeclaração no mesmo escopo
  * tipo da expressão x tipo declarado (varDecl, atribuição, argumentos,
    retorno): permitido apenas o alargamento int -> float
  * operadores aritméticos exigem int/float; ordenação (< > <= >=) exige
    int/float; == e != exigem tipos iguais (ou ambos numéricos)
  * chamada de função: existência, nº de argumentos e tipos
  * 'redire' fora de função ou com tipo diferente do retorno declarado
"""
from AssisParser import AssisParser        # classes de contexto (um tipo de nó por regra da gramática)
from AssisVisitor import AssisVisitor      # visitor-base gerado pelo ANTLR (visitChildren etc.)
from TabelaDeSimbolos import TabelaDeSimbolos

NUMERICOS = {"int", "float"}               # tipos que aceitam + - * / < > <= >=


# Herda de AssisVisitor (gerado pelo ANTLR) e SOBRESCREVE só os métodos dos
# nós que importam para a semântica; os demais seguem o comportamento padrão.
class MeuVisitorCustomizado(AssisVisitor):
    def __init__(self):
        self.tabela = TabelaDeSimbolos()         # declarações vistas até agora (com escopos)
        self.erros: list[str] = []               # mensagens de erro semântico, em ordem
        self._retorno_atual: str | None = None   # tipo de retorno da função em análise
                                                 # (None = estamos fora de qualquer função)

    @property
    def com_erros(self) -> bool:
        # Usado por main.py para decidir qual mensagem final escrever no relatório.
        return len(self.erros) > 0

    # ---- utilitários -----------------------------------------------
    def _erro(self, linha, mensagem: str) -> None:
        # Registra o erro (e o imprime) mas NÃO interrompe: a análise continua
        # para listar todos os erros de uma vez.
        texto = f"Erro Semântico [Linha {linha if linha is not None else '?'}]: {mensagem}"
        print(texto)
        self.erros.append(texto)

    @staticmethod
    def _compativel(destino: str, origem: str) -> bool:
        """origem pode ser usada onde se espera destino? (int -> float ok)"""
        return destino == origem or (destino == "float" and origem == "int")

    @staticmethod
    def _tipo_numerico(a: str, b: str) -> str:
        # Regra do tipo do resultado: se qualquer operando é float, o resultado é float
        # (ex.: 1 + 2.5 -> float); só int com int permanece int.
        return "float" if "float" in (a, b) else "int"

    # ---- 1. declarações e escopos ----------------------------------
    # Regras de Assis.g4 tratadas aqui: varDecl, functionDecl, param, block, returnStmt.
    # Aqui a tabela de símbolos é ESCRITA (declarações) e os escopos são abertos/fechados.
    def visitVarDecl(self, ctx: AssisParser.VarDeclContext):
        # varDecl : type ID ATRIB expr PONTO_VIRGULA      ex.: int x = 10;
        tipo_decl = ctx.type_().getText()       # tipo escrito na declaração ('int')
        tok = ctx.ID().getSymbol()              # token do nome, guarda texto e linha
        nome, linha = tok.text, tok.line

        # Visita a expressão ANTES de declarar a variável: assim `int x = x + 1;`
        # acusa x como não declarada. O retorno é o tipo da expressão.
        tipo_expr = self.visit(ctx.expr())      # visita antes de declarar

        # adicionar() devolve False se o nome já existe NO MESMO escopo (redeclaração)
        if not self.tabela.adicionar(nome, tipo_decl):
            self._erro(linha, f"A variável '{nome}' já foi declarada neste escopo.")
            return None
        # Verificação de TIPOS: o valor cabe no tipo declarado? (None = já deu erro, não repete)
        if tipo_expr is not None and not self._compativel(tipo_decl, tipo_expr):
            self._erro(linha, f"Incompatibilidade de tipos na declaração de '{nome}': "
                              f"esperado '{tipo_decl}', mas recebeu '{tipo_expr}'.")
        return None

    def visitFunctionDecl(self, ctx: AssisParser.FunctionDeclContext):
        # functionDecl : FUNC type ID PAR_ESQ paramList? PAR_DIR block
        #   ex.: funct int soma(int a, int b) { redire a + b; }
        retorno = ctx.type_().getText()       # tipo de retorno declarado
        tok = ctx.ID().getSymbol()
        nome, linha = tok.text, tok.line

        # Lista dos tipos dos parâmetros: é a "assinatura" usada depois para
        # conferir cada chamada (quantidade e tipos dos argumentos).
        params = []
        if ctx.paramList() is not None:
            params = [p.type_().getText() for p in ctx.paramList().param()]

        # declara ANTES de visitar o corpo (permite recursão)
        if not self.tabela.adicionar_funcao(nome, retorno, params):
            self._erro(linha, f"A função '{nome}' já foi declarada.")

        # Corpo da função = novo escopo (nível local). Guardamos o retorno esperado
        # para o `redire` conferir, e o valor anterior para restaurar ao sair.
        self.tabela.entrar_escopo()
        anterior, self._retorno_atual = self._retorno_atual, retorno

        if ctx.paramList() is not None:
            self.visit(ctx.paramList())          # declara os parâmetros
        for stmt in ctx.block().statement():     # corpo no mesmo escopo dos parâmetros
            self.visit(stmt)

        self._retorno_atual = anterior   # volta ao contexto de fora da função
        self.tabela.sair_escopo()        # descarta as variáveis locais e os parâmetros
        return None

    def visitParam(self, ctx: AssisParser.ParamContext):
        # param : type ID  — cada parâmetro vira uma variável local da função
        tipo = ctx.type_().getText()
        tok = ctx.ID().getSymbol()
        if not self.tabela.adicionar(tok.text, tipo):
            self._erro(tok.line, f"Parâmetro duplicado '{tok.text}'.")
        return None

    def visitBlock(self, ctx: AssisParser.BlockContext):
        # block : CHAVE_ESQ statement* CHAVE_DIR
        # Cada { ... } abre um escopo: variáveis declaradas dentro não existem fora.
        self.tabela.entrar_escopo()
        self.visitChildren(ctx)          # visita os comandos do bloco
        self.tabela.sair_escopo()
        return None

    def visitReturnStmt(self, ctx: AssisParser.ReturnStmtContext):
        # returnStmt : RETURN expr PONTO_VIRGULA   ex.: redire a + b;
        tipo = self.visit(ctx.expr())
        linha = ctx.RETURN().getSymbol().line
        if self._retorno_atual is None:      # não estamos dentro de nenhuma função
            self._erro(linha, "'redire' usado fora de uma função.")
        elif tipo is not None and not self._compativel(self._retorno_atual, tipo):
            self._erro(linha, f"A função retorna '{self._retorno_atual}', "
                              f"mas 'redire' devolve '{tipo}'.")
        return None

    # ---- 2. expressões ---------------------------------------------
    # Regras de Assis.g4 tratadas aqui: expr (rótulos atribuicao/comparacao/
    # expressaoAritmetica), exprLog, additiveExpr, multiplicativeExpr e
    # primaryExpr (chamadaFuncao, entreParenteses, entreChaves).
    # Aqui a tabela é CONSULTADA e o tipo de cada expressão é calculado de
    # baixo para cima: o tipo de uma conta depende dos tipos dos operandos.
    # As condições de si/alitersi/dum são 'exprLog', que a gramática já
    # garante ser uma comparação (bool); basta visitá-las (visitChildren).

    def visitComparacao(self, ctx: AssisParser.ComparacaoContext):
        # expr # comparacao -> só repassa o tipo da comparação (exprLog), que é 'bool'
        return self.visit(ctx.exprLog())

    def visitExpressaoAritmetica(self, ctx: AssisParser.ExpressaoAritmeticaContext):
        # expr # expressaoAritmetica -> repassa o tipo da soma/subtração
        return self.visit(ctx.additiveExpr())

    def visitAtribuicao(self, ctx: AssisParser.AtribuicaoContext):
        # expr # atribuicao : ID ATRIB expr      ex.: y = y + 1
        # Atribuição é EXPRESSÃO (devolve o tipo da variável), então a = b = 10 funciona.
        tok = ctx.ID().getSymbol()
        nome, linha = tok.text, tok.line
        tipo_expr = self.visit(ctx.expr())
        tipo_var = self.tabela.get_tipo(nome)

        if tipo_var is None:                 # variável nunca declarada
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
        # exprLog : additiveExpr (== | != | < | > | <= | >=) additiveExpr
        # Comparações sempre resultam em 'bool'. Como as condições de si/alitersi/dum
        # são do tipo exprLog, a gramática já garante que são booleanas e não é
        # preciso checar o tipo da condição nesses comandos.
        esq = self.visit(ctx.additiveExpr(0))
        dir_ = self.visit(ctx.additiveExpr(1))
        if esq is None or dir_ is None:
            return None
        op = ctx.getChild(1).getText()   # o operador está no filho do meio
        linha = ctx.start.line

        if op in ("==", "!="):             # igualdade: tipos iguais (ou ambos numéricos)
            ok = esq == dir_ or (esq in NUMERICOS and dir_ in NUMERICOS)
            if not ok:
                self._erro(linha, f"Operadores '==' e '!=' exigem tipos compatíveis "
                                  f"(recebeu '{esq}' e '{dir_}').")
                return None
        else:                            # ordem (< > <= >=): só números
            if esq not in NUMERICOS or dir_ not in NUMERICOS:
                self._erro(linha, f"O operador '{op}' exige operandos int ou float "
                                  f"(recebeu '{esq}' e '{dir_}').")
                return None
        return "bool"

    def _aritmetica(self, ctx):
        """Dobra (a op b op c ...) da esquerda para a direita."""
        # Compartilhado por additiveExpr e multiplicativeExpr, que têm o mesmo formato:
        # filho 0 = 1º operando; depois vêm pares (operador, operando).
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
        # additiveExpr : multiplicativeExpr ((+ | -) multiplicativeExpr)*
        return self._aritmetica(ctx)

    def visitMultiplicativeExpr(self, ctx: AssisParser.MultiplicativeExprContext):
        # multiplicativeExpr : primaryExpr ((* | /) primaryExpr)*
        # (a gramática já dá precedência de * e / sobre + e - ao aninhá-las assim)
        return self._aritmetica(ctx)

    def visitEntreParenteses(self, ctx: AssisParser.EntreParentesesContext):
        return self.visit(ctx.expr())

    def visitEntreChaves(self, ctx: AssisParser.EntreChavesContext):
        return self.visit(ctx.expr())

    def visitChamadaFuncao(self, ctx: AssisParser.ChamadaFuncaoContext):
        # primaryExpr # chamadaFuncao : ID PAR_ESQ (expr (VIRGULA expr)*)? PAR_DIR
        #   ex.: soma(10, 20)
        tok = ctx.ID().getSymbol()
        nome, linha = tok.text, tok.line
        tipos_args = [self.visit(e) for e in (ctx.expr() or [])]   # visita sempre

        # 1) o nome existe? 2) é mesmo uma função? 3) nº de argumentos? 4) tipo de cada um?
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
        return retorno                   # o tipo da chamada é o tipo de retorno da função

    # ---- 3. folhas -------------------------------------------------
    # Pontas da árvore: de onde o tipo "nasce". Identificador -> tipo vem da tabela;
    # literal -> tipo vem do próprio valor (definido pelo token léxico: INT, REAL, CHAR...).
    def visitIdentificador(self, ctx: AssisParser.IdentificadorContext):
        # primaryExpr # identificador : ID    (uso de uma variável)
        tok = ctx.ID().getSymbol()
        tipo = self.tabela.get_tipo(tok.text)
        if tipo is None:
            self._erro(tok.line, f"A variável '{tok.text}' foi usada sem ter sido declarada.")
            return None
        if tipo == "funct":
            self._erro(tok.line, f"'{tok.text}' é uma função; use '{tok.text}(...)' para chamá-la.")
            return None
        return tipo

    # token INT -> 'int', REAL -> 'float', CHAR -> 'char', STRING -> 'String', TRUE/FALSE -> 'bool'
    def visitInteiroLiteral(self, ctx):  return "int"
    def visitFloatLiteral(self, ctx):    return "float"
    def visitCharLiteral(self, ctx):     return "char"
    def visitTextoLiteral(self, ctx):    return "String"
    def visitTrueLiteral(self, ctx):     return "bool"
    def visitFalseLiteral(self, ctx):    return "bool"