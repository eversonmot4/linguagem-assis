# Linguagem Assis

- Baixar os requerimentos
        
  ```terminal
  pip install -r requirements.txt
  ```
---

- Código pra gerar os arquivos do ANTRL em .py

  ```terminal
  java -jar antlr-4.13.2-complete.jar -Dlanguage=Python3 -visitor Assis.g4

