grammar Assis;

// =========================
// REGRAS DO ANALISADOR SINTATICO
// =========================

program
    : statement* EOF
    ;

statement
    : varDecl
    | ifStmt
    | block
    | exprStmt
    | functionDecl
    | whileStatement
    | returnStmt
    ;

functionDecl
    : FUNC type ID PAR_ESQ paramList? PAR_DIR block
    ;

paramList
    : param (VIRGULA param)*
    ;

param
    : type ID
    ;

returnStmt
    : RETURN expr PONTO_VIRGULA
    ;

varDecl
    : type ID ATRIB expr PONTO_VIRGULA
    ;

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

ifStmt
    : KW_IF PAR_ESQ exprLog PAR_DIR statement
      (KW_ELSEIF PAR_ESQ exprLog PAR_DIR statement)*
      (KW_ELSE statement)?
    ;

block
    : CHAVE_ESQ statement* CHAVE_DIR
    ;

exprStmt
    : expr PONTO_VIRGULA
    ;

// =========================
// REGRAS DE EXPRESSOES
// =========================

expr
    : ID ATRIB expr          # atribuicao
    | exprLog                # comparacao
    | additiveExpr           # expressaoAritmetica
    ;

exprLog
    : additiveExpr (OP_EQ | OP_NE | OP_LT | OP_GT | OP_LE | OP_GE) additiveExpr
    ;

additiveExpr
    : multiplicativeExpr ((OP_SOMA | OP_SUB) multiplicativeExpr)*
    ;

multiplicativeExpr
    : primaryExpr ((OP_MULT | OP_DIV) primaryExpr)*
    ;

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

// Comentarios
LINE_COMMENT  : '//' ~[\r\n]* -> skip;
BLOCK_COMMENT : '/*' .*? '*/' -> skip;

// Espacos em branco
WS : [ \t\r\n]+ -> skip;