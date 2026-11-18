# Linguagem Assis

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