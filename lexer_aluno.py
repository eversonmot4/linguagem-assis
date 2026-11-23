"""
LEXER DA LINGUAGEM ASSIS
FASE 1 DO COMPILADOR: ANÁLISE LÉXICA
=====================================

Visão geral do front-end do compilador (3 fases, uma alimenta a próxima):

  1. ANÁLISE LÉXICA     -> ESTE ARQUIVO (lexer_aluno.py)
        entrada: texto do programa (sequência de caracteres)
        saída:   lista de tokens  -> gravada em tokens.tsv
  2. ANÁLISE SINTÁTICA  -> Assis.g4 (gramática) + AssisParser.py (gerado) + main.py
        entrada: tokens           saída: árvore sintática
  3. ANÁLISE SEMÂNTICA  -> MeuVisitorCustomizado.py + TabelaDeSimbolos.py
        entrada: árvore           saída: tabela de símbolos e erros de tipo/escopo

O que a análise léxica faz
--------------------------
Lê o código-fonte caractere a caractere e o agrupa em "palavras com
significado" (TOKENS): palavras reservadas, identificadores, números,
literais, operadores e delimitadores. Espaços e comentários são consumidos
e descartados. Ela NÃO sabe se os tokens estão numa ordem válida (isso é
trabalho da fase sintática) nem se os tipos combinam (fase semântica);
só detecta erros "de escrita", como um caractere que não pertence à
linguagem ou uma aspa que nunca fecha.

Como é feita (arquitetura do professor)
---------------------------------------
Cada categoria de token é reconhecida por um AFD (autômato finito
determinístico) guardado como tabela de transições. O Lexer testa todos
os AFDs na posição atual e fica com o que reconhece o MAIOR trecho
(regra do maior prefixo / "maximal munch"). Palavras reservadas são
lidas como identificadores e reclassificadas depois.

Uso:
    python lexer_aluno.py exemplo.txt [saida.tsv]

Seções deste arquivo:
    1. Token
    2. AFD (tabela de transições)
    3. Configuração da linguagem (espelha o Assis.g4)
    4. Construtores genéricos (literal, trie)
    5. Construtores específicos (ID, NUM, CHAR, STRING, comentários)
    6. Lexer (motor: maior prefixo, reclassificação, erros)
    7. Programa principal (gera o tokens.tsv para a fase sintática)

Extensões feitas sobre o esqueleto do professor (por exigência da gramática):
  * AFD.transicao_padrao(): transição "por complemento" (~[...] do ANTLR),
    pois não dá para listar na tabela todos os caracteres possíveis.
  * AFDs novos: CHAR, STRING, comentário de linha, comentário de bloco e
    AFDs "detectores de erro" (string aberta, comentário de bloco aberto).
  * afd_numero() reconhece INT e REAL no mesmo autômato.
"""
from __future__ import annotations
from dataclasses import dataclass
import base64
import sys


# =====================================================================
# 1. TOKEN
# =====================================================================

# O token é o PRODUTO da análise léxica e a ENTRADA da análise sintática.
#   tipo   -> categoria, com o mesmo nome do token na gramática (TP_INT, ID, OP_GE...)
#   valor  -> lexema: o texto exato que foi lido do código ("idade", ">=", "1.75")
#   linha/coluna -> onde o token começa (contagem a partir de 1); serve para
#                   mensagens de erro léxico, sintático e semântico.
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

