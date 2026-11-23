grammar Assis;

// ============================================================================
// GRAMÁTICA DA LINGUAGEM ASSIS — referência das TRÊS fases do front-end
//
//  ANÁLISE LÉXICA     regras com nome em MAIÚSCULAS (parte final deste arquivo).
//                     Definem os tokens. Implementadas à mão em lexer_aluno.py
//                     (o ANTLR também gera um AssisLexer, mas o projeto usa o nosso).
//  ANÁLISE SINTÁTICA  regras com nome em minúsculas (parte inicial). Definem a
//                     ESTRUTURA válida de um programa. O ANTLR gera AssisParser.py
//                     a partir delas.
//  ANÁLISE SEMÂNTICA  não está escrita na gramática: é feita pelo visitor
//                     (MeuVisitorCustomizado.py), que percorre a árvore gerada
//                     por estas regras. Os rótulos `# nome` nas alternativas
//                     viram métodos visitNome() no visitor.
// ============================================================================

// =========================
// REGRAS DO ANALISADOR SINTATICO
// (FASE 2: o parser confere se a sequência de tokens tem forma válida)
// =========================

// Regra inicial: um programa é uma sequência de comandos até o fim do arquivo.
program
    : statement* EOF
    ;

// Qualquer comando que pode aparecer num programa ou dentro de um bloco { }.
statement
    : varDecl
    | ifStmt
    | block
    | exprStmt
    | functionDecl
    | whileStatement
    | returnStmt
    ;

// Declaração de função:  funct int soma(int a, int b) { ... }
functionDecl
    : FUNC type ID PAR_ESQ paramList? PAR_DIR block
    ;

paramList
    : param (VIRGULA param)*
    ;

param
    : type ID
    ;

// Retorno:  redire a + b;
returnStmt
    : RETURN expr PONTO_VIRGULA
    ;

// Declaração de variável (sempre com valor inicial):  int x = 10;
varDecl
    : type ID ATRIB expr PONTO_VIRGULA
    ;

// Repetição:  dum (x < 10) x = x + 1;   (a condição é sempre uma comparação)
whileStatement
    : WHILE PAR_ESQ exprLog PAR_DIR statement
    ;

type
    : TP_INT
    | TP_FLOAT
    | TP_CHAR
    | TP_BOOL
    | TP_STRING
    ;

// Condicional com 'senão-se' e 'senão' opcionais:  si (...) ... alitersi (...) ... aliter ...
ifStmt
    : KW_IF PAR_ESQ exprLog PAR_DIR statement
      (KW_ELSEIF PAR_ESQ exprLog PAR_DIR statement)*
      (KW_ELSE statement)?
    ;

// Bloco { ... }: na análise semântica, cada bloco abre um novo escopo.
block
    : CHAVE_ESQ statement* CHAVE_DIR
    ;

exprStmt
    : expr PONTO_VIRGULA
    ;

// =========================
// REGRAS DE EXPRESSOES
// A ordem aninhada (expr -> exprLog/additiveExpr -> multiplicativeExpr ->
// primaryExpr) é o que dá PRECEDÊNCIA: * e / são agrupados antes de + e -,
// e as comparações são avaliadas por último.
// =========================

expr
    : ID ATRIB expr          # atribuicao
    | exprLog                # comparacao
    | additiveExpr           # expressaoAritmetica
    ;

// Comparação (resultado sempre bool): é o que se pode usar como condição.
exprLog
    : additiveExpr (OP_EQ | OP_NE | OP_LT | OP_GT | OP_LE | OP_GE) additiveExpr
    ;

// Soma e subtração (menor precedência aritmética).
additiveExpr
    : multiplicativeExpr ((OP_SOMA | OP_SUB) multiplicativeExpr)*
    ;

// Multiplicação e divisão (precedência maior que + e -).
multiplicativeExpr
    : primaryExpr ((OP_MULT | OP_DIV) primaryExpr)*
    ;

// Elementos básicos: chamadas, variáveis, literais e expressões entre ( ) ou { }.
// Na análise semântica, é daqui que o TIPO de cada expressão "nasce".
primaryExpr
    : ID PAR_ESQ (expr (VIRGULA expr)*)? PAR_DIR # chamadaFuncao
    | ID                                         # identificador
    | INT                                        # inteiroLiteral
    | REAL                                       # floatLiteral
    | CHAR                                       # charLiteral
    | STRING                                     # textoLiteral
    | TRUE                                       # trueLiteral
    | FALSE                                      # falseLiteral
    | PAR_ESQ expr PAR_DIR                       # entreParenteses
    | CHAVE_ESQ expr CHAVE_DIR                   # entreChaves
    ;

// =========================
// REGRAS DO ANALISADOR LEXICO
// (FASE 1: definem os tokens; espelhadas em lexer_aluno.py)
//
// Como o lexer escolhe o token: vence o MAIOR trecho reconhecido; em empate,
// vence a regra escrita primeiro neste arquivo. Por isso:
//   * as palavras reservadas vêm antes de ID (si/int/... não viram identificador);
//   * REAL vem antes de INT (1.75 não vira INT + PONTO + INT);
//   * CHAR vem antes de STRING ("A" é CHAR; "AB" é STRING).
// =========================

// Tipos
TP_INT    : 'int';
TP_FLOAT  : 'float';
TP_CHAR   : 'char';
TP_BOOL   : 'bool';
TP_STRING : 'String';

// Condicionais
KW_IF     : 'si';
KW_ELSE   : 'aliter';
KW_ELSEIF : 'alitersi';

// Valores booleanos
TRUE  : 'verum';
FALSE : 'falsum';

// Funcoes e retorno
FUNC   : 'funct';
RETURN : 'redire';

// Repeticao
WHILE : 'dum';

// Identificadores e literais numericos
REAL : [0-9]+ '.' [0-9]+;
INT  : [0-9]+;
ID   : [a-zA-Z_][a-zA-Z_0-9]*;

// Literais de caracteres e texto
CHAR   : '"' ~[" \r\n] '"';
STRING : '"' ~["\r\n]* '"';

// Atribuicao
ATRIB : '=';

// Operadores aritmeticos
OP_SOMA : '+';
OP_SUB  : '-';
OP_MULT : '*';
OP_DIV  : '/';

// Operadores relacionais
OP_LE : '<=';
OP_GE : '>=';
OP_EQ : '==';
OP_NE : '!=';
OP_LT : '<';
OP_GT : '>';

// Delimitadores
PAR_ESQ       : '(';
PAR_DIR       : ')';
CHAVE_ESQ     : '{';
CHAVE_DIR     : '}';
VIRGULA       : ',';
PONTO_VIRGULA : ';';
PONTO         : '.';

// Comentarios (-> skip: são consumidos e NÃO geram token)
LINE_COMMENT  : '//' ~[\r\n]* -> skip;
BLOCK_COMMENT : '/*' .*? '*/' -> skip;

// Espacos em branco (-> skip: não geram token, mas contam para linha/coluna)
WS : [ \t\r\n]+ -> skip;