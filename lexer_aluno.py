"""
 Uso:
   python lexer_aluno.py exemplo.txt

 Estrutura espelhada em lexer_aluno.py
   1. Token
   2. AFD (tabela de transições)
   3. Configuração da linguagem
   4. Construtores genéricos (literal, trie)
   5. Construtores específicos (ID, NUM)
   6. Lexer
   7. Programa principal
"""
from __future__ import annotations
from dataclasses import dataclass
import base64
import sys


# =====================================================================
# 1. TOKEN
# =====================================================================

@dataclass
class Token:
    tipo: str
    valor: str
    linha: int
    coluna: int

    def __repr__(self) -> str:
        return f"<{self.tipo}, {self.valor!r}> @ {self.linha}:{self.coluna}"


# =====================================================================
# 2. AFD — tabela de transições
# =====================================================================

class AFD:
    """AFD representado por tabela (estado, símbolo) -> estado.

    Extensão: `padrao` guarda, por estado, uma transição "por
    complemento": (conjunto de caracteres excluídos, destino). Ela só é
    usada quando NÃO existe transição explícita na tabela principal.
    """

    def __init__(self, nome: str):
        self.nome = nome
        self.transicoes: dict[tuple[int, str], int] = {}
        self.padrao: dict[int, tuple[str, int]] = {}
        self.finais: set[int] = set()
        self.inicial: int = 0
        self._prox: int = 1

    def novo_estado(self) -> int:
        e = self._prox
        self._prox += 1
        return e

    def transicao(self, origem: int, simbolos: str, destino: int) -> None:
        """TODO 1: para CADA caractere c em `simbolos`, registre
        transicoes[(origem, c)] = destino."""
        for c in simbolos:
            self.transicoes[(origem, c)] = destino

    def transicao_padrao(self, origem: int, destino: int, exceto: str = "") -> None:
        """(Extensão) Qualquer caractere que NÃO esteja em `exceto` (e que
        não tenha transição explícita) leva de `origem` a `destino`.
        Equivale ao ~[...] do ANTLR."""
        self.padrao[origem] = (exceto, destino)

    def proximo_estado(self, estado: int, c: str) -> int | None:
        """Consulta a tabela; se não houver entrada explícita, tenta a
        transição por complemento. None = sem transição (estado morto)."""
        prox = self.transicoes.get((estado, c))
        if prox is not None:
            return prox
        if estado in self.padrao:
            exceto, destino = self.padrao[estado]
            if c not in exceto:
                return destino
        return None

    def marcar_final(self, estado: int) -> None:
        """TODO 2: adicione `estado` a self.finais."""
        self.finais.add(estado)

    def maior_prefixo(self, texto: str) -> int:
        """TODO 3: comprimento do MAIOR prefixo de `texto` aceito pelo AFD,
        ou -1 se nenhum prefixo for aceito.

        O autômato continua lendo até travar; a cada vez que passa por um
        estado final, anota a posição. Ao travar, vale a última anotada.
        """
        estado = self.inicial
        ultimo = 0 if estado in self.finais else -1
        for i, c in enumerate(texto):
            prox = self.proximo_estado(estado, c)
            if prox is None:
                break
            estado = prox
            if estado in self.finais:
                ultimo = i + 1
        return ultimo


# =====================================================================
# 3. CONFIGURAÇÃO DA LINGUAGEM ASSIS
# =====================================================================

# --- Alfabeto de identificadores: [a-zA-Z_][a-zA-Z_0-9]* ------------
LETRAS_ID       = "abcdefghijklmnopqrstuvwxyzABCDEFGHIJKLMNOPQRSTUVWXYZ"
INICIAIS_ID     = LETRAS_ID + "_"
CONTINUACAO_ID  = LETRAS_ID + "0123456789_"

# --- Dígitos ---------------------------------------------------------
DIGITOS = "0123456789"

# --- Palavras reservadas: lexema -> tipo ----------------------------
PALAVRAS_RESERVADAS: dict[str, str] = {
    "si":       "KW_IF",
    "aliter":   "KW_ELSE",
    "alitersi": "KW_ELSEIF",
    "funct":    "FUNC",
    "redire":   "RETURN",
    "dum":      "WHILE",
    "int":      "TP_INT",
    "float":    "TP_FLOAT",
    "char":     "TP_CHAR",
    "bool":     "TP_BOOL",
    "String":   "TP_STRING",
    "verum":    "TRUE",
    "falsum":   "FALSE",
}

