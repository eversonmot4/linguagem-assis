/*
 * Analisador lexico da Linguagem Assis (MiniC.g4).
 *
 * Uso:
 *   gcc -std=c11 -Wall -Wextra -pedantic lexer_assis.c -o lexer_assis
 *   ./lexer_assis teste.txt
 *   ./lexer_assis teste.txt tokens_saida.txt
 *
 * O programa grava uma sequencia de NOMES de tokens, separados por espaco,
 * no arquivo tokens_saida.txt (ou no caminho passado como segundo argumento).
 * Nao imprime uma tabela de lexemas. Comentarios e espacos sao ignorados.
 *
 * Esta implementacao reproduz as regras lexicas do MiniC.g4 fornecido,
 * inclusive a ordem de prioridade, o maior prefixo e os comandos -> skip.
 * Regras do parser (statement, expr, exprLog...) nao sao tokens.
 * A sequencia textual nao substitui um TokenStream real do ANTLR.
 */

#include <stdbool.h>
#include <stdio.h>
#include <stdlib.h>
#include <string.h>

/* =====================================================================
 * 1. TOKEN
 * ===================================================================== */

typedef struct {
    char tipo[32];
    char valor[256];
    int linha;
    int coluna;
} Token;

/* =====================================================================
 * 2. AFD - tabela de transicoes
 * ===================================================================== */

#define MAX_ESTADOS 32
#define NUM_SIMBOLOS 256

typedef struct {
    char nome[32];
    int transicoes[MAX_ESTADOS][NUM_SIMBOLOS];
    bool finais[MAX_ESTADOS];
    int inicial;
    int prox_estado;
} AFD;

static void afd_init(AFD *afd, const char *nome) {
    snprintf(afd->nome, sizeof afd->nome, "%s", nome);
    for (int i = 0; i < MAX_ESTADOS; ++i) {
        afd->finais[i] = false;
        for (int j = 0; j < NUM_SIMBOLOS; ++j)
            afd->transicoes[i][j] = -1;
    }
    afd->inicial = 0;
    afd->prox_estado = 1;
}

static int afd_novo_estado(AFD *afd) {
    if (afd->prox_estado >= MAX_ESTADOS) {
        fprintf(stderr, "AFD '%s' excedeu MAX_ESTADOS=%d\n", afd->nome,
                MAX_ESTADOS);
        exit(EXIT_FAILURE);
    }
    return afd->prox_estado++;
}

static void afd_transicao(AFD *afd, int origem, const char *simbolos,
                          int destino) {
    for (const unsigned char *p = (const unsigned char *)simbolos; *p; ++p)
        afd->transicoes[origem][*p] = destino;
}

static void afd_marcar_final(AFD *afd, int estado) {
    afd->finais[estado] = true;
}

static int afd_maior_prefixo(const AFD *afd, const char *texto) {
    int estado = afd->inicial;
    int ultimo = afd->finais[estado] ? 0 : -1;

    for (int i = 0; texto[i] != '\0'; ++i) {
        unsigned char c = (unsigned char)texto[i];
        int prox = afd->transicoes[estado][c];
        if (prox < 0)
            break;
        estado = prox;
        if (afd->finais[estado])
            ultimo = i + 1;
    }
    return ultimo;
}

/* =====================================================================
 * 3. CONFIGURACAO LEXICA DO MiniC.g4
 * ===================================================================== */

#define LETRAS_ID "abcdefghijklmnopqrstuvwxyzABCDEFGHIJKLMNOPQRSTUVWXYZ"
#define INICIAIS_ID LETRAS_ID "_"
#define CONTINUACAO_ID LETRAS_ID "0123456789_"
#define DIGITOS "0123456789"

typedef struct {
    const char *lexema;
    const char *tipo;
} Entrada;

/* A regra ID vem depois das palavras-chave no .g4. Em empates de
 * comprimento, identificadores iguais a palavras-chave sao reclassificados.
 */
static const Entrada PALAVRAS_RESERVADAS[] = {
    {"int", "TP_INT"},       {"float", "TP_FLOAT"},
    {"char", "TP_CHAR"},     {"bool", "TP_BOOL"},
    {"String", "TP_STRING"}, {"si", "KW_IF"},
    {"aliter", "KW_ELSE"},   {"alitersi", "KW_ELSEIF"},
    {"verum", "TRUE"},      {"falsum", "FALSE"},
    {"funct", "FUNC"},      {"redire", "RETURN"},
    {"dum", "WHILE"},
    {NULL, NULL}
};