# Um AFD (autômato finito determinístico) é uma "máquina de estados" que lê
# caracteres um a um:
#   - tem um estado INICIAL e alguns estados FINAIS (= "até aqui já formei
#     um token válido");
#   - a TABELA DE TRANSIÇÕES diz, para cada (estado, caractere lido), qual o
#     próximo estado. Se não houver entrada na tabela, o autômato "trava";
#   - "determinístico" = para cada par (estado, caractere) existe no máximo
#     um próximo estado, então não há escolhas ambíguas.
class AFD:
    """AFD representado por tabela (estado, símbolo) -> estado.

    Extensão: `padrao` guarda, por estado, uma transição "por
    complemento": (conjunto de caracteres excluídos, destino). Ela só é
    usada quando NÃO existe transição explícita na tabela principal.
    """

    def __init__(self, nome: str):
        self.nome = nome                                  # nome do AFD (só para depuração)
        self.transicoes: dict[tuple[int, str], int] = {}  # a TABELA: (estado, char) -> estado
        self.padrao: dict[int, tuple[str, int]] = {}      # extensão: "qualquer char exceto ..."
        self.finais: set[int] = set()                     # estados que aceitam um token
        self.inicial: int = 0                             # estado onde toda leitura começa
        self._prox: int = 1                               # próximo número de estado livre (0 já é o inicial)

    def novo_estado(self) -> int:
        # Cria um estado novo, numerado em sequência (1, 2, 3, ...).
        e = self._prox
        self._prox += 1
        return e

    def transicao(self, origem: int, simbolos: str, destino: int) -> None:
        """TODO 1: para CADA caractere c em `simbolos`, registre
        transicoes[(origem, c)] = destino."""
        # Uma chamada com vários símbolos (ex.: DIGITOS) vira várias entradas na tabela.
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
        # 1º a tabela principal (transição explícita) ...
        prox = self.transicoes.get((estado, c))
        if prox is not None:
            return prox
        # 2º a transição por complemento, se o estado tiver uma e o char não estiver excluído
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
        # `ultimo` = tamanho do maior prefixo aceito visto até agora.
        # Começa em 0 se o estado inicial já for final (aceita vazio), senão -1.
        ultimo = 0 if estado in self.finais else -1
        for i, c in enumerate(texto):
            prox = self.proximo_estado(estado, c)
            if prox is None:
                break                      # sem transição: o autômato travou, para de ler
            estado = prox
            if estado in self.finais:
                ultimo = i + 1             # passou por um estado final: anota (i+1 chars lidos)
        return ultimo                      # vale o ÚLTIMO final visitado, não o primeiro


# =====================================================================
# 3. CONFIGURAÇÃO DA LINGUAGEM ASSIS
# ---------------------------------------------------------------------
# Esta seção é um espelho das regras léxicas (as de nome em MAIÚSCULAS)
# do Assis.g4. É aqui que se define QUAIS tokens existem e COMO se chamam;
# os nomes precisam ser idênticos aos da gramática, porque o parser do
# ANTLR vai localizar cada token pelo nome (ver main.py).
# =====================================================================

# --- Alfabeto de identificadores: [a-zA-Z_][a-zA-Z_0-9]* ------------
# Um identificador começa com letra ou '_' e continua com letras, dígitos ou '_'.
LETRAS_ID       = "abcdefghijklmnopqrstuvwxyzABCDEFGHIJKLMNOPQRSTUVWXYZ"
INICIAIS_ID     = LETRAS_ID + "_"
CONTINUACAO_ID  = LETRAS_ID + "0123456789_"

# --- Dígitos ---------------------------------------------------------
DIGITOS = "0123456789"

# --- Palavras reservadas: lexema -> tipo ----------------------------
# Não existe um AFD para cada palavra reservada. O lexer as lê como ID e,
# depois, consulta esta tabela (ver Lexer._reclassificar). Assim 'si' vira
# KW_IF, mas 'sii' continua sendo um ID comum.
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
        prox = afd.novo_estado()        # um estado novo para cada caractere do texto
        afd.transicao(atual, c, prox)   # lendo `c` no estado atual, avança para o novo
        atual = prox
    afd.marcar_final(atual)             # só o último estado (texto completo) aceita
    return afd


def afd_conjunto_literais(nome: str, textos: list[str]) -> AFD:
    """AFD (trie) que reconhece QUALQUER uma das strings, compartilhando
    estados de prefixos comuns ("=" e "==" dividem o 1º estado)."""
    afd = AFD(nome)
    for texto in textos:
        atual = afd.inicial             # cada texto é inserido a partir da raiz do trie
        for c in texto:
            prox = afd.transicoes.get((atual, c))
            if prox is None:            # caminho ainda não existe: cria o estado
                prox = afd.novo_estado()
                afd.transicao(atual, c, prox)
            atual = prox                # se já existia, reaproveita (prefixo compartilhado)
        afd.marcar_final(atual)         # o nó onde o texto termina aceita (ex.: '=' e '==')
    return afd


# =====================================================================
# 5. CONSTRUTORES ESPECÍFICOS
# Um construtor por regra léxica 'não fixa' do Assis.g4 (ID, INT/REAL, CHAR,
# STRING, comentários). Os "detectores de erro" só existem para que erros
# léxicos (aspas ou /* sem fechar) sejam reconhecidos por um AFD, como o resto.
# =====================================================================

def afd_identificador() -> AFD:
    """[a-zA-Z_][a-zA-Z_0-9]* -> tipo bruto ID."""
    afd = AFD("ID")
    q1 = afd.novo_estado()
    afd.transicao(afd.inicial, INICIAIS_ID, q1)  # 1º caractere: letra ou '_'
    afd.transicao(q1, CONTINUACAO_ID, q1)        # demais: letra, dígito ou '_' (laço em q1)
    afd.marcar_final(q1)                         # qualquer comprimento >= 1 é aceito
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