# --- Operadores: lexema -> tipo --------------------------------------
OPERADORES: dict[str, str] = {
    "=":  "ATRIB",
    "+":  "OP_SOMA",
    "-":  "OP_SUB",
    "*":  "OP_MULT",
    "/":  "OP_DIV",
    "<=": "OP_LE",
    ">=": "OP_GE",
    "==": "OP_EQ",
    "!=": "OP_NE",
    "<":  "OP_LT",
    ">":  "OP_GT",
}

# --- Delimitadores (1 caractere): lexema -> tipo -------------------
SIMBOLOS: dict[str, str] = {
    "(": "PAR_ESQ",
    ")": "PAR_DIR",
    "{": "CHAVE_ESQ",
    "}": "CHAVE_DIR",
    ",": "VIRGULA",
    ";": "PONTO_VIRGULA",
    ".": "PONTO",
}

FIXOS: dict[str, str] = {**OPERADORES, **SIMBOLOS}

# --- Tipos brutos que o lexer descarta (comentários) -----------------
COMENTARIOS_IGNORADOS = {"LINE_COMMENT", "BLOCK_COMMENT"}

# --- Tipos brutos que representam ERRO léxico (AFDs detectores) ------
ERROS_LEXICOS: dict[str, str] = {
    "STRING_ABERTA": "Literal sem fechamento de aspas",
    "BLOCK_ABERTO":  "Comentário de bloco sem fechamento '*/'",
}


# =====================================================================
# 4. CONSTRUTORES GENÉRICOS DE AFDs
# =====================================================================

def afd_literal(nome: str, texto: str) -> AFD:
    """AFD que reconhece EXATAMENTE a string `texto` (um estado por
    prefixo; só o estado do texto completo é final)."""
    afd = AFD(nome)
    atual = afd.inicial
    for c in texto:
        prox = afd.novo_estado()
        afd.transicao(atual, c, prox)
        atual = prox
    afd.marcar_final(atual)
    return afd


def afd_conjunto_literais(nome: str, textos: list[str]) -> AFD:
    """AFD (trie) que reconhece QUALQUER uma das strings, compartilhando
    estados de prefixos comuns ("=" e "==" dividem o 1º estado)."""
    afd = AFD(nome)
    for texto in textos:
        atual = afd.inicial
        for c in texto:
            prox = afd.transicoes.get((atual, c))
            if prox is None:
                prox = afd.novo_estado()
                afd.transicao(atual, c, prox)
            atual = prox
        afd.marcar_final(atual)
    return afd


# =====================================================================
# 5. CONSTRUTORES ESPECÍFICOS
# =====================================================================

def afd_identificador() -> AFD:
    """[a-zA-Z_][a-zA-Z_0-9]* -> tipo bruto ID."""
    afd = AFD("ID")
    q1 = afd.novo_estado()
    afd.transicao(afd.inicial, INICIAIS_ID, q1)
    afd.transicao(q1, CONTINUACAO_ID, q1)
    afd.marcar_final(q1)
    return afd


def afd_numero() -> AFD:
    """[0-9]+ ('.' [0-9]+)? -> tipo bruto NUM (INT ou REAL).

        q0 -d-> q1(final, INT) -.-> q2 -d-> q3(final, REAL)
                 ^ d  |                       ^ d |
                 +----+                       +---+
    "1." NÃO é REAL: o AFD trava em q2 (não final); o último estado final
    visitado foi q1, logo o prefixo aceito é "1" (INT) e "." sobra (PONTO).
    A distinção INT/REAL é feita em _reclassificar.
    """
    afd = AFD("NUM")
    q1 = afd.novo_estado()
    q2 = afd.novo_estado()
    q3 = afd.novo_estado()
    afd.transicao(afd.inicial, DIGITOS, q1)
    afd.transicao(q1, DIGITOS, q1)
    afd.marcar_final(q1)
    afd.transicao(q1, ".", q2)
    afd.transicao(q2, DIGITOS, q3)
    afd.transicao(q3, DIGITOS, q3)
    afd.marcar_final(q3)
    return afd


def afd_char() -> AFD:
    """CHAR: '"' ~[" \\r\\n] '"'   (exatamente 1 caractere entre aspas).
    Atenção: o conjunto excluído da gramática inclui o ESPAÇO."""
    afd = AFD("CHAR")
    q1, q2, q3 = afd.novo_estado(), afd.novo_estado(), afd.novo_estado()
    afd.transicao(afd.inicial, '"', q1)
    afd.transicao_padrao(q1, q2, exceto='" \r\n')
    afd.transicao(q2, '"', q3)
    afd.marcar_final(q3)
    return afd