/* A ordem reflete o lexer do .g4: a primeira regra vence um empate.
 * ASPAS_DUP_DIR e ASPAS_DUP_ESQ reconhecem o mesmo lexema, por isso a
 * primeira regra (ASPAS_DUP_ESQ) vence, como ocorreria no ANTLR.
 * Os marcadores de comentario sao tokens normais no .g4 fornecido.
 */
static const Entrada FIXOS[] = {
    {"=", "ATRIB"},
    {"+", "OP_SOMA"}, {"-", "OP_SUB"},
    {"*", "OP_MULT"}, {"/", "OP_DIV"},
    {"<=", "OP_LE"}, {">=", "OP_GE"},
    {"==", "OP_EQ"}, {"!=", "OP_NE"},
    {"<", "OP_LT"}, {">", "OP_GT"},
    {"(", "PAR_ESQ"}, {")", "PAR_DIR"},
    {"{", "CHAVE_ESQ"}, {"}", "CHAVE_DIR"},
    {",", "VIRGULA"}, {";", "PONTO_VIRGULA"},
    {".", "PONTO"},
    {"\"", "ASPAS_DUP_ESQ"},
    {"\"", "ASPAS_DUP_DIR"},
    {"//", "INI_LINE_COMMENT"},
    {"/*", "INI_BLOCK_COMMENT"},
    {"*/", "FIM_BLOCK_COMMENT"},
    {NULL, NULL}
};

/* =====================================================================
 * 4. CONSTRUTORES DE AFD
 * ===================================================================== */

static void afd_conjunto_literais(AFD *afd, const char *nome,
                                 const Entrada *ents) {
    afd_init(afd, nome);
    for (int i = 0; ents[i].lexema != NULL; ++i) {
        int atual = afd->inicial;
        for (const unsigned char *p = (const unsigned char *)ents[i].lexema;
             *p; ++p) {
            int prox = afd->transicoes[atual][*p];
            if (prox < 0) {
                prox = afd_novo_estado(afd);
                char simbolo[2] = {(char)*p, '\0'};
                afd_transicao(afd, atual, simbolo, prox);
            }
            atual = prox;
        }
        afd_marcar_final(afd, atual);
    }
}

static void afd_identificador(AFD *afd) {
    afd_init(afd, "ID");
    int q1 = afd_novo_estado(afd);
    afd_transicao(afd, afd->inicial, INICIAIS_ID, q1);
    afd_transicao(afd, q1, CONTINUACAO_ID, q1);
    afd_marcar_final(afd, q1);
}

/* INT : [0-9]+ ; */
static void afd_inteiro(AFD *afd) {
    afd_init(afd, "INT");
    int q1 = afd_novo_estado(afd);
    afd_transicao(afd, afd->inicial, DIGITOS, q1);
    afd_transicao(afd, q1, DIGITOS, q1);
    afd_marcar_final(afd, q1);
}

/* REAL : [0-9]+ PONTO [0-9]+ ; */
static void afd_real(AFD *afd) {
    afd_init(afd, "REAL");
    int inteiros = afd_novo_estado(afd);
    int ponto = afd_novo_estado(afd);
    int decimais = afd_novo_estado(afd);

    afd_transicao(afd, afd->inicial, DIGITOS, inteiros);
    afd_transicao(afd, inteiros, DIGITOS, inteiros);
    afd_transicao(afd, inteiros, ".", ponto);
    afd_transicao(afd, ponto, DIGITOS, decimais);
    afd_transicao(afd, decimais, DIGITOS, decimais);
    afd_marcar_final(afd, decimais);
}

/* LINE_COMMENT : '//' ~[\r\n]* -> skip ; */
static void afd_comentario_linha(AFD *afd) {
    afd_init(afd, "LINE_COMMENT");
    int barra = afd_novo_estado(afd);
    int corpo = afd_novo_estado(afd);
    afd_transicao(afd, afd->inicial, "/", barra);
    afd_transicao(afd, barra, "/", corpo);
    for (int c = 1; c < NUM_SIMBOLOS; ++c) {
        if (c != '\n' && c != '\r')
            afd->transicoes[corpo][c] = corpo;
    }
    afd_marcar_final(afd, corpo);
}

/* BLOCK_COMMENT: inicia com barra-asterisco, termina com
 * asterisco-barra. O AFD para no primeiro terminador.
 */
