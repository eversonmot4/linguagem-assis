# Linguagem Assis

A Assis é uma linguagem de programação inspirada em C, com palavras reservadas em latim (si, aliter, dum, funct, redire). Este projeto implementa seu front-end de compilador em Python: um analisador léxico baseado em autômatos finitos determinísticos com a regra do maior prefixo, que grava os tokens em tokens.tsv; um parser gerado pelo ANTLR a partir de Assis.g4, alimentado por esses tokens; e um visitor de análise semântica com tabela de símbolos e escopos, que produz um relatório com a árvore sintática, a tabela e os erros encontrados.

## Requisitos:
```
pip install -r requirements.txt
```

## Gerar o parser em Python:
```
java -jar antlr-4.13.2-complete.jar -Dlanguage=Python3 -visitor Assis.g4
```

## Alternativa caso não funcione pra gerar o parser, usar máquina virtual:
```
python -m venv .venv
source .venv/bin/activate
python -m pip install -r requirements.txt
```

## Executar:
```
# 1. lexer próprio -> tokens.tsv
python lexer_aluno.py exemplo.txt

# 2. parser ANTLR + análise semântica -> relatorio_saida.txt
python main.py
```