def afd_string() -> AFD:
    """STRING: '"' ~["\\r\\n]* '"'."""
    afd = AFD("STRING")
    q1, q2 = afd.novo_estado(), afd.novo_estado()
    afd.transicao(afd.inicial, '"', q1)
    afd.transicao_padrao(q1, q1, exceto='"\r\n')
    afd.transicao(q1, '"', q2)
    afd.marcar_final(q2)
    return afd


def afd_string_aberta() -> AFD:
    """Detector de erro: '"' ~["\\r\\n]*  (sem aspa de fechamento).
    Perde para STRING/CHAR quando a aspa existe (elas são mais longas)."""
    afd = AFD("STRING_ABERTA")
    q1 = afd.novo_estado()
    afd.transicao(afd.inicial, '"', q1)
    afd.transicao_padrao(q1, q1, exceto='"\r\n')
    afd.marcar_final(q1)
    return afd


def afd_comentario_linha() -> AFD:
    """LINE_COMMENT: '//' ~[\\r\\n]*   (não consome a quebra de linha)."""
    afd = AFD("LINE_COMMENT")
    q1, q2 = afd.novo_estado(), afd.novo_estado()
    afd.transicao(afd.inicial, "/", q1)
    afd.transicao(q1, "/", q2)
    afd.transicao_padrao(q2, q2, exceto="\r\n")
    afd.marcar_final(q2)
    return afd


def afd_comentario_bloco() -> AFD:
    """BLOCK_COMMENT: '/*' .*? '*/'  (não guloso: termina no 1º '*/').

        q0 -/-> q1 -*-> S --*--> T --/--> F(final)
                        ^ outro  | *(fica em T)
                        +--outro-+
    S = dentro do comentário; T = acabou de ver '*' (pode fechar).
    """
    afd = AFD("BLOCK_COMMENT")
    q1, s, t, f = (afd.novo_estado() for _ in range(4))
    afd.transicao(afd.inicial, "/", q1)
    afd.transicao(q1, "*", s)
    afd.transicao(s, "*", t)
    afd.transicao_padrao(s, s, exceto="*")
    afd.transicao(t, "*", t)
    afd.transicao(t, "/", f)
    afd.transicao_padrao(t, s, exceto="*/")
    afd.marcar_final(f)
    return afd


def afd_comentario_bloco_aberto() -> AFD:
    """Detector de erro: '/*' seguido de qualquer coisa SEM conter '*/'.
    É o autômato acima sem o estado F e com S e T finais: se existir o
    '*/', BLOCK_COMMENT é mais longo e vence; senão este consome até o EOF."""
    afd = AFD("BLOCK_ABERTO")
    q1, s, t = afd.novo_estado(), afd.novo_estado(), afd.novo_estado()
    afd.transicao(afd.inicial, "/", q1)
    afd.transicao(q1, "*", s)
    afd.transicao(s, "*", t)
    afd.transicao_padrao(s, s, exceto="*")
    afd.transicao(t, "*", t)
    afd.transicao_padrao(t, s, exceto="*/")
    afd.marcar_final(s)
    afd.marcar_final(t)
    return afd


# =====================================================================
# 6. LEXER
# =====================================================================