static void afd_comentario_bloco(AFD *afd) {
    afd_init(afd, "BLOCK_COMMENT");
    int barra = afd_novo_estado(afd);
    int corpo = afd_novo_estado(afd);
    int estrela = afd_novo_estado(afd);
    int fim = afd_novo_estado(afd);

    afd_transicao(afd, afd->inicial, "/", barra);
    afd_transicao(afd, barra, "*", corpo);
    for (int c = 1; c < NUM_SIMBOLOS; ++c) {
        if (c != '*')
            afd->transicoes[corpo][c] = corpo;
    }
    afd_transicao(afd, corpo, "*", estrela);
    for (int c = 1; c < NUM_SIMBOLOS; ++c) {
        if (c == '*')
            afd->transicoes[estrela][c] = estrela;
        else if (c == '/')
            afd->transicoes[estrela][c] = fim;
        else
            afd->transicoes[estrela][c] = corpo;
    }
    afd_marcar_final(afd, fim);
}

/* =====================================================================
 * 5. REGEX DE CHAR E STRING (suporte a caracteres UTF-8)
 * ===================================================================== */

/* O .g4 usa [^” ]: proibe a aspa CURVA U+201D e o espaco ASCII,
 * nao a aspa ASCII '"'. Para nao alterar a especificacao do usuario,
 * estas duas regras usam a leitura de caracteres UTF-8. As demais
 * regras continuam implementadas com AFDs, como no codigo original.
 */
static int ler_caractere_utf8(const char *s, unsigned int *codigo) {
    const unsigned char *p = (const unsigned char *)s;
    unsigned char a = p[0];
    if (a == '\0')
        return 0;
    if (a < 0x80) {
        *codigo = a;
        return 1;
    }
    int n = 0;
    unsigned int cp = 0;
    unsigned int minimo = 0;
    if (a >= 0xC2 && a <= 0xDF) {
        n = 2; cp = a & 0x1F; minimo = 0x80;
    } else if (a >= 0xE0 && a <= 0xEF) {
        n = 3; cp = a & 0x0F; minimo = 0x800;
    } else if (a >= 0xF0 && a <= 0xF4) {
        n = 4; cp = a & 0x07; minimo = 0x10000;
    } else {
        *codigo = a;
        return 1;
    }
    for (int i = 1; i < n; ++i) {
        if (p[i] == 0 || (p[i] & 0xC0) != 0x80) {
            *codigo = a;
            return 1;
        }
        cp = (cp << 6) | (p[i] & 0x3F);
    }
    if (cp < minimo || cp > 0x10FFFF || (cp >= 0xD800 && cp <= 0xDFFF)) {
        *codigo = a;
        return 1;
    }
    *codigo = cp;
    return n;
}

/* CHAR : '"' [^” ] '"' ; */
static int maior_prefixo_char(const char *texto) {
    if (texto[0] != '"')
        return -1;
    unsigned int cp = 0;
    int n = ler_caractere_utf8(texto + 1, &cp);
    if (n <= 0 || cp == ' ' || cp == 0x201D)
        return -1;
    return texto[1 + n] == '"' ? n + 2 : -1;
}

/* STRING : '"' [^” ]* '"' ;
 * Inclui o maior prefixo (inclusive se ele cruzar outras aspas ASCII).
 */
static int maior_prefixo_string(const char *texto) {
    if (texto[0] != '"')
        return -1;
    int pos = 1;
    int ultimo = -1;
    while (texto[pos] != '\0') {
        unsigned int cp = 0;
        int n = ler_caractere_utf8(texto + pos, &cp);
        if (n <= 0 || cp == ' ' || cp == 0x201D)
            break;
        if (cp == '"')
            ultimo = pos + n;
        pos += n;
    }
    return ultimo;
}

/* =====================================================================
 * 6. RECLASSIFICACAO
 * ===================================================================== */

static const char *reclassificar(const char *tipo, const char *valor) {
    const Entrada *tabela = NULL;
    if (strcmp(tipo, "ID") == 0)
        tabela = PALAVRAS_RESERVADAS;
    else if (strcmp(tipo, "FIXO") == 0)
        tabela = FIXOS;

    if (tabela != NULL) {
        for (int i = 0; tabela[i].lexema != NULL; ++i) {
            if (strcmp(tabela[i].lexema, valor) == 0)
                return tabela[i].tipo;
        }
    }
    return tipo;
}

