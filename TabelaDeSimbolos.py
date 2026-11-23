"""
TabelaDeSimbolos.py — APOIO DA FASE 3 (ANÁLISE SEMÂNTICA)
==========================================================

A tabela de símbolos é a "memória" do analisador semântico: guarda tudo
o que o programa declarou (variáveis, parâmetros e funções) com o seu
TIPO e o seu ESCOPO, para que cada uso possa ser conferido contra a
declaração. É usada pelo MeuVisitorCustomizado.py:
  * ao DECLARAR (varDecl, param, functionDecl)  -> adicionar()/adicionar_funcao()
  * ao USAR (identificador, atribuição, chamada) -> get_tipo()/existe()/get_funcao()
  * ao abrir/fechar { } e corpos de função       -> entrar_escopo()/sair_escopo()

ESCOPOS: o programa é uma "pilha de gavetas". A gaveta 0 é o escopo Global.
Cada bloco ou função empilha uma gaveta nova; ao terminar, ela é descartada.
Uma busca vai da gaveta de cima (mais interna) para baixo, então uma variável
local "esconde" uma global de mesmo nome, e variáveis de blocos já fechados
deixam de existir. A declaração só conflita com nomes da MESMA gaveta.
"""
class TabelaDeSimbolos:
    def __init__(self):
        # Pilha de escopos; cada escopo é um dicionário nome -> tipo. Começa com o Global.
        self._escopos: list[dict[str, str]] = [{}]   # pilha de escopos
        # Registro permanente de tudo que foi declarado (mesmo de escopos já fechados),
        # só para imprimir a tabela no relatório final.
        self._historico: list[dict[str, str]] = []   # {nome, tipo, escopo} p/ dump
        # Assinatura de cada função: nome -> (tipo de retorno, [tipos dos parâmetros]).
        # Usada para conferir as chamadas.
        self._assinaturas: dict[str, tuple[str, list[str]]] = {}

    def entrar_escopo(self) -> None:
        # Abre um escopo novo (início de bloco ou de função).
        self._escopos.append({})

    def sair_escopo(self) -> None:
        # Fecha o escopo atual e esquece suas variáveis. O Global nunca é removido.
        if len(self._escopos) > 1:
            self._escopos.pop()

    def existe(self, nome: str) -> bool:
        """True se `nome` está visível em algum escopo."""
        # reversed(): busca do escopo mais interno para o mais externo
        return any(nome in escopo for escopo in reversed(self._escopos))

    def adicionar(self, nome: str, tipo: str, descricao: str | None = None) -> bool:
        """Declara `nome` no escopo atual. False se já existir NESTE escopo.
        `descricao` (opcional) só muda o texto exibido no dump."""
        atual = self._escopos[-1]          # só o escopo de cima conta para redeclaração
        if nome in atual:
            return False                   # já existe neste escopo
        atual[nome] = tipo
        self._historico.append({
            "nome": nome,
            "tipo": descricao or tipo,
            # Global se só existe uma gaveta; senão "Local (Nível n)", onde n = quantos
            # escopos há acima do Global (1 = dentro de uma função/bloco, 2 = bloco dentro de bloco...)
            "escopo": "Global" if len(self._escopos) == 1
                      else f"Local (Nível {len(self._escopos) - 1})",
        })
        return True

    def get_tipo(self, nome: str) -> str | None:
        """Tipo do símbolo visível mais interno, ou None se não declarado."""
        # O primeiro escopo (de dentro para fora) que tiver o nome é o que vale.
        for escopo in reversed(self._escopos):
            if nome in escopo:
                return escopo[nome]
        return None                        # não declarado em lugar nenhum

    # ---- funções ---------------------------------------------------
    # Uma função também é um símbolo (tipo 'funct'), mas precisa guardar a
    # assinatura para que cada chamada seja conferida (aridade e tipos).
    def adicionar_funcao(self, nome: str, retorno: str, params: list[str]) -> bool:
        desc = f"funct {retorno}({', '.join(params)})"
        if not self.adicionar(nome, "funct", desc):
            return False
        self._assinaturas[nome] = (retorno, params)
        return True

    def get_funcao(self, nome: str) -> tuple[str, list[str]] | None:
        """(tipo_retorno, [tipos dos parâmetros]) ou None se não for função."""
        if self.get_tipo(nome) == "funct":
            return self._assinaturas.get(nome)
        return None

    def dump(self) -> str:
        # Gera o texto da seção "TABELA DE SÍMBOLOS" do relatorio_saida.txt.
        if not self._historico:
            return "Tabela de Símbolos vazia.\n"
        linhas = ["NOME\t|\tTIPO\t|\tESCOPO",
                  "------------------------------------------"]
        for item in self._historico:
            linhas.append(f"{item['nome']}\t|\t{item['tipo']}\t|\t{item['escopo']}")
        return "\n".join(linhas) + "\n"