# O Lexer é o "motor": percorre o código-fonte e, a cada passo, decide qual
# é o próximo token. Guarda a posição atual (pos) e também linha/coluna, que
# acompanham a leitura para que cada token saiba onde começou.
class Lexer:
    def __init__(self, entrada: str, regras: list[tuple[str, AFD]]):
        self.entrada = entrada
        self.regras = regras
        self.pos = 0
        self.linha = 1
        self.coluna = 1

    def _avancar(self, n: int) -> None:
        # Anda `n` caracteres, mantendo linha/coluna atualizadas:
        # '\n' zera a coluna e soma uma linha; qualquer outro caractere soma uma coluna.
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
            # 1) pular espaços em branco (atualizando linha/coluna).
            #    Espaços, tabs e quebras não geram token, mas contam para a posição.
            while self.pos < len(self.entrada) and self.entrada[self.pos] in " \t\r\n":
                self._avancar(1)
            if self.pos >= len(self.entrada):
                return None

            linha, coluna = self.linha, self.coluna
            resto = self.entrada[self.pos:]

            # 2) maximal munch: TODOS os AFDs tentam reconhecer um prefixo de `resto`;
            #    vence o que reconhecer mais caracteres. Em empate (mesmo tamanho),
            #    vence a regra que aparece primeiro em construir_regras()
            #    (é o que faz "A" ser CHAR e não STRING, como na gramática).
            melhor_tipo: str | None = None
            melhor_tam = 0
            for tipo, afd in self.regras:
                tam = afd.maior_prefixo(resto)
                if tam > melhor_tam:
                    melhor_tam = tam
                    melhor_tipo = tipo

            # Nenhum AFD reconheceu nada: o caractere não pertence à linguagem.
            # ERRO LÉXICO: informa o caractere e sua posição.
            if melhor_tam == 0:
                raise SyntaxError(
                    f"Caractere inesperado {resto[0]!r} em L{linha}:C{coluna}"
                )

            # 2b) AFDs detectores de erro: se um deles venceu, o programa tem uma
            #     aspa ou um '/*' sem fechamento -> ERRO LÉXICO com a posição de início.
            if melhor_tipo in ERROS_LEXICOS:
                raise SyntaxError(
                    f"{ERROS_LEXICOS[melhor_tipo]}: {resto[:melhor_tam]!r} "
                    f"em L{linha}:C{coluna}"
                )

            valor = resto[:melhor_tam]
            self._avancar(melhor_tam)

            # 2c) comentários: o texto é consumido (e linha/coluna avançam),
            #     mas nenhum token é devolvido; o laço recomeça no próximo trecho.
            if melhor_tipo in COMENTARIOS_IGNORADOS:
                continue

            # 3) reclassificação: refina o tipo bruto (ID -> palavra reservada,
            #    NUM -> INT/REAL, FIXO -> operador ou delimitador específico).
            melhor_tipo = self._reclassificar(melhor_tipo, valor)
            return Token(melhor_tipo, valor, linha, coluna)

    def tokenizar(self) -> list[Token]:
        """TODO 9: chama proximo_token() até acabar a entrada."""
        # Pede tokens um a um até a entrada acabar (None). Se houver erro léxico,
        # o SyntaxError sobe daqui e nenhum token é entregue à fase sintática.
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

# A lista de regras define quais AFDs competem na regra do maior prefixo.
# ATENÇÃO À ORDEM: ela desempata (CHAR antes de STRING, como no Assis.g4).
def construir_regras() -> list[tuple[str, AFD]]:
    """Monta a lista de regras. A ORDEM define o desempate:
    CHAR vem antes de STRING (como na gramática)."""
    return [
        ("ID",            afd_identificador()),
        ("NUM",           afd_numero()),
        ("FIXO",          afd_conjunto_literais("FIXO", sorted(FIXOS))),  # operadores + delimitadores (trie)
        ("CHAR",          afd_char()),
        ("STRING",        afd_string()),
        ("LINE_COMMENT",  afd_comentario_linha()),
        ("BLOCK_COMMENT", afd_comentario_bloco()),
        ("STRING_ABERTA", afd_string_aberta()),
        ("BLOCK_ABERTO",  afd_comentario_bloco_aberto()),
    ]


# PONTE ENTRE AS FASES 1 E 2: o lexer não chama o parser diretamente; ele
# grava os tokens em um arquivo e o main.py os lê depois (ver main.py).
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
            # Base64 evita que TAB, quebra de linha ou aspas dentro do lexema quebrem o TSV.
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
        # Em caso de erro léxico nenhum arquivo é gravado (a fase sintática nem começa).
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