/* =====================================================================
 * 7. LEXER
 * ===================================================================== */

#define MAX_REGRAS 8

typedef enum {
    REGRA_AFD,
    REGRA_CHAR,
    REGRA_STRING
} TipoRegra;

typedef struct {
    AFD afd;
    const char *tipo;
    TipoRegra modo;
    bool ignorar;
} Regra;

typedef struct {
    const char *entrada;
    size_t pos;
    int linha;
    int coluna;
    Regra regras[MAX_REGRAS];
    int n_regras;
} Lexer;

static void lexer_init(Lexer *lx, const char *entrada) {
    lx->entrada = entrada;
    lx->pos = 0;
    lx->linha = 1;
    lx->coluna = 1;
    lx->n_regras = 0;
}

static void lexer_add_regra(Lexer *lx, const char *tipo, const AFD *afd,
                             TipoRegra modo, bool ignorar) {
    if (lx->n_regras >= MAX_REGRAS) {
        fprintf(stderr, "Numero maximo de regras excedido.\n");
        exit(EXIT_FAILURE);
    }
    Regra *regra = &lx->regras[lx->n_regras++];
    if (afd != NULL)
        regra->afd = *afd;
    regra->tipo = tipo;
    regra->modo = modo;
    regra->ignorar = ignorar;
}

static void lexer_avancar(Lexer *lx, int n) {
    for (int i = 0; i < n; ++i) {
        unsigned char c = (unsigned char)lx->entrada[lx->pos];
        if (c == '\0')
            return;
        if (c == '\n') {
            ++lx->linha;
            lx->coluna = 1;
        } else if ((c & 0xC0) != 0x80) {
            ++lx->coluna;
        }
        ++lx->pos;
    }
}

/* Retorna false em EOF e true quando houver um token visivel. */
static bool lexer_proximo(Lexer *lx, Token *out) {
    for (;;) {
        /* WS : [ \t\r\n]+ -> skip ; */
        while (lx->entrada[lx->pos] == ' ' ||
               lx->entrada[lx->pos] == '\t' ||
               lx->entrada[lx->pos] == '\r' ||
               lx->entrada[lx->pos] == '\n')
            lexer_avancar(lx, 1);

        if (lx->entrada[lx->pos] == '\0')
            return false;

        int linha = lx->linha;
        int coluna = lx->coluna;
        const char *resto = lx->entrada + lx->pos;
        int melhor_tam = 0;
        const Regra *melhor = NULL;

        /* Maior prefixo; em empate, vence a regra adicionada primeiro. */
        for (int i = 0; i < lx->n_regras; ++i) {
            const Regra *r = &lx->regras[i];
            int tam = -1;
            if (r->modo == REGRA_AFD)
                tam = afd_maior_prefixo(&r->afd, resto);
            else if (r->modo == REGRA_CHAR)
                tam = maior_prefixo_char(resto);
            else if (r->modo == REGRA_STRING)
                tam = maior_prefixo_string(resto);
            if (tam > melhor_tam) {
                melhor_tam = tam;
                melhor = r;
            }
        }

        if (melhor == NULL || melhor_tam <= 0) {
            unsigned char c = (unsigned char)resto[0];
            fprintf(stderr,
                    "Erro lexico: byte 0x%02X inesperado em L%d:C%d\n",
                    (unsigned int)c, linha, coluna);
            exit(EXIT_FAILURE);
        }

        /* Comentarios completos seguem -> skip e nao viram tokens. */
        if (melhor->ignorar) {
            lexer_avancar(lx, melhor_tam);
            continue;
        }

        if ((size_t)melhor_tam >= sizeof out->valor) {
            fprintf(stderr, "Token muito longo em L%d:C%d\n", linha, coluna);
            exit(EXIT_FAILURE);
        }

        memcpy(out->valor, resto, (size_t)melhor_tam);
        out->valor[melhor_tam] = '\0';
        out->linha = linha;
        out->coluna = coluna;
        const char *tipo = reclassificar(melhor->tipo, out->valor);
        snprintf(out->tipo, sizeof out->tipo, "%s", tipo);
        lexer_avancar(lx, melhor_tam);
        return true;
    }
}

/* =====================================================================
 * 8. CONSTRUCAO DAS REGRAS NA ORDEM DE PRIORIDADE DO .g4
 * ===================================================================== */

