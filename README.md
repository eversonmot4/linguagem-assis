# Linguagem Assis

## Requisitos
```
pip install -r requirements.txt
```
(Java é necessário só para rodar o jar do ANTLR.)

## Gerar o parser em Python
```
java -jar antlr-4.13.2-complete.jar -Dlanguage=Python3 -visitor Assis.g4
```

## Executar
```
# 1. lexer próprio -> tokens.tsv
python lexer_aluno.py exemplo.txt

# 2. parser ANTLR + análise semântica -> relatorio_saida.txt
python main.py
```
Teste de erros semânticos: `python lexer_aluno.py exemplo_erros.txt && python main.py`

## Testes do lexer
```
python testes_lexer.py
```