class Lexer:
    def __init__(self, entrada: str, regras: list[tuple[str, AFD]]):
        self.entrada = entrada
        self.regras = regras
        self.pos = 0
        self.linha = 1
        self.coluna = 1

    def _avancar(self, n: int) -> None:
        for _ in range(n):
            if self.pos >= len(self.entrada):
                return
            if self.entrada[self.pos] == "\n":
                self.linha += 1
                self.coluna = 1
            else:
                self.coluna += 1
            self.pos += 1

    def _reclassificar(self, tipo: str, valor: str) -> str:
        """Refina o tipo bruto usando a CONFIGURAÇÃO:
          - ID   -> palavra reservada, se aplicável
          - NUM  -> REAL (tem '.') ou INT
          - FIXO -> operador ou delimitador específico
        """
        if tipo == "ID" and valor in PALAVRAS_RESERVADAS:
            return PALAVRAS_RESERVADAS[valor]
        if tipo == "NUM":
            return "REAL" if "." in valor else "INT"
        if tipo == "FIXO":
            return FIXOS[valor]
        return tipo

    def proximo_token(self) -> Token | None:
        while True:
            # 1) pular espaços em branco (atualizando linha/coluna)
            while self.pos < len(self.entrada) and self.entrada[self.pos] in " \t\r\n":
                self._avancar(1)
            if self.pos >= len(self.entrada):
                return None

            linha, coluna = self.linha, self.coluna
            resto = self.entrada[self.pos:]

            # 2) maximal munch; empate => vence a regra listada primeiro
            melhor_tipo: str | None = None
            melhor_tam = 0
            for tipo, afd in self.regras:
                tam = afd.maior_prefixo(resto)
                if tam > melhor_tam:
                    melhor_tam = tam
                    melhor_tipo = tipo

            if melhor_tam == 0:
                raise SyntaxError(
                    f"Caractere inesperado {resto[0]!r} em L{linha}:C{coluna}"
                )

            # 2b) AFDs detectores de erro
            if melhor_tipo in ERROS_LEXICOS:
                raise SyntaxError(
                    f"{ERROS_LEXICOS[melhor_tipo]}: {resto[:melhor_tam]!r} "
                    f"em L{linha}:C{coluna}"
                )

            valor = resto[:melhor_tam]
            self._avancar(melhor_tam)

            # 2c) comentários: consumidos, mas não geram token
            if melhor_tipo in COMENTARIOS_IGNORADOS:
                continue

            # 3) reclassificação
            melhor_tipo = self._reclassificar(melhor_tipo, valor)
            return Token(melhor_tipo, valor, linha, coluna)

    def tokenizar(self) -> list[Token]:
        """TODO 9: chama proximo_token() até acabar a entrada."""
        tokens: list[Token] = []
        while True:
            tok = self.proximo_token()
            if tok is None:
                break
            tokens.append(tok)
        return tokens


# =====================================================================
# 7. PROGRAMA PRINCIPAL
# =====================================================================

def construir_regras() -> list[tuple[str, AFD]]:
    """Monta a lista de regras. A ORDEM define o desempate:
    CHAR vem antes de STRING (como na gramática)."""
    return [
        ("ID",            afd_identificador()),
        ("NUM",           afd_numero()),
        ("FIXO",          afd_conjunto_literais("FIXO", sorted(FIXOS))),
        ("CHAR",          afd_char()),
        ("STRING",        afd_string()),
        ("LINE_COMMENT",  afd_comentario_linha()),
        ("BLOCK_COMMENT", afd_comentario_bloco()),
        ("STRING_ABERTA", afd_string_aberta()),
        ("BLOCK_ABERTO",  afd_comentario_bloco_aberto()),
    ]


def gravar_tokens_tsv(tokens: list[Token], caminho: str) -> None:
    """Grava os tokens no formato de intercâmbio com o ANTLR.

    Uma linha por token, 4 colunas separadas por TAB:
        TIPO <TAB> LINHA <TAB> COLUNA <TAB> TEXTO_EM_BASE64(UTF-8)

    * TIPO é o nome do token na gramática (ex.: TP_INT, ID, OP_GE).
    * LINHA e COLUNA são 1-based (como no resto deste lexer).
    * O texto vai em Base64 para que TAB, quebra de linha ou aspas dentro
      do lexema não quebrem o formato (comentários não aparecem: são
      descartados). O token EOF NÃO é gravado; o leitor o acrescenta.
    """
    with open(caminho, "w", encoding="utf-8", newline="\n") as f:
        for tok in tokens:
            texto_b64 = base64.b64encode(tok.valor.encode("utf-8")).decode("ascii")
            f.write(f"{tok.tipo}\t{tok.linha}\t{tok.coluna}\t{texto_b64}\n")


def main() -> None:
    if len(sys.argv) > 1:
        with open(sys.argv[1], "r", encoding="utf-8") as f:
            codigo = f.read()
    else:
        codigo = ""
    saida = sys.argv[2] if len(sys.argv) > 2 else "tokens.tsv"

    try:
        tokens = Lexer(codigo, construir_regras()).tokenizar()
    except SyntaxError as e:
        # Em caso de erro léxico nenhum arquivo é gravado.
        print(f"Erro léxico: {e}")
        sys.exit(1)

    print(f"{'TEXTO':<14} {'TOKEN':<14} {'POSIÇÃO':<8}")
    print("-" * 38)
    for tok in tokens:
        print(f"{tok.valor:<14} {tok.tipo:<14} {tok.linha}:{tok.coluna}")

    gravar_tokens_tsv(tokens, saida)
    print(f"\n{len(tokens)} tokens gravados em {saida}")


if __name__ == "__main__":
    main()