static void construir_regras(Lexer *lx) {
    AFD afd;

    /* Tokens fixos declarados antes de CHAR/STRING e comentarios. */
    afd_conjunto_literais(&afd, "FIXO", FIXOS);
    lexer_add_regra(lx, "FIXO", &afd, REGRA_AFD, false);

    /* CHAR vem antes de STRING no MiniC.g4, portanto ganha empates. */
    lexer_add_regra(lx, "CHAR", NULL, REGRA_CHAR, false);
    lexer_add_regra(lx, "STRING", NULL, REGRA_STRING, false);

    afd_comentario_linha(&afd);
    lexer_add_regra(lx, "LINE_COMMENT", &afd, REGRA_AFD, true);

    afd_comentario_bloco(&afd);
    lexer_add_regra(lx, "BLOCK_COMMENT", &afd, REGRA_AFD, true);

    afd_real(&afd);
    lexer_add_regra(lx, "REAL", &afd, REGRA_AFD, false);

    afd_inteiro(&afd);
    lexer_add_regra(lx, "INT", &afd, REGRA_AFD, false);

    afd_identificador(&afd);
    lexer_add_regra(lx, "ID", &afd, REGRA_AFD, false);
}

/* =====================================================================
 * 9. PROGRAMA PRINCIPAL
 * ===================================================================== */

int main(int argc, char **argv) {
    const char *arquivo_saida = "tokens_saida.txt";
    char *buffer = NULL;
    FILE *f = NULL;
    FILE *saida = NULL;
    Lexer *lx = NULL;
    int status = EXIT_FAILURE;

    if (argc < 2 || argc > 3) {
        fprintf(stderr, "Uso: %s arquivo_fonte [arquivo_tokens]\n", argv[0]);
        return EXIT_FAILURE;
    }
    if (argc == 3)
        arquivo_saida = argv[2];
    if (strcmp(argv[1], arquivo_saida) == 0) {
        fprintf(stderr, "Erro: arquivo de entrada e de saida devem ser diferentes.\n");
        return EXIT_FAILURE;
    }

    f = fopen(argv[1], "rb");
    if (f == NULL) {
        perror(argv[1]);
        goto finalizar;
    }
    if (fseek(f, 0, SEEK_END) != 0) {
        perror("fseek");
        goto finalizar;
    }
    long n = ftell(f);
    if (n < 0 || fseek(f, 0, SEEK_SET) != 0) {
        perror("ftell/fseek");
        goto finalizar;
    }
    buffer = malloc((size_t)n + 1);
    if (buffer == NULL) {
        fprintf(stderr, "Falha ao alocar memoria para o arquivo.\n");
        goto finalizar;
    }
    size_t lidos = fread(buffer, 1, (size_t)n, f);
    if (ferror(f)) {
        perror("fread");
        goto finalizar;
    }
    buffer[lidos] = '\0';
    fclose(f);
    f = NULL;

    /* Lexer contem os AFDs e e grande; manter no heap. */
    lx = malloc(sizeof *lx);
    if (lx == NULL) {
        fprintf(stderr, "Falha ao alocar memoria para o lexer.\n");
        goto finalizar;
    }
    lexer_init(lx, buffer);
    construir_regras(lx);

    saida = fopen(arquivo_saida, "w");
    if (saida == NULL) {
        perror(arquivo_saida);
        goto finalizar;
    }

    /* Emite so os nomes dos tokens, na ordem em que aparecem no codigo.
     * Nao escreve lexemas, comentarios, brancos nem nomes de regras parser.
     */
    Token token;
    bool primeiro = true;
    while (lexer_proximo(lx, &token)) {
        if (!primeiro && fputc(' ', saida) == EOF) {
            perror("Escrita de tokens");
            goto finalizar;
        }
        if (fputs(token.tipo, saida) == EOF) {
            perror("Escrita de tokens");
            goto finalizar;
        }
        primeiro = false;
    }
    if (fputc('\n', saida) == EOF) {
        perror("Escrita da quebra de linha");
        goto finalizar;
    }
    if (fclose(saida) == EOF) {
        perror("Finalizacao de tokens");
        saida = NULL;
        goto finalizar;
    }
    saida = NULL;
    printf("Sequencia de tokens salva em: %s\n", arquivo_saida);
    status = EXIT_SUCCESS;

finalizar:
    if (saida != NULL)
        fclose(saida);
    if (f != NULL)
        fclose(f);
    free(lx);
    free(buffer);
    return